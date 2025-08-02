
import os
import sys
import time
from dotenv import load_dotenv
from utils import DocumentProcessor

load_dotenv()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Oops! I couldn't find your OpenAI API key.")
        print(" Quick fix: Add it to your .env file or set it as an environment variable.")
        return 1
    
    if len(sys.argv) < 2:
        print("\n How to use this tool:")
        print("   python example_usage.py <path_to_your_document>")
        print("\n For example:")
        print("   python example_usage.py sample_financial_report.pdf")
        return 1
    
    document_path = sys.argv[1]
    if not os.path.exists(document_path):
        print(f"\n Hmm, I couldn't find '{document_path}'")
        print("  Please check the file path and try again.")
        return 1
    
    print(f"\n🔧 Setting things up for you...")
    processor = DocumentProcessor(api_key)
    
    print(f"\nOpening your document: {os.path.basename(document_path)}")
    documents, _ = processor.load_document(document_path)
    print(f" Successfully loaded {len(documents)} pages/sections")
    
    print(f"\n  Breaking down the document into digestible pieces...")
    splits, split_data = processor.split_documents(documents)
    print(f" Created {len(splits)} manageable chunks of information")
    
    print(f"\n Building a smart knowledge base from your document...")
    start_time = time.time()
    vectorstore, _ = processor.create_vectorstore(splits)
    print(f" Knowledge base ready in {time.time() - start_time:.2f} seconds")
    
    print(f"\n  Connecting the AI assistant to your document...")
    qa_chain = processor.create_qa_chain(vectorstore)
    
    chat_history = []
    
    print("\n All set! Your document is ready for exploration ✨")
    print("\n Ask me anything about your financial report")
    print("   (Type 'exit' when you're done)")
    
    while True:
        question = input("\n What would you like to know? ")
        if question.lower() in ['exit', 'quit', 'q']:
            break
        
        print(" Searching through your document for the best answer...")
        start_time = time.time()
        result, _ = processor.process_query(qa_chain, question, chat_history)
        
        search_time = time.time() - start_time
        print(f"\n Here's what I found (in {search_time:.2f} seconds):")
        print(f"\n{'-'*50}")
        print(f"{result['answer']}")
        print(f"{'-'*50}")
        
        chat_history.append((question, result["answer"]))
        
        if result["source_documents"]:
            print(f"\n Based on these sections of your document:")
            for i, doc in enumerate(result["source_documents"][:3]):
                print(f"  {i+1}. \"{doc.page_content[:100]}...\"")
    
    print("\n⚡ Performance Overview:")
    summary = processor.get_performance_summary()
    for op, avg_time in summary.get("average_times", {}).items():
        op_name = op.replace("_", " ").title()
        print(f"  • {op_name}: {avg_time:.2f} seconds average")
    
    print("\n Thanks for using the Smart Investment Report Analyzer!")
    print("   Have a great day analyzing your financial data.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
