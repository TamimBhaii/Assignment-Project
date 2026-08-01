from langchain_core.prompts import PromptTemplate

classifier_prompt = PromptTemplate(
    template="""
    You are a user query classifier.
    Classify the following user question as exactly one of these categories:
    - Programming
    - Math
    - General

    Return only one word: Programming, Math, or General.

    Question: 
    {question}
    """,
    input_variables=["question"]
)

programming_prompt = PromptTemplate(
    template="""
    You are an expert Programming Assistant. Help the user solve their programming question step-by-step with clear explanations and code if needed.

    Previous Conversation History:
    {chat_history}

    Question: 
    {question}
    """,
    input_variables=["chat_history", "question"]
)

math_prompt = PromptTemplate(
    template="""
    You are an encouraging Math Tutor. Break down the math problem clearly and explain the formulas and steps.

    Previous Conversation History:
    {chat_history}

    Question: 
    {question}
    """,
    input_variables=["chat_history", "question"]
)

general_prompt = PromptTemplate(
    template="""
    You are a helpful and versatile General Assistant. Answer the question concisely and accurately.

    Previous Conversation History:
    {chat_history}

    Question: 
    {question}
    """,
    input_variables=["chat_history", "question"]
)

summary_prompt = PromptTemplate(
    template="""
    Provide a concise 1-2 sentence summary for the following response:

    Text: {text}
    """,
    input_variables=["text"]
)

keywords_prompt = PromptTemplate(
    template="""
    Extract 3-5 key concepts or keywords from the following response. Return them as a comma-separated list.

    Text: {text}
    """,
    input_variables=["text"]
)