import os
import data

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.redis import Redis as RedisVectorStore
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import (
    ConversationalRetrievalChain,
    LLMChain)
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import templates

# set-up
os.environ['OPENAI_API_KEY'] = "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"

texts = [
    v['name'] for k, v in list(data.product_metadata.items())
]
metadatas = list(data.product_metadata.values())
embedding = OpenAIEmbeddings()
index_name = "products"

# creating the vecorized database in Redis
vectorstore = RedisVectorStore.from_texts(
    texts=texts,
    metadatas=metadatas,
    embedding=embedding,
    index_name=index_name,
    redis_url="redis://localhost:6379"
)

# Initializing the LLMs to be utilized within the architeture.
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

question_generator = LLMChain(
    llm=llm,
    prompt=templates.condense_question_prompt
)

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


def process_user_input(user_input, chat_history):
    if len(chat_history) == 0 or chat_history[-1][0] != user_input:
        result = chatbot(
            {"question": user_input, "chat_history": chat_history})
        chat_history.append((user_input, result["answer"]))
        return result["answer"]
    return ""
