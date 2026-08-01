import os
from typing import List, Union
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableParallel
from langchain_core.messages import HumanMessage, AIMessage

from prompts import (
    classifier_prompt,
    programming_prompt,
    math_prompt,
    general_prompt,
    summary_prompt,
    keywords_prompt
)
from schemas import ChatbotResponse

load_dotenv()

model = ChatGroq(model="llama-3.3-70b-versatile")
parser = StrOutputParser()
structured_model = model.with_structured_output(ChatbotResponse)

classifier_chain = classifier_prompt | model | parser

programming_chain = programming_prompt | model | parser
math_chain = math_prompt | model | parser
general_chain = general_prompt | model | parser

branch_chain = RunnableBranch(
    (
        lambda x: "programming" in x["category"].strip().lower(), programming_chain
    ),
    (
        lambda x: "math" in x["category"].strip().lower(), math_chain
    ),
    general_chain 
)

summary_chain = summary_prompt | model | parser
keywords_chain = keywords_prompt | model | parser

parallel_chain = RunnableParallel({
    "summary": summary_chain,
    "keywords_raw": keywords_chain
})

def format_chat_history(chat_history: List[Union[HumanMessage, AIMessage]]) -> str:
    formatted = ""
    for msg in chat_history:
        role = "User" if isinstance(msg, HumanMessage) else "Assistant"
        formatted += f"{role}: {msg.content}\n"
        
    return formatted if formatted else "No previous history."

def process_user_query(user_question: str, chat_history: List[Union[HumanMessage, AIMessage]] = None) -> ChatbotResponse:
    if chat_history is None:
        chat_history = []

    formatted_history = format_chat_history(chat_history)

    #Runnable Chain
    category = classifier_chain.invoke({"question": user_question})
    
    #RunnableBranch
    main_answer = branch_chain.invoke({
        "question": user_question,
        "category": category,
        "chat_history": formatted_history
    })
    
    #RunnableParallel
    parallel_outputs = parallel_chain.invoke({"text": main_answer})
    
    raw_keywords = parallel_outputs["keywords_raw"]

    structured_prompt = PromptTemplate(
        template="""
        You are a JSON formatting assistant. Format the provided information strictly according to the output schema.

        Detected Category: {category}
        Main Answer: {main_answer}
        Summary: {summary}
        Keywords Raw: {keywords_raw}
        """,
        input_variables=["category", "main_answer", "summary", "keywords_raw"]
    )
    
    final_structured_chain = structured_prompt | structured_model    
    pydantic_response = final_structured_chain.invoke({
        "category": category.strip(),
        "main_answer": main_answer,
        "summary": parallel_outputs["summary"],
        "keywords_raw": raw_keywords
    })
    
    return pydantic_response