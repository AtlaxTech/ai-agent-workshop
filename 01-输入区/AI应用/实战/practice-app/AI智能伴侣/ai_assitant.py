import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# st.set_page_config(
#     page_title="AI智能伴侣",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items={}
# )

# 大标题
# st.title("AI智能伴侣")

# st.logo("./resources/Blossom_4k_Icon_1.webp")

# 创建AI大模型交互的客户端对象（API_KEY 环境变量名）
# zai
load_dotenv(Path(__file__).with_name(".env"))
glm_api_key = os.getenv("ZAI_API_KEY")
glm_base_url = os.getenv("ZAI_BASE_URL")
glm_model = os.getenv("ZAI_MODEL")

# print("API Key 是否读取成功：", bool(api_key)) # 只是检查 Key 有没有读到，不会把真实 Key 打印出来。
# print("Base URL：", base_url) # 去环境变量里找一个名字叫 ZAI_API_KEY 的东西，把它的值拿回来。
# print("Model：", model)

glm_client = OpenAI(
    api_key=glm_api_key,
    base_url=glm_base_url
)

# print(glm_client)
# response = glm_client.chat.completions.create(
#     model=glm_model,
#     messages=[
#         {"role": "user", "content": "你好，请用一句话介绍你自己"}
#     ]
# )
# print(response.choices[0].message.content)

# ollama
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
ollama_model = os.getenv("OLLAMA_MODEL")
ollama_api_key = os.getenv("OLLAMA_API_KEY")

ollama_client = OpenAI(
    api_key=ollama_api_key,
    base_url=ollama_base_url
)

# print(ollama_client)
# response = ollama_client.chat.completions.create(
#     model=ollama_model,
#     messages=[
#         {"role": "user", "content": "你好，请用一句话介绍你自己"}
#     ]
# )
# print(response.choices[0].message.content)

# grok
# grok_api_key = os.getenv("BACKUP_API_KEY")
# grok_base_url = os.getenv("BACKUP_BASE_URL")
# grok_model = os.getenv("BACKUP_MODEL")
#
# grok_client = OpenAI(
#     api_key = grok_api_key,
#     base_url = grok_base_url
# )
# print(grok_client)
# try:
#     response = grok_client.chat.completions.create(
#         model=grok_model,
#         messages=[
#             {"role": "user", "content": "你好，请用一句话介绍你自己"}
#         ]
#     )
#     print(response.choices[0].message.content)
# except PermissionDeniedError as e:
#     print("状态码：", e.status_code)
#     print("服务器返回：", e.body)
#     print("响应头：", e.response.headers)

import httpx

# 1. 从 .env 读取 Grok 配置
grok_api_key = os.getenv("BACKUP_API_KEY")
grok_base_url = os.getenv("BACKUP_BASE_URL")
grok_model = os.getenv("BACKUP_MODEL")

# 2. 要发送给模型的数据
# data = {
#     "grok_model": grok_model,
#     "messages": [
#         {
#             "role": "user",
#             "content": "Hello"
#         }
#     ]
# }

# 3. Grok 的聊天接口地址
# url = f"{base_url.rstrip('/')}/chat/completions" # rstrip("/"): 把 URL 最后可能存在的 / 删除掉。

# 4. 向 Grok 发送 HTTP 请求
# response = httpx.post(
#     url,
#     headers={
#         "Authorization": f"Bearer {api_key}" # Bearer: 相当于告诉服务器：这是我的 API Key，请验证我的身份
#         # 最终 HTTP 请求大概长这样：Authorization: Bearer sk-xxxxxxxx
#     },
#     json=data,
#     timeout=60,
#     trust_env=False,   # 不读取系统代理环境变量
# )

# 5. 查看服务器返回结果
# print("状态码：", response.status_code)
# print("返回：", response.text)

# fallback 调用
from openai import OpenAIError


def ask_ai(question):
    # 1. 先尝试主模型 GLM
    try:
        print("正在使用 GLM...")

        response = glm_client.chat.completions.create(
            model=glm_model,
            messages=[
                {"role": "user", "content": question}
            ]
        )

        return response.choices[0].message.content

    # GLM 调用失败，就切换到本地 Ollama
    except OpenAIError as error:
        print("GLM 调用失败：", error)

    # 2. GLM 失败，再尝试本地 Ollama
    try:
        print("切换到 Ollama...")

        response = ollama_client.chat.completions.create(
            model=ollama_model,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except OpenAIError as error:
        print("Ollama 调用失败：", error)

    # 3. Ollama 也失败，最后使用 Grok
    print("切换到 Grok...")

    url = f"{grok_base_url.rstrip('/')}/chat/completions"

    response = httpx.post(
        url,
        headers={
            "Authorization": f"Bearer {grok_api_key}"
        },
        json={
            "model": grok_model,
            "messages": [
                {"role": "user", "content": question}
            ]
        },
        timeout=60,
        trust_env=False,
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]


answer = ask_ai("用一句话解释什么是 AI Agent")
print("回答：", answer)

# # 消息输入框
# prompt = st.chat_input("请输入你要问的问题")
# if prompt: # 字符串会自动转换为bool，如果字符串为空返回False，非空返回True
#     st.chat_message("user").write(prompt)
#     print("------------------> 调用 AI 大模型，提示词：", prompt) # 输出到终端中，用于调试
#
#     # 调用 AI 大模型
