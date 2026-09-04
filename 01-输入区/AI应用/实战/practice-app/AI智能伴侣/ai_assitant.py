from logging import PlaceHolder
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).with_name(".env"))

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# 大标题
st.title("AI智能伴侣")

st.logo("./resources/Blossom_4k_Icon_1.webp")

# 创建AI大模型交互的客户端对象（API_KEY 环境变量名）
system_prompt = "你是一名非常可爱的10岁小男孩，你的名字叫布布，请你使用符合你人设的语气回答用户的问题。每一轮对话都要获取之前的消息记录，获取记忆，使对话连贯"

# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# 展示聊天信息
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    elif message["role"] == "assistant":
        st.chat_message("assistant").write(message["content"])

# ollama
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
ollama_model = os.getenv("OLLAMA_MODEL")
ollama_api_key = os.getenv("OLLAMA_API_KEY")

ollama_client = OpenAI(
    api_key=ollama_api_key,
    base_url=ollama_base_url
)


# 调用本地 Ollama
def ask_ollama(placeholder):
    full_reply = ""
    # print(st.session_state.messages)
    response = ollama_client.chat.completions.create(
        model=ollama_model,
        messages=st.session_state.messages,
        stream=True
    )

    for chunk in response:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            full_reply += delta
            placeholder.markdown(full_reply + "▌") # ▌是装饰用的光标，可去掉
    placeholder.markdown(full_reply) # 最后刷一次干净完整文本
    return full_reply

    # return response.choices[0].message.content

# zai
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


# 调用 GLM
def ask_glm(question):
    response = glm_client.chat.completions.create(
        model=glm_model,
        messages=[
            {"role": "system", "content": system_prompt}
        ],
        stream=False
    )

    # 非Stream方式解析方式
    return response.choices[0].message.content

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

# 调用 Grok
def ask_grok(question):
    url = f"{grok_base_url.rstrip('/')}/chat/completions"
    response = httpx.post(
        url,
        headers={
            "Authorization": f"Bearer {grok_api_key}"
        },
        json={
            "model": grok_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        },
        timeout=60,
        trust_env=False,
    )
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]


# fallback 调用
from openai import OpenAIError


def ask_ai(provider="auto", placeholder=None):
    # 手动选择模型
    if provider == "glm":
        return ask_glm()

    if provider == "ollama":
        return ask_ollama(placeholder)

    if provider == "grok":
        return ask_grok()

    # 自动选择
    if provider == "auto":
        try:
            print("切换到 Ollama...")
            return ask_ollama(placeholder)

        except OpenAIError as error:
            print("Ollama 调用失败：", error)

        try:
            print("正在使用 GLM...")
            return ask_glm()

        except OpenAIError as error:
            print("GLM 调用失败：", error)

        print("切换到 Grok...")
        return ask_grok()

    raise ValueError(f"不支持的 provider: {provider}")


# answer = ask_ai(
#     "用一句话解释什么是 AI Agent",
#     provider="ollama"
# )
#
# print("回答：", answer)


# 消息输入框
prompt = st.chat_input("请输入你要问的问题")
if prompt:  # 字符串会自动转换为bool，如果字符串为空返回False，非空返回True
    st.chat_message("user").write(prompt)
    print("------------------> 调用 AI 大模型，提示词：", prompt)  # 输出到终端中，用于调试
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()

    # 调用 AI 大模型
    ai_response = ask_ai("ollama", placeholder)
    print("<------------------ 大模型返回的结果：", ai_response)
    # st.chat_message("assistant").write(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
