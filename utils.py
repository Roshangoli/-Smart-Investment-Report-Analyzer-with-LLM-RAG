import os
import time
import logging
from typing import List, Dict, Any, Tuple

# Import our document processing tools
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import Document

# Set up friendly logging to track what's happening behind the scenes
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('investment_analyzer')

class DocumentProcessor:
    """Your friendly document assistant that handles loading, understanding, and answering questions about financial reports."""
    
    def __init__(self, openai_api_key: str):
        """Get everything ready to process your documents."""
        self.openai_api_key = openai_api_key
        os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # How we break down documents into manageable pieces
        self.chunk_size = 1500      # Each piece is about a page of text
        self.chunk_overlap = 150    # Overlap ensures we don't miss context between pieces
        
        # We keep track of how we're performing to help improve over time
        self.performance_logs = []
    
    def load_document(self, file_path: str) -> Tuple[List[Document], Dict[str, Any]]:
        """Open and read your financial document so we can work with it."""
        start_time = time.time()
        
        try:
            # Figure out what kind of document you've shared with us
            if file_path.endswith('.pdf'):
                logger.info(f"Opening your PDF document: {os.path.basename(file_path)}")
                loader = PyPDFLoader(file_path)
                documents = loader.load()
                file_type = 'pdf'
            elif file_path.endswith('.docx'):
                logger.info(f"Opening your Word document: {os.path.basename(file_path)}")
                loader = Docx2txtLoader(file_path)
                documents = loader.load()
                file_type = 'docx'
            else:
                raise ValueError(f"I can't read this file type yet: {file_path}. Please use PDF or DOCX files.")
            
            # Keep track of how we're doing
            processing_time = time.time() - start_time
            performance_data = {
                "operation": "document_loading",
                "file_type": file_type,
                "page_count": len(documents),
                "processing_time": processing_time
            }
            
            self.performance_logs.append(performance_data)
            logger.info(f"Successfully read your {file_type} document with {len(documents)} pages in {processing_time:.2f} seconds")
            
            return documents, performance_data
            
        except Exception as e:
            logger.error(f"Hmm, I had trouble reading your document: {str(e)}")
            raise
    
    def split_documents(self, documents: List[Document]) -> Tuple[List[Document], Dict[str, Any]]:
        """Break down your document into smaller, digestible pieces so we can understand it better."""
        start_time = time.time()
        
        try:
            logger.info("Breaking down your document into smaller sections for better understanding...")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
            
            splits = text_splitter.split_documents(documents)
            
            # Keep track of our progress
            processing_time = time.time() - start_time
            performance_data = {
                "operation": "document_splitting",
                "input_docs": len(documents),
                "output_chunks": len(splits),
                "chunk_size": self.chunk_size,
                "chunk_overlap": self.chunk_overlap,
                "processing_time": processing_time
            }
            
            self.performance_logs.append(performance_data)
            logger.info(f"Successfully divided your {len(documents)} document pages into {len(splits)} manageable pieces in {processing_time:.2f} seconds")
            
            return splits, performance_data
            
        except Exception as e:
            logger.error(f"I had trouble breaking down your document: {str(e)}")
            raise
    
    def create_vectorstore(self, splits: List[Document]) -> Tuple[Chroma, Dict[str, Any]]:
        """Build a smart knowledge base from your document that we can search through quickly."""
        start_time = time.time()
        
        try:
            logger.info("Creating a smart searchable database from your document...")
            embeddings = OpenAIEmbeddings()
            vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
            
            # Track our progress
            processing_time = time.time() - start_time
            performance_data = {
                "operation": "vectorstore_creation",
                "chunk_count": len(splits),
                "processing_time": processing_time
            }
            
            self.performance_logs.append(performance_data)
            logger.info(f"Successfully created a searchable knowledge base from {len(splits)} document sections in {processing_time:.2f} seconds")
            
            return vectorstore, performance_data
            
        except Exception as e:
            logger.error(f"I had trouble creating the searchable database: {str(e)}")
            raise
    
    def create_qa_chain(self, vectorstore: Chroma, model_name: str = "gpt-3.5-turbo-16k") -> ConversationalRetrievalChain:
        """Connect an AI assistant to your document so you can have a conversation about it."""
        start_time = time.time()
        
        try:
            logger.info(f"Setting up your AI assistant using {model_name}...")
            llm = ChatOpenAI(temperature=0, model_name=model_name)
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm,
                vectorstore.as_retriever(search_kwargs={"k": 6}),  # We look at 6 sections of your document for each question
                return_source_documents=True
            )
            
            # Track our setup time
            processing_time = time.time() - start_time
            performance_data = {
                "operation": "qa_chain_creation",
                "model": model_name,
                "processing_time": processing_time
            }
            
            self.performance_logs.append(performance_data)
            logger.info(f"Your AI assistant is ready to answer questions about your document! Setup took {processing_time:.2f} seconds")
            
            return qa_chain
            
        except Exception as e:
            logger.error(f"I had trouble setting up the AI assistant: {str(e)}")
            raise
    
    def process_query(self, qa_chain: ConversationalRetrievalChain, query: str, chat_history: List[Tuple[str, str]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Find the answer to your question by searching through the document."""
        start_time = time.time()
        
        try:
            logger.info(f"Searching for an answer to: '{query}'")
            result = qa_chain({"question": query, "chat_history": chat_history})
            
            # Track how quickly we found your answer
            processing_time = time.time() - start_time
            performance_data = {
                "operation": "query_processing",
                "query_length": len(query),
                "response_length": len(result["answer"]),
                "processing_time": processing_time
            }
            
            self.performance_logs.append(performance_data)
            logger.info(f"Found an answer to your question in {processing_time:.2f} seconds")
            
            return result, performance_data
            
        except Exception as e:
            logger.error(f"I had trouble answering your question: {str(e)}")
            raise
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a friendly overview of how we've been performing for you."""
        if not self.performance_logs:
            return {}
        
        # Collect all our performance stats
        summary = {
            "total_operations": len(self.performance_logs),
            "total_processing_time": sum(log["processing_time"] for log in self.performance_logs),
            "operation_counts": {},
            "average_times": {}
        }
        
        # Group our activities by type
        operation_groups = {}
        for log in self.performance_logs:
            op = log["operation"]
            if op not in operation_groups:
                operation_groups[op] = []
            operation_groups[op].append(log)
        
        # Calculate how quickly we're responding on average
        for op, logs in operation_groups.items():
            summary["operation_counts"][op] = len(logs)
            summary["average_times"][op] = sum(log["processing_time"] for log in logs) / len(logs)
        
        logger.info(f"Performance summary: Handled {summary['total_operations']} operations in {summary['total_processing_time']:.2f} seconds total")
        return summary