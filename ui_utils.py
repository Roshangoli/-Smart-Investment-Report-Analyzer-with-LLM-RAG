import streamlit as st
import pandas as pd
import plotly.express as px

def display_header():
    st.set_page_config(page_title="Smart Investment Report Analyzer", layout="wide")
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
    st.title("Smart Investment Report Analyzer")

def display_welcome_message():
    with st.expander("👋 Welcome! Here's how I can help you today:", expanded=True):
        st.markdown("""
        I'm your personal AI assistant for financial reports. My goal is to help you find the insights you need without the headache of manual analysis.
        
        **Here’s our game plan:**
        1.  **Upload a Document:** Share a financial report (PDF or DOCX) with me using the sidebar.
        2.  **Ask Me Anything:** Use plain English to ask questions about the report.
        3.  **Get Clear Answers:** I'll provide you with answers that are grounded in the document's content.
        
        Your documents are handled securely and are not stored after your session ends. Let's get started!
        """)

def display_sidebar():
    with st.sidebar:
        st.header("Let's Get Started 🚀")
        uploaded_file = st.file_uploader("Drop your financial report here", type=["pdf", "docx"])
        openai_api_key = st.text_input("Your OpenAI API Key", type="password", 
                                     help="I need this to understand your document. It's kept secure and only used for this session.")
        process_btn = st.button("Analyze My Document")
    return uploaded_file, openai_api_key, process_btn

def display_chat_interface(chat_history):
    st.header("Let's Chat About Your Report 💬")
    
    for i, message in enumerate(chat_history):
        if i % 2 == 0:
            st.markdown(f"<div style='background-color: #E3F2FD; padding: 10px; border-radius: 10px; margin-bottom: 10px;'><strong>You:</strong> {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: #F1F5F9; padding: 10px; border-radius: 10px; margin-bottom: 10px;'><strong>Financial Assistant:</strong> {message}</div>", unsafe_allow_html=True)
            
    question = st.text_input("What would you like to know?", placeholder="e.g., 'What was the revenue growth last year?'")
    
    if not chat_history:
        st.info("👆 Ask me anything about the report. I'll find the answers for you.")
        
    return question

def display_insights_dashboard(performance_logs, document_details):
    st.header("Your Insights Dashboard 📊")
    
    with st.expander("How I'm Performing For You", expanded=True):
        if performance_logs:
            qa_logs = [log for log in performance_logs if log["operation"] == "query_processing"]
            if qa_logs:
                avg_response_time = sum(log["processing_time"] for log in qa_logs) / len(qa_logs)
                st.metric("Average Answer Speed", f"{avg_response_time:.2f} sec")
                
                if len(qa_logs) > 1:
                    df = pd.DataFrame(qa_logs)
                    fig = px.line(df, y="processing_time", labels={"index": "Question #", "processing_time": "Response Time (s)"})
                    fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig, use_container_width=True)

    with st.expander("About Your Document"):
        if document_details:
            st.info(f"📄 You uploaded: {document_details['file_name']}")
            st.info(f"🧩 I divided it into {document_details['chunk_count']} pieces to better understand it.")
            st.info(f"⏱️ It took me {document_details['processing_time']:.2f} seconds to process everything.")

    with st.expander("How to Get the Best Answers From Me"):
        st.markdown("""
        💡 **Pro-tips for our conversation:**
        - **Be specific:** "What was the revenue in Q2 2023?" works better than "Tell me about revenue."
        - **Ask for comparisons:** "How did profits change from 2022 to 2023?" helps me find trends.
        - **Explore risks:** "What are the top 3 risks mentioned?" gets you focused insights.
        - **Request summaries:** "Summarize the outlook section" helps digest complex parts.
        """)

def display_initial_capabilities():
    st.info("👋 Hi there! To get started, please upload your financial report using the sidebar on the left.")
    st.header("Here's How I Can Help You 🌟")
    
    capabilities = [
        {"title": "Find Key Numbers Fast ⚡", "description": "Ask me things like 'What was our profit margin?' and I'll find it instantly."},
        {"title": "Decode Risk Factors 🛡️", "description": "I can explain what those dense risk sections actually mean for the business."},
        {"title": "Spot Year-Over-Year Trends 📈", "description": "Ask 'How did our expenses change from last year?' and I'll show you the patterns."},
        {"title": "Get the TL;DR Version 📝", "description": "Need a quick summary of the Management Discussion section? I've got you covered."},
        {"title": "Explain the Jargon 🔍", "description": "Don't know what 'adjusted EBITDA' means? Just ask me to explain it simply."},
    ]
    
    cols = st.columns(3)
    for i, cap in enumerate(capabilities):
        with cols[i % 3]:
            st.markdown(f"""<div style='background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; height: 200px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>  
            <h3 style='color: #2563EB;'>{cap['title']}</h3>
            <p>{cap['description']}</p>
            </div>""", unsafe_allow_html=True)

def display_footer():
    st.markdown("""<div style='margin-top: 50px; text-align: center; color: #64748B; font-size: 0.8em;'>
                Smart Investment Report Analyzer | Making financial documents less boring since 2023 ✨<br>
                Built with LangChain & OpenAI
                </div>""", unsafe_allow_html=True)