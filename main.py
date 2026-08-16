# This code will ask question from ollama models llm using ollama locally inference

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3:8b ",
    temperature=0.2
)

response = llm.invoke(
    "Explain LangChain agents in simple terms."
)

print(response.content)