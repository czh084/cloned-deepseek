from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory  # ✅ 修正后的导入路径
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import os

# 1. 创建历史记录存储池（支持多会话）
session_store = {}


def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


# 2. 构建新式对话链
def create_chat_chain(deepseek_api_key):
    model = ChatOpenAI(
        openai_api_key=deepseek_api_key,
        openai_api_base="https://api.deepseek.com",
        model="deepseek-chat",
    )

    # 定义提示模板（包含历史记录插槽）
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的科学知识助手"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    # 构建基础链
    chain = prompt | model

    # 包装历史管理
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )


# 3. 调用方式（带会话ID）
def get_chat_response(prompt, session_id="default", deepseek_api_key=None):
    chain = create_chat_chain(deepseek_api_key)
    return chain.invoke(
        {"input": prompt},
        config={"configurable": {"session_id": session_id}}
    ).content


# 使用示例
if __name__ == "__main__":
    api_key = os.getenv("DeepSeek API Key")

    # 会话1（物理问答）
    print(get_chat_response("牛顿提出过哪些知名定律？", "session_physics", api_key))

    # 会话2（数学问答）
    print(get_chat_response("微积分基本定理是什么？", "session_math", api_key))

    # 查询历史（需相同session_id）
    print(get_chat_response("我上一个问题是什么？", "session_physics", api_key))
