import openai
import requests
import time
from config import LLM_BACKEND, OPENAI_API_KEY, OPENAI_API_BASE, GLM4_API_KEY, GLM4_API_URL, MOONSHOT_API_KEY, MOONSHOT_API_URL

class LLMClient:
    def __init__(self):
        if LLM_BACKEND == "openai":
            openai.api_key = OPENAI_API_KEY
            openai.api_base = OPENAI_API_BASE

    def generate(self, prompt, history=[]):
        if LLM_BACKEND == "openai":
            return self._call_openai(prompt, history)
        elif LLM_BACKEND == "glm4":
            return self._call_glm4(prompt, history)
        elif LLM_BACKEND == "moonshot":
            return self._call_moonshot(prompt, history)
        else:
            raise ValueError(f"Unsupported LLM_BACKEND: {LLM_BACKEND}")

    def _call_openai(self, prompt, history):
        messages = [{"role": "system", "content": "你是一个专业的劳动法智能顾问。"}] + history + [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.2,
            max_tokens=800,
        )
        return response.choices[0].message.content

    def _call_glm4(self, prompt, history):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GLM4_API_KEY}"
        }
        messages = [{"role": "system", "content": "你是一个专业的劳动法智能顾问。"}] + history + [{"role": "user", "content": prompt}]
        data = {
            "model": "glm-4",
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 1024
        }
        for attempt in range(3):
            try:
                response = requests.post(GLM4_API_URL, headers=headers, json=data, timeout=30)
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"GLM-4请求失败，重试 {attempt + 1}/3 次...")
                time.sleep(2)
        raise RuntimeError("GLM-4 API调用失败，请检查网络或配额")

    def _call_moonshot(self, prompt, history):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MOONSHOT_API_KEY}"
        }
        messages = [{"role": "system", "content": "你是一个专业的劳动法智能顾问。"}] + history + [{"role": "user", "content": prompt}]
        data = {
            "model": "moonshot-v1-8k",
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 1024
        }
        response = requests.post(MOONSHOT_API_URL, headers=headers, json=data, timeout=30)
        result = response.json()
        return result["choices"][0]["message"]["content"]