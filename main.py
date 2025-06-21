import streamlit as st
import utils  # 导入您的 utils 模块

st.title("克隆DeepSeek聊天")

# 使用固定会话ID（或根据用户生成唯一ID）
SESSION_ID = "default_user_session"

with st.sidebar:
    DeepSeek_API_Key = st.text_input("请输DeepSeek API密钥：", type="password")
    st.markdown("[获取DeepSeek API密钥](https://platform.deepseek.com/api_keys)")

    # 添加清空对话按钮
    if st.button("清空对话历史"):
        # 清除当前会话的历史记录
        if SESSION_ID in utils.session_store:
            del utils.session_store[SESSION_ID]
        st.session_state.messages = [{"role": "ai", "content": "您好，我是您的AI助手，有什么可以帮你的吗？"}]
        st.rerun()

# 初始化消息历史
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "您好，我是您的AI助手，有什么可以帮你的吗？"}
    ]

# 显示历史消息
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])


# API密钥验证函数（需添加到主程序）
def is_valid_deepseek_key(api_key):
    """验证DeepSeek API密钥格式"""
    return api_key.startswith("sk-") and len(api_key) == 35


prompt = st.chat_input()
if prompt:
    if not DeepSeek_API_Key:
        st.error("❌ 请输入你的DeepSeek API密钥")
        st.stop()
    elif not is_valid_deepseek_key(DeepSeek_API_Key.strip()):
        st.error("❌ 无效的API密钥格式！请确保输入的是DeepSeek API密钥（以'sk-'开头，共35个字符）")
        st.stop()

    # 添加用户消息到界面
    st.session_state.messages.append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍候..."):
        # 使用utils中的get_chat_response函数，传递session_id
        response = utils.get_chat_response(
            prompt=prompt,
            session_id=SESSION_ID,
            deepseek_api_key=DeepSeek_API_Key
        )

    # 添加AI回复到界面
    st.session_state.messages.append({"role": "ai", "content": response})
    st.chat_message("ai").write(response)
