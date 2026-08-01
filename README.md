#Chatbot

A powerful AI Chatbot application built with **LangChain**, **ChatGroq**, **Streamlit**, and **Pydantic**.

This project demonstrates advanced LangChain features including dynamic routing using `RunnableBranch`, concurrent output generation via `RunnableParallel`, native schema validation using `with_structured_output()`, and conversational memory handling.

---

## Features

- **Dynamic Query Routing (`RunnableBranch`):** Automatically classifies user queries into `Programming`, `Math`, or `General` categories and routes them to specialized system prompts.
- **Parallel Processing (`RunnableParallel`):** Concurrently generates concise response summaries and extracts relevant keywords from the generated answer.
- **Pydantic Structured Output:** Enforces strict response formatting and data type safety using `model.with_structured_output()`.
- **Conversational Memory(Extra add) :** Preserves multi-turn chat history (`HumanMessage` & `AIMessage`) across user sessions.
- **Interactive Streamlit UI:** Features a modern chat screen with history rendering and a clear button to reset conversations.

---

## Project Structure

```text
.
├── app.py             
├── chatbot.py       
├── prompts.py          
├── schemas.py          
├── requirements.txt    
├── .env.example   
└── README.md          
