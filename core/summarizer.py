from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableSequence, RunnableLambda
import os 

def get_llm():
    return ChatMistralAI(
        model = "mistral-small-latest",
        mistral_api_key = os.getenv("MISTRAL_API_KEY"),
        temperature = 0.3
    )

def split_transcript(transcript :str) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
    )
    return text_splitter.split_text(transcript)

def summarize(transcript :str) ->str:
    llm = get_llm()
    map_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert summarizer. Summarize the following content concisely while preserving all important information."),
            ("human","{text}")
        ]
    )

    parser = StrOutputParser()

    chain = map_prompt | llm | parser

    chunks = split_transcript(transcript)

    chunk_summaries = [chain.invoke({"text":chunk}) for chunk in chunks]

    combined_summary ="\n\n".join(chunk_summaries)

    combined_prompt = ChatPromptTemplate.from_messages(
        [
            ("system",  "You are an expert meeting summarizer. Combine these partial summaries "),
            ("human", "{text}")
        ]
    )

    combined_chain = combined_prompt | llm | parser

    final_summary = combined_chain.invoke({"text":combined_summary})

    return final_summary

def generate_title(summary :str) ->str:

    llm = get_llm()

    tprompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert at generating concise and informative titles. " "Based on the following summary, generate a professional title ""(maximum 8 words). Return only the title."),
            ("human", "{text}")

        ]
    )
    parser = StrOutputParser()

    chain = tprompt | llm | parser

    title = chain.invoke({"text":summary})

    return title





