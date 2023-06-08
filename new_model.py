# pip install langchain==0.0.123
# pip install openai==0.27.2
# pip install redis==4.5.3
# pip install numpy
# pip install pandas
# pip install gdown

import os
import data

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.redis import Redis as RedisVectorStore
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import (
    ConversationalRetrievalChain,
    LLMChain
)
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.prompts.prompt import PromptTemplate
import templates

# set-up
os.environ['OPENAI_API_KEY'] = "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"

texts = [
    v['name'] for k, v in list(data.product_metadata.items())
]
metadatas = list(data.product_metadata.values())
embedding = OpenAIEmbeddings()
index_name = "products"
redis_url = "redis://localhost:6379"

print(1)
# creating the vecorized database in Redis
vectorstore = RedisVectorStore.from_texts(
    texts=texts,
    metadatas=metadatas,
    embedding=embedding,
    index_name=index_name,
    redis_url=redis_url
)


print(3)

# define two LLM models from OpenAI
llm = OpenAI(temperature=0)

streaming_llm = OpenAI(
    streaming=True,
    callback_manager=CallbackManager([
        StreamingStdOutCallbackHandler()
    ]),
    verbose=True,
    max_tokens=300,
    temperature=0.2
)

# use the LLM Chain to create a question creation chain
question_generator = LLMChain(
    llm=llm,
    prompt=templates.condense_question_prompt
)

# use the streaming LLM to create a question answering chain
doc_chain = load_qa_chain(
    llm=streaming_llm,
    chain_type="stuff",
    prompt=templates.qa_prompt
)


chatbot = ConversationalRetrievalChain(
    retriever=vectorstore.as_retriever(),
    combine_docs_chain=doc_chain,
    question_generator=question_generator
)

print(5)


# chat_history = []
# question = input("Hi! What are you looking for today?")

# # keep the bot running in a loop to simulate a conversation
# while True:
#     result = chatbot(
#         {"question": question, "chat_history": chat_history}
#     )
#     print("\n")
#     chat_history.append((result["question"], result["answer"]))
#     question = input()

def process_user_input(user_input, chat_history):
    if len(chat_history) == 0 or chat_history[-1][0] != user_input:
        result = chatbot(
            {"question": user_input, "chat_history": chat_history})
        chat_history.append((user_input, result["answer"]))
        return result["answer"]
    return ""
