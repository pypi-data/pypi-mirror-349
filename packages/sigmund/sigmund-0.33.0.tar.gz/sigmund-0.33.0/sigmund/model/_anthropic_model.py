from . import BaseModel
from .. import config, utils
import logging
import json
logger = logging.getLogger('sigmund')


class AnthropicModel(BaseModel):
    
    supports_not_done_yet = False
    
    def __init__(self, sigmund, model, thinking=False, **kwargs):
        from anthropic import Anthropic, AsyncAnthropic
        super().__init__(sigmund, **kwargs)
        self._thinking = thinking
        self._model = model
        self._tool_use_id = 0
        self._client = Anthropic(api_key=config.anthropic_api_key)
        self._async_client = AsyncAnthropic(api_key=config.anthropic_api_key)
        
    def predict(self, messages, attachments=None, track_tokens=True):
        # import pprint
        # print('=== preparing tool messages')
        # pprint.pprint(messages)
        # print('---')        
        if isinstance(messages, str):
            return super().predict([self.convert_message(messages)],
                                   attachments, track_tokens)
        messages = utils.prepare_messages(messages, allow_ai_first=False,
                                          allow_ai_last=False,
                                          merge_consecutive=True)
        messages = [self.convert_message(message) for message in messages]
        # The Anthropic messages API doesn't accept tool results in a separate
        # message. Instead, tool results are included as a special content 
        # block in a user message. Since two subsequent user messages aren't
        # allowed, we need to convert a tool message to a user message and if
        # necessary merge it with the next user message.
        while True:
            logger.info('entering message postprocessing loop')
            for i, message in enumerate(messages):
                if message['role'] == 'tool':
                    if i == 0:
                        raise ValueError(
                            'The first message cannot be a tool message')
                    logger.info('converting tool message to user message')
                    tool_info = json.loads(message['content'])
                    message['role'] = 'user'
                    if tool_info['content'] is None:
                        tool_info['content'] = ''
                    message['content'] = [{
                        'type': 'tool_result',
                        'tool_use_id': str(self._tool_use_id),
                        'content': [{
                            'type': 'text',
                            'text': tool_info['content']
                        }]
                    }]
                    # The previous message needs to have a tool-use block
                    prev_message = messages[i - 1]
                    prev_message['content'] = [
                        {'type': 'text',
                         'text': prev_message['content']},
                        {'type': 'tool_use',
                         'id': str(self._tool_use_id),
                         'input': {'args': tool_info['args']},
                         'name': tool_info['name']
                        }
                    ]
                    self._tool_use_id += 1
                    if len(messages) > i + 1:
                        next_message = messages[i + 1]
                        if next_message['role'] == 'user':
                            logger.info('merging tool and user message')
                            message['content'].append({
                                "type": "text",
                                "text": next_message['content']
                            })
                            break
            else:
                break
            logger.info('dropping duplicate user message')
            messages.remove(next_message)
        # Attachments are included with the last message. The content is now
        # no longer a single str, but a list of dict
        if attachments:
            logger.info('adding attachments to last message')
            content = [{'type': 'text', 'text': messages[-1]['content']}]
            for attachment in attachments:
                # Decompose the HTML-style data into a mimetype and the 
                # actual data
                url = attachment['url']
                mimetype = url[5:url.find(';')]
                data = url[url.find(',') + 1:]
                if attachment['type'] == 'image':
                    content.append({
                        'type': 'image',
                        'source': {'type': 'base64',
                                   'media_type': mimetype,
                                   'data': data}
                    })
                elif attachment['type'] == 'document':
                    content.append({
                        'type': 'document',
                        'source': {'type': 'base64',
                                   'media_type': mimetype,
                                   'data': data}
                    })
            messages[-1]['content'] = content
        return super().predict(messages, attachments, track_tokens)
        
    def get_response(self, response):
        text = []
        for block in response.content:
            if block.type == 'tool_use':
                for tool in self._tools:
                    if tool.name == block.name:
                        return tool.bind(json.dumps(block.input))
                return self.invalid_tool
            if block.type == 'text':
                text.append(block.text)
        return '\n'.join(text)
        
        
    def _tool_args(self):
        if not self._tools:
            return {}
        alternative_format_tools = []
        for tool in self.tools():
            if tool['type'] == 'function':
                function = tool['function']
                alt_tool = {
                    "name": function['name'],
                    "description": function['description'],
                    "input_schema": function['parameters']
                }
                alternative_format_tools.append(alt_tool)
        return {'tools': alternative_format_tools}
        
    def _anthropic_invoke(self, fnc, messages):
        kwargs = self._tool_args()
        kwargs.update(config.anthropic_kwargs)
        # If the first message is the system prompt, we need to separate this
        # from the user and assistant messages, because the Anthropic messages
        # API takes this as a separate keyword argument
        if messages[0]['role'] == 'system':
            kwargs['system'] = messages[0]['content']
            messages = messages[1:]
        if self._thinking:
            kwargs['thinking'] = {
                "type": "enabled",
                "budget_tokens": config.anthropic_max_thinking_tokens
            }
        return fnc(model=self._model, messages=messages, **kwargs)
        
    def invoke(self, messages):
        return self._anthropic_invoke(self._client.messages.create, messages)
        
    def async_invoke(self, messages):
        return self._anthropic_invoke(self._async_client.messages.create,
                                      messages)
