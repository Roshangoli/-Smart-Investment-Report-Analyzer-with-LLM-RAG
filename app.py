import streamlit as st
import os
import tempfile
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import time
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="Investment Report Analyzer", layout="wide")

# Custom CSS for a more professional look
st.markdown("""
<style>
    .main {background-color: #f5f7f9;}
    .stApp {max-width: 1200px; margin: 0 auto;}
    h1 {color: #1E3A8A;}
    h2 {color: #2563EB;}
    .stButton>button {background-color: #2563EB; color: white;}
    .stButton>button:hover {background-color: #1E40AF;}
    .report-container {background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'document_processed' not in st.session_state:
    st.session_state.document_processed = False
if 'qa' not in st.session_state:
    st.session_state.qa = None
if 'performance_logs' not in st.session_state:
    st.session_state.performance_logs = []

# Title and introduction with a more welcoming tone
st.title("Smart Investment Report Analyzer")

with st.expander("ℹ️ About this app", expanded=True):
    st.markdown("""
    👋 Welcome! I'm your AI financial report assistant.
    
    I'll help you unlock insights from complex financial documents without the headache of manual analysis. Here's how we can work together:
    
    1. 📄 Upload your financial document (PDF or DOCX)
    2. 💬 Ask me questions in everyday language
    3. ✨ Get clear insights backed by your document's actual content
    
    I use advanced AI to understand both your questions and your document, finding the most relevant information for you.
    
    Don't worry about security - your documents aren't stored permanently, and all processing happens securely.
    """)

# Sidebar for document upload and processing with friendlier language
with st.sidebar:
    st.header("Let's Get Started 🚀")
    uploaded_file = st.file_uploader("Drop your financial report here", type=["pdf", "docx"])
    
    # API Key input with friendlier help text
    openai_api_key = st.text_input("Your OpenAI API Key", type="password", 
                                 help="I need this to analyze your document. Don't worry - it's only used for this session and not stored anywhere.")
    
    # Process document button with more engaging text
    process_btn = st.button("Analyze My Document")
    
    if process_btn and uploaded_file and openai_api_key:
        with st.spinner("Processing your document... This might take a minute."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # Load document based on file type
            start_time = time.time()
            
            if uploaded_file.name.endswith('.pdf'):
                loader = PyPDFLoader(tmp_path)
                document = loader.load()
                st.sidebar.success(f"PDF loaded: {len(document)} pages")
            elif uploaded_file.name.endswith('.docx'):
                loader = Docx2txtLoader(tmp_path)
                document = loader.load()
                st.sidebar.success(f"DOCX loaded successfully")
            
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=150
            )
            splits = text_splitter.split_documents(document)
            st.sidebar.info(f"Document split into {len(splits)} chunks for processing")
            
            # Create embeddings and store in vector database
            try:
                os.environ["OPENAI_API_KEY"] = openai_api_key
                embeddings = OpenAIEmbeddings()
                vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
                
                # Create retrieval chain
                llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
                st.session_state.qa = ConversationalRetrievalChain.from_llm(
                    llm,
                    vectorstore.as_retriever(search_kwargs={"k": 6}),
                    return_source_documents=True
                )
                
                processing_time = time.time() - start_time
                st.sidebar.success(f"✅ Document processed in {processing_time:.2f} seconds!")
                st.session_state.document_processed = True
                
                # Log performance
                st.session_state.performance_logs.append({
                    "operation": "document_processing",
                    "file_name": uploaded_file.name,
                    "chunks": len(splits),
                    "processing_time": processing_time
                })
                
                # Clean up temp file
                os.unlink(tmp_path)
                
            except Exception as e:
                st.sidebar.error(f"Error processing document: {str(e)}")
    
    elif process_btn and not uploaded_file:
        st.sidebar.warning("Oops! I need a document to analyze. Could you upload one first?")
    elif process_btn and not openai_api_key:
        st.sidebar.warning("I need your OpenAI API key to work my magic. Mind adding it above?")

# Main content area
if st.session_state.document_processed:
    # Create two columns for chat and insights
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Let's Chat About Your Report 💬")
        
        # Display chat history with more personalized labels
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:  # User message
                st.markdown(f"<div style='background-color: #E3F2FD; padding: 10px; border-radius: 10px; margin-bottom: 10px;'><strong>You:</strong> {message}</div>", unsafe_allow_html=True)
            else:  # AI response
                st.markdown(f"<div style='background-color: #F1F5F9; padding: 10px; border-radius: 10px; margin-bottom: 10px;'><strong>Financial Assistant:</strong> {message}</div>", unsafe_allow_html=True)
        
        # Input for new question with more engaging placeholder
        question = st.text_input("What would you like to know?", placeholder="E.g., 'What was the revenue growth last year?' or 'Explain the main risk factors...'")
        
        # Add a hint for first-time users if chat history is empty
        if not st.session_state.chat_history:
            st.info("👆 Ask me anything about the financial report. I'll search through the document and give you specific answers based on its content.")
        
        if question and question.strip():
            # Add user question to chat history
            st.session_state.chat_history.append(question)
            
            # Get answer from QA chain with more engaging spinner text
            with st.spinner("Searching through your document for insights..."):
                start_time = time.time()
                result = st.session_state.qa({"question": question, "chat_history": [(st.session_state.chat_history[i], st.session_state.chat_history[i+1]) for i in range(0, len(st.session_state.chat_history)-1, 2)] if len(st.session_state.chat_history) > 1 else []})
                answer_time = time.time() - start_time
            
            # Add answer to chat history
            st.session_state.chat_history.append(result["answer"])
            
            # Log performance
            st.session_state.performance_logs.append({
                "operation": "question_answering",
                "question": question,
                "response_time": answer_time
            })
            
            # Force refresh
            st.experimental_rerun()
    
    with col2:
        st.header("Your Insights Dashboard 📊")
        
        # Performance metrics with more engaging descriptions
        with st.expander("How I'm Performing For You", expanded=True):
            if st.session_state.performance_logs:
                qa_logs = [log for log in st.session_state.performance_logs if log["operation"] == "question_answering"]
                if qa_logs:
                    avg_response_time = sum(log["response_time"] for log in qa_logs) / len(qa_logs)
                    st.metric("How quickly I find answers", f"{avg_response_time:.2f} sec")
                    
                    # Create response time chart
                    if len(qa_logs) > 1:
                        df = pd.DataFrame(qa_logs)
                        fig = px.line(df, y="response_time", labels={"index": "Question #", "response_time": "Response Time (s)"})
                        fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
                        st.plotly_chart(fig, use_container_width=True)
        
        # Document stats with more conversational descriptions
        with st.expander("About Your Document"):
            doc_logs = [log for log in st.session_state.performance_logs if log["operation"] == "document_processing"]
            if doc_logs:
                st.info(f"📄 You uploaded: {doc_logs[0]['file_name']}")
                st.info(f"🧩 I divided it into {doc_logs[0]['chunks']} pieces to better understand it")
                st.info(f"⏱️ It took me {doc_logs[0]['processing_time']:.2f} seconds to process everything")
        
        # Tips for better questions with more conversational tone
        with st.expander("How to Get the Best Answers From Me"):
            st.markdown("""
            💡 Here are some tips to help us have a great conversation:
            
            - **Be specific**: "What was the revenue in Q2 2023?" works better than "Tell me about revenue"
            - **Ask for comparisons**: "How did profits change from 2022 to 2023?" helps me find trends
            - **Explore risk factors**: "What are the top 3 risks mentioned?" gets you focused insights
            - **Request summaries**: "Summarize the outlook section" helps digest complex parts
            - **Follow up**: If my answer isn't quite what you needed, ask me to clarify or go deeper!
            """)

else:
    # Display instructions when no document is processed - more conversational
    st.info("👋 Hi there! To get started, please upload your financial report using the sidebar on the left.")
    
    # Sample capabilities with more engaging header
    st.header("Here's How I Can Help You 🌟")
    
    capabilities = [
        {"title": "Find Key Numbers Fast ⚡", "description": "Just ask me things like 'What was our profit margin?' and I'll find it instantly - no more ctrl+F struggles!"},
        {"title": "Decode Risk Factors 🛡️", "description": "I can explain what those dense risk sections actually mean for the business in plain language."},
        {"title": "Spot Year-Over-Year Trends 📈", "description": "Ask 'How did our expenses change from last year?' and I'll show you the important patterns."},
        {"title": "Get the TL;DR Version 📝", "description": "Need a quick summary of the Management Discussion section? I've got you covered."},
        {"title": "Explain the Jargon 🔍", "description": "Don't know what 'adjusted EBITDA' means in this context? Just ask me to explain it simply."},
    ]
    
    # Display capabilities in a grid
    cols = st.columns(3)
    for i, cap in enumerate(capabilities):
        with cols[i % 3]:
            st.markdown(f"""<div style='background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; height: 200px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>  
            <h3 style='color: #2563EB;'>{cap['title']}</h3>
            <p>{cap['description']}</p>
            </div>""", unsafe_allow_html=True)

# Footer with more personality
st.markdown("""<div style='margin-top: 50px; text-align: center; color: #64748B; font-size: 0.8em;'>
            Smart Investment Report Analyzer | Making financial documents less boring since 2023 ✨<br>
            Built with LangChain & OpenAI
            </div>""", unsafe_allow_html=True)