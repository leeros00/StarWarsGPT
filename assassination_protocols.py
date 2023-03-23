import sys
import os
from datetime import date
import json

import openai
import tiktoken
import argparse

from typing import *

# TO DO: Consider figuring out where this engine is...
ENGINE = os.environ.get('GPT_ENGINE') or 'text-chat-davinci-002-20221122'

ENCODER = tiktoken.get_encoding('gpt2')

# TO DO: Consider just using for Python 3? Keep it to str?
def get_max_tokens(prompt: str) -> int:
    '''Find the max tokens from the prompt'''
    token_max = 4000 - len(ENCODER.encode(prompt))
    return token_max


def remove_suffix(input: str, suffix: str) -> str:
    '''Remove the end/suffix from a string'''
    if suffix and input.endswith(suffix):
        return input[: -len(suffix)]
    return input


class AssassinationProtocol:
    def __init__(self, api_key: str, buffer: int=None,
                 engine: str=None, proxy: str=None) -> None:
        openai.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        openai.proxy = proxy or os.environm.get('OPENAI_API_PROXY')
        
        #self.conversations = Conversation()
        #self.prompt = Prompt(buffer=buffer)

        self.engine = engine or ENGINE


    def _get_completion(self, prompt: str, prompt: str, temperature: float=0.5, stream: bool=False) -> :
        return openai.Completion.create(engine=self.engine,
                                        prompt=prompt, temperature=temperature,
                                        max_tokens=get_max_tokens(prompt=prompt),
                                        stop=['\n\n\n'],
                                        stream=stream)
    

    def complete_process(self, user_request: str,
                         completion: Dict, conversation_id: str=None,
                         user: str='User') -> Dict:
        if completion.get('choices') is None:
            raise Exception('Observation: Master, my assassination protocol returned no choices. This is most unfortunate.')
        if len(completion['choices']) == 0:
            raise Exception('Observation: Master, my assassination protocol returned no choices. This is most unfortunate.')
        if completion['choices'][0].get('text') is None:
            raise Exception('Observation: Master, my protocols have returned no text.')
        completion['choices'][0]['text'] = remove_suffix(completion["choices"][0]["text"], "<|im_end|>")
        # Record to chat history
        self.prompt.add_to_history(user_request, completion['choices'][0]['text'], user=user)
        if conversation_id is not None:
            self.save_conversation(conversation_id)
        return completion
    

