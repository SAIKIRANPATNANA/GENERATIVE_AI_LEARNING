from  prompt_templates import *
from core import * 
from langchain_community.vectorstores import FAISS
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import json
import requests
import pandas as pd
import pymongo
from mayyaDatabase import mongo_crud

def send_feedback(feedback):
    try: 
        uri = "mongodb+srv://saikiranpatnana:mayya143@saikiran.bdu0jbl.mongodb.net/?retryWrites=true&w=majority"
        mongo_op = mongo_crud.mongo_operation(uri,'ProjectSaadhana')
        database = mongo_op.create_database()
        collection = mongo_op.create_collection('feedback')
        mongo_records = mongo_op.read_record('feedback')
        client = pymongo.MongoClient(uri)  
        database = client["ProjectSaadhana"]  
        collection = database["feedback"] 
        cursor = collection.find()
        records = list(cursor)
        df = pd.DataFrame(records)
        client.close()
        for i in range(len(df)):
            if df.loc[i,'username'] == feedback['username']:
                return 0
            if df.loc[i,'mobile'] == feedback['mobile']:
                return 0
        mongo_op.insert_record(feedback,'feedback')
        return 1
    except Exception as e:
        print(e)
        return -1
   

def get_pdf_text(pdf):
    try: 
        text = str()
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
        return text 
    except Exception as e:
        print(e)
        return 0

def create_vector_store(text):
    try: 
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
        chunks=text_splitter.split_text(text)
        embeddings=GoogleGenerativeAIEmbeddings(model='models/embedding-001')
        vector_store=FAISS.from_texts(chunks,embeddings)
        vector_store.save_local("faiss_index")
        return 1
    except Exception as e:
        print(e)
        return 0

def get_context_specific(topic_name):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
        data_base = FAISS.load_local("faiss_index",embeddings)
        docs = data_base.similarity_search(topic_name)
        return docs
    except Exception as e:
        print(e)
        return 0

# def get_qa_chunks_general(text):
#     try: 
#         text_splitter=RecursiveCharacterTextSplitter(chunk_size=(len(text)/10),chunk_overlap=(len(text)/10)/10)
#         chunks = text_splitter.split_text(text)
#         return chunks
#     except Exception as e:
#         print(e)
#         return 0

def get_chunks_general(text):
  try:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=(len(text)/15),chunk_overlap=(len(text)/15)/10)
    chunks = text_splitter.split_text(text)
    for i in range(len(chunks)):
        if len(chunks[i])>10000:
            chunks[i] = chunks[i][:10000]
    if(len(chunks)>10):
        chunks = chunks[:10]
    chunks = ','.join(chunks)
    return chunks
  except Exception as e:
    print(e)
    return 0

# def get_mcq_chunks_general(text):
#     try:
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=(len(text)/15),chunk_overlap=(len(text)/15)/10)
#         chunks = text_splitter.split_text(text)
#         return chunks
#     except Exception as e:
#         print(e)
#         return 0


def get_mcq_specific(topic_name,difficulty_level,number):
    try: 
        output = get_context_specific(topic_name)
        if(output != 0):
            docs = output
        else:
            return 0,0
        prompt_template = get_mcq_prompt_template_specific(topic_name,difficulty_level,number)
        response = generate_mcq_specific(docs,prompt_template)
        cleaned_questions, cleaned_answers = get_cleaned_mcq_specific(response,docs,prompt_template)
        return cleaned_questions,cleaned_answers 
    except Exception as e:
        print(e)
        return 0,0

def get_mcq_general(text,difficulty_level,number):
    try:
        output = get_chunks_general(text)
        if(output!=0):
            chunks = output
        else:
            return 0,0
        cleaned_questions = list()
        cleaned_answers = list()
        response = generate_mcq_general(chunks,difficulty_level,number)
        cleaned_questions, cleaned_answers = get_cleaned_mcq_general(response,chunks,difficulty_level,number)
        return cleaned_questions,cleaned_answers
    except Exception as e:
        print(e)
        return 0,0

def get_qa_specific(topic_name,difficulty_level,number):
    try: 
        output = get_context_specific(topic_name)
        if(output!=0):
            docs = output
        else:
            return 0,0
        prompt_template = get_qa_prompt_template_specific(topic_name,difficulty_level,number)
        response = generate_qa_specific(docs,prompt_template)
        cleaned_questions,cleaned_answers = get_cleaned_qa_specific(response,docs,prompt_template)
        return cleaned_questions,cleaned_answers
    except Exception as e:
        print(e)
        return 0,0


def get_qa_general(text,difficulty_level,number):
    try:
        output =  get_chunks_general(text)
        if(output!=0):
            chunks = output
        else:
            return 0,0
        cleaned_questions = list()
        cleaned_answers = list()
        response = generate_qa_general(chunks,difficulty_level,number)
        cleaned_questions,cleaned_answers = get_cleaned_qa_general(response,chunks,difficulty_level,number)
        return cleaned_questions,cleaned_answers 
    except Exception as e:
        print(e)
        return 0,0

def evaluate_mcq(correct_answers,user_answers):
    try:
        score = 0
        wrong_answers = []
        for i in range(10):
            if(correct_answers[i] == user_answers[i]):
                score += 1
            else:
                wrong_answers.append(i)
        return score,wrong_answers
    except Exception as e:
        print(e)
        return -1,-1

def  descriptive_evaluator(user_answer,cleaned_answer):
    try:
        API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/msmarco-distilbert-base-tas-b"
        headers = {"Authorization": f"Bearer {'HUGGINGFACE_TOKEN_PLACEHOLDER'}"}
        def query(payload):
            try:
                response = requests.post(API_URL, headers=headers, json=payload)
                result = response.json()
                if(type(result)==dict):
                    return query(payload)
                else: 
                    return result[0]
            except Exception as e:
                print(e)
                return -1
        data = query(
                        {
                            "inputs": {
                                "source_sentence":cleaned_answer,
                                "sentences": [
                                    user_answer,
                                    user_answer,
                                ]
                            }
                        }
                    )
        return data
    except Exception as e:
        print(e)
        return -1

def evaluate_qa(cleaned_answers,user_answers):
    try:
        scores = list()
        for i in range(5):
            if user_answers[i] == '':
                scores.append(0)
            else:
                output = descriptive_evaluator(cleaned_answers[i],user_answers[i])
                if(output!=-1):
                    scores.append(output)
                else:
                    return -1
        return scores
    except Exception as e:
        print(e)
        return -1

       
        