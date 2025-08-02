
import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from utils import DocumentProcessor
import ui_utils as ui

# Load environment variables
load_dotenv()

def main():
    """Main function to run the Streamlit application."""
    # Initialize the UI
    ui.display_header()
    ui.display_welcome_message()

    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'document_processed' not in st.session_state:
        st.session_state.document_processed = False
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = None
    if 'qa_chain' not in st.session_state:
        st.session_state.qa_chain = None
    if 'document_details' not in st.session_state:
        st.session_state.document_details = {}

    # Sidebar for user inputs
    uploaded_file, openai_api_key, process_btn = ui.display_sidebar()

    if process_btn:
        if not uploaded_file:
            st.sidebar.warning("Oops! I need a document to analyze. Could you upload one first?")
        elif not openai_api_key:
            st.sidebar.warning("I need your OpenAI API key to work my magic. Mind adding it above?")
        else:
            with st.spinner("Processing your document... This might take a moment."):
                try:
                    # Temporarily save the uploaded file
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    # Initialize the document processor
                    st.session_state.doc_processor = DocumentProcessor(openai_api_key)

                    # Process the document
                    docs, _ = st.session_state.doc_processor.load_document(tmp_path)
                    splits, split_info = st.session_state.doc_processor.split_documents(docs)
                    vectorstore, _ = st.session_state.doc_processor.create_vectorstore(splits)
                    st.session_state.qa_chain = st.session_state.doc_processor.create_qa_chain(vectorstore)

                    # Store document details for the dashboard
                    st.session_state.document_details = {
                        'file_name': uploaded_file.name,
                        'chunk_count': split_info['output_chunks'],
                        'processing_time': st.session_state.doc_processor.get_performance_summary().get('total_processing_time', 0)
                    }

                    st.session_state.document_processed = True
                    st.sidebar.success("✅ Document processed successfully!")
                    os.unlink(tmp_path)  # Clean up the temporary file

                except Exception as e:
                    st.sidebar.error(f"Error processing document: {e}")

    # Main content area
    if st.session_state.document_processed:
        col1, col2 = st.columns([2, 1])
        with col1:
            question = ui.display_chat_interface(st.session_state.chat_history)
            if question:
                st.session_state.chat_history.append(question)
                with st.spinner("Searching for insights..."):
                    result, _ = st.session_state.doc_processor.process_query(
                        st.session_state.qa_chain,
                        question,
                        st.session_state.chat_history[:-1] # Pass previous chat history
                    )
                    st.session_state.chat_history.append(result['answer'])
                    st.experimental_rerun() # Refresh to show the new answer

        with col2:
            ui.display_insights_dashboard(
                st.session_state.doc_processor.performance_logs,
                st.session_state.document_details
            )
    else:
        ui.display_initial_capabilities()

    # Footer
    ui.display_footer()

if __name__ == '__main__':
    main()
