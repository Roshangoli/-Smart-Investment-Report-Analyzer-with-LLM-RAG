# Smart Investment Report Analyzer

A powerful tool that uses AI to analyze financial reports and answer your questions in natural language. This application leverages Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to provide accurate, document-grounded answers about financial reports like annual 10-Ks.

## Features

- **Document Processing**: Upload PDF or DOCX financial reports for analysis
- **Natural Language Q&A**: Ask questions in plain English about the report
- **Context-Aware Responses**: Get answers grounded in the actual content of your documents
- **Performance Tracking**: Monitor response times and system performance
- **User-Friendly Interface**: Clean, intuitive Streamlit interface for easy interaction

## How It Works

The system uses a Retrieval-Augmented Generation (RAG) approach:

1. **Document Processing**:
   - Documents are split into manageable chunks
   - Text chunks are converted to vector embeddings using OpenAI's embedding model
   - Embeddings are stored in a ChromaDB vector database for efficient retrieval

2. **Question Answering**:
   - When you ask a question, the system finds the most relevant document chunks
   - These chunks are sent to the LLM along with your question
   - The LLM generates an answer based on the retrieved context

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone this repository or download the files

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your OpenAI API key (optional):

```
OPENAI_API_KEY=your_api_key_here
```

### Running the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your default web browser.

## Usage

1. **Upload a Document**:
   - Use the sidebar to upload a financial report (PDF or DOCX)
   - Enter your OpenAI API key if not provided in the .env file
   - Click "Process Document"

2. **Ask Questions**:
   - Type your question in the text input field
   - The system will retrieve relevant information and provide an answer
   - Continue the conversation with follow-up questions

3. **View Insights**:
   - Check the performance metrics in the sidebar
   - See document statistics and processing information

## Example Questions

- "What was the company's revenue in the last fiscal year?"
- "What are the main risk factors mentioned in the report?"
- "How has the gross margin changed compared to the previous year?"
- "Summarize the company's future outlook."
- "What were the major expenses in the last quarter?"

## Performance Considerations

- Large documents may take longer to process initially
- The system is optimized for financial reports and related queries
- Performance metrics are displayed to help track system efficiency

## Limitations

- The system can only answer questions based on information present in the uploaded document
- Very large documents may be truncated due to token limitations
- The quality of answers depends on the clarity and structure of the original document

## Future Improvements

- Support for more document formats
- Enhanced visualization of financial data
- Comparative analysis between multiple reports
- Custom fine-tuning for specific financial document types

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [LangChain](https://github.com/hwchase17/langchain)
- Vector database powered by [ChromaDB](https://github.com/chroma-core/chroma)
- LLM capabilities provided by [OpenAI](https://openai.com/)
- Interface created with [Streamlit](https://streamlit.io/)