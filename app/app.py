import json

import streamlit as st
from langchain_core.messages import ToolMessage
from llm import agent_executor

st.title("Dify Sandbox Chat App")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = agent_executor.invoke(
            {"messages": prompt},
            config={"configurable": {"thread_id": "example_session"}},
        )
        if isinstance(response["messages"][-2], ToolMessage):
            tool_content = response["messages"][-2].content
            code = json.loads(tool_content)["code"]
            result = json.loads(tool_content).get(
                "result", json.loads(tool_content).get("error")
            )

        content = response["messages"][-1].content
        display_content = (
            f"#### コード\n```python\n{code}\n```\n\n#### 結果\n{result}\n\n{content}"
        )
        st.markdown(display_content)
        st.session_state.messages.append(
            {"role": "assistant", "content": display_content}
        )
