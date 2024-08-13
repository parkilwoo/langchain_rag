from rag_chain.extractor.document import DocumentExtractor
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from rag_chain.prompter.chat_prompt import ChatPrompt
from rag_chain.connector.open_ai import OpeanAiConnector
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
# from langchain.chains import ConversationChain
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationSummaryMemory



# document_extractor = DocumentExtractor("./test.pdf", RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#                                                         chunk_size=1000,
#                                                         chunk_overlap=200,
#                                                         encoding_name='cl100k_base'
#                                                     ))
# docs = document_extractor.docs

# from rag_chain.store.vector import VectorStore
# VectorStore.add_document(docs)

# # search_kwargs = {
# #     'search_type': "similarity_score_threshold",
# #     'search_kwargs': {"score_threshold": 0.5}
# # }

# retriever = VectorStore.get_retriever(search_kwargs={'k': 1})
# prompt = ChatPrompt.get_prompt()

# openai_connector = OpeanAiConnector("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", "gpt-4o-2024-08-06")
# llm_model = openai_connector.get_connector()

# def format_docs(docs):
#     # 검색한 문서 결과를 하나의 문단으로 합쳐줍니다.
#     return "\n\n".join(doc.page_content for doc in docs)


# # 단계 8: 체인 생성(Create Chain)
# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | openai_connector.get_connector()
#     | StrOutputParser()
# )


# # question = "신용정보법 제22조의 9에 대해서 알려줘."
# # resp = rag_chain.invoke(question)
# # print(resp)

# conversation = ConversationChain(
#     llm=llm_model,
#     memory = ConversationSummaryMemory(llm=llm_model, return_messages=True)
# )

# resp = conversation.invoke("나는 박일우야. 나이는 33살이고, 직업은 프로그래머야")
# print(resp)
# resp_2 = conversation.invoke("내 인공지능 비서 이름이 뭐지?")
# print(resp_2)
# resp_3 = conversation.invoke("내 정보를 알려줘.")
# print(resp_3)

from infrastructure.connector.open_ai import OpenAiConnector
async def test():
    conn = OpenAiConnector("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", "gpt-4o-2024-08-06")
    # conn = OpenAiConnector("adsad", "gpt-3.5-turbo-instruct")
    await conn.test_connection()

import asyncio
asyncio.run(test())
    