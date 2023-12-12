import logging
import openai
import os
import json

from module.get_source import load_talkchannel, load_from_file

# 환경 변수 처리 필요!

SYSTEM_MSG = "당신은 카카오 서비스 제공자입니다."
logger = logging.getLogger("aibot")


class AIBot(object):
    def __init__(self, system_msg=''):
        openai.api_key = load_from_file('../KEY')
        self.aibot = openai
        self.system_msg = system_msg
        self.temperature = 0.1
        self.gpt_model = "gpt-3.5-turbo"

        self.functions = [{
            "name": "what_is_talkchannel",
            "description": "decription for kakaotalkchannel in korean",
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": [],
            },
        }]
        self.available_functions = {
            "what_is_talkchannel": load_talkchannel,
        }

    def _call_function(self, function_name, **args):
        if function_name in self.available_functions.keys():
            return self.available_functions[function_name](**args)
        logger.error(f"%s is not available", function_name)

    def req_to_openai_with_func(self, query):
        message_log = [
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": query},
        ]
        response = self.aibot.ChatCompletion.create(
            model=self.gpt_model,
            messages=message_log,
            temperature=0,
            functions=self.functions,
            function_call='auto',
        )
        response_message = response["choices"][0]["message"]
        logging.debug(response_message)

        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_response = self._call_function(function_name, **json.loads(response_message["function_call"]["arguments"]))
            message_log.append(response_message)  # GPT의 지난 답변을 message_logs에 추가하기
            message_log.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )
            response = self.aibot.ChatCompletion.create(
                model=self.gpt_model,
                messages=message_log,
                temperature=self.temperature,
            )  # 함수 실행 결과를 GPT에 보내 새로운 답변 받아오기

        return response.choices[0].message.content


if __name__ == "__main__":
    ai = AIBot()
    logger.setLevel(logging.DEBUG)
    print(ai.req_to_openai_with_func(query="채팅 API는 어떤게 있어?"))