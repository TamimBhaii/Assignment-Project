import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from chatbot import process_user_query

st.set_page_config(page_title="Chatbot")
st.title("Chatbot")

#Memory Session State 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "display_history" not in st.session_state:
    st.session_state.display_history = []

st.sidebar.title("Options")
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.session_state.display_history = []
    st.rerun()

for item in st.session_state.display_history:
    if item["role"] == "user":
        with st.chat_message("user"):
            st.write(item["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(f"**Detected Category:** `{item['category']}`")
            st.markdown(f"### Answer:\n{item['content']}")
            st.info(f"**Summary:** {item['summary']}")
            st.markdown(f"**Keywords:** {item['keywords']}")


if user_input := st.chat_input("Ask a programming, math, or general question..."):
    

    with st.chat_message("user"):
        st.write(user_input)


    with st.chat_message("assistant"):
        with st.spinner("Thinking & Processing Pipeline..."):
            try:
                response = process_user_query(user_input, st.session_state.chat_history)

                st.markdown(f"**Detected Category:** `{response.category}`")
                st.markdown(f"### Answer:\n{response.main_answer}")
                st.info(f"**Summary:** {response.summary}")
                
                keywords_str = ", ".join([f"`{k}`" for k in response.keywords])
                st.markdown(f"**Keywords:** {keywords_str}")

                #Update Memory (HumanMessage & AIMessage)
                st.session_state.chat_history.append(HumanMessage(content=user_input))
                st.session_state.chat_history.append(AIMessage(content=response.main_answer))
                
                st.session_state.display_history.append({
                    "role": "user",
                    "content": user_input
                })
                st.session_state.display_history.append({
                    "role": "assistant",
                    "category": response.category,
                    "content": response.main_answer,
                    "summary": response.summary,
                    "keywords": keywords_str
                })

            except Exception as e:
                st.error(f"An error occurred: {e}")