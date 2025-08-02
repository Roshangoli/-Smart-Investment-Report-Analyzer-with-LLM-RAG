import os
import time
import logging
from typing import List, Dict, Any, Tuple
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import Document

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('investment_analyzer')

class DocumentProcessor:
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.performance_logs = []
    
    def load_document(self, file_path: str) -> Tuple[List[Document], Dict[str, Any]]:
        start_time = time.time()
        try:
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents = loader.load()
                file_type = 'pdf'
            elif file_path.endswith('.docx'):
                loader = Docx2txtLoader(file_path)
                documents = loader.load()
                file_type = 'docx'
            else:
                raise ValueError(f"Unsupported file type: {file_path}")
            
            processing_time = time.time() - start_time
            performance_data = {
                "operation": "document_loading",
                "file_type": file_type,
                "page_count": len(documents),
                "processing_time": processing_time
            }
            self.performance_logs.append(performance_data)
            logger.info(f"Loaded {len(documents)} pages from {file_type} document in {processing_time:.2f}s.")
            return documents, performance_data
        except Exception as e:
            logger.error(f"Error loading document: {e}")
            raise
    
    def split_documents(self, documents: List[Document]) -> Tuple[List[Document], Dict[str, Any]]:
        start_time = time.time()
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
            splits = text_splitter.split_documents(documents)
            
            processing_time = time.time() - start_time
            performance_data = {
                "operation": "document_splitting",
                "input_docs": len(documents),
                "output_chunks": len(splits),
                "processing_time": processing_time
            }
            self.performance_logs.append(performance_data)
            logger.info(f"Split {len(documents)} documents into {len(splits)} chunks in {processing_time:.2f}s.")
            return splits, performance_data
        except Exception as e:
            logger.error(f"Error splitting documents: {e}")
            raise
    
    def create_vectorstore(self, splits: List[Document]) -> Tuple[Chroma, Dict[str, Any]]:
        start_time = time.time()
        try:
            embeddings = OpenAIEmbeddings()
            vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
            
            processing_time = time.time() - start_time
            performance_data = {
                "operation": "vectorstore_creation",
                "chunk_count": len(splits),
                "processing_time": processing_time
            }
            self.performance_logs.append(performance_data)
            logger.info(f"Created vector store from {len(splits)} chunks in {processing_time:.2f}s.")
            return vectorstore, performance_data
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def create_qa_chain(self, vectorstore: Chroma) -> ConversationalRetrievalChain:
        try:
            llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm,
                vectorstore.as_retriever(search_kwargs={"k": 6}),
                return_source_documents=True
            )
            logger.info("Created Q&A chain.")
            return qa_chain
        except Exception as e:
            logger.error(f"Error creating Q&A chain: {e}")
            raise
    
    def process_query(self, qa_chain: ConversationalRetrievalChain, query: str, chat_history: List[Tuple[str, str]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        start_time = time.time()
        try:
            result = qa_chain({"question": query, "chat_history": chat_history})
            
            processing_time = time.time() - start_time
            performance_data = {
                "operation": "query_processing",
                "query_length": len(query),
                "response_length": len(result["answer"]),
                "processing_time": processing_time
            }
            self.performance_logs.append(performance_data)
            logger.info(f"Processed query in {processing_time:.2f}s.")
            return result, performance_data
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise

    def get_performance_summary(self) -> Dict[str, Any]:
        if not self.performance_logs:
            return {}
        
        summary = {
            "total_operations": len(self.performance_logs),
            "total_processing_time": sum(log["processing_time"] for log in self.performance_logs),
            "operation_counts": {},
            "average_times": {}
        }
        
        operation_groups = {}
        for log in self.performance_logs:
            op = log["operation"]
            if op not in operation_groups:
                operation_groups[op] = []
            operation_groups[op].append(log)
        
        for op, logs in operation_groups.items():
            summary["operation_counts"][op] = len(logs)
            summary["average_times"][op] = sum(log["processing_time"] for log in logs) / len(logs)
        
        return summary