import os
import json
import time
import argparse
import pandas as pd
from dotenv import load_dotenv
from utils import DocumentProcessor

# Load environment variables
load_dotenv()

def evaluate_system(document_path, questions_path, output_path=None):
    """Evaluate the RAG system on a set of test questions."""
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set it in .env file or as an environment variable.")
    
    # Load test questions
    with open(questions_path, 'r') as f:
        test_data = json.load(f)
    
    # Initialize document processor
    processor = DocumentProcessor(api_key)
    
    # Process document
    print(f"Loading document: {document_path}")
    documents, _ = processor.load_document(document_path)
    
    print(f"Splitting document into chunks")
    splits, _ = processor.split_documents(documents)
    
    print(f"Creating vector store")
    vectorstore, _ = processor.create_vectorstore(splits)
    
    print(f"Creating QA chain")
    qa_chain = processor.create_qa_chain(vectorstore)
    
    # Evaluate each question
    results = []
    chat_history = []
    
    for i, item in enumerate(test_data):
        question = item["question"]
        expected_answer = item.get("expected_answer", None)  # Optional ground truth
        
        print(f"\nProcessing question {i+1}/{len(test_data)}: {question}")
        
        # Process query
        start_time = time.time()
        result, perf_data = processor.process_query(qa_chain, question, chat_history)
        end_time = time.time()
        
        # Update chat history for context
        chat_history.append((question, result["answer"]))
        
        # Store result
        eval_result = {
            "question": question,
            "answer": result["answer"],
            "expected_answer": expected_answer,
            "processing_time": end_time - start_time,
            "source_documents": [doc.page_content[:100] + "..." for doc in result["source_documents"]]
        }
        
        results.append(eval_result)
        
        print(f"Answer: {result['answer'][:100]}...")
        print(f"Processing time: {end_time - start_time:.2f} seconds")
    
    # Calculate overall statistics
    avg_time = sum(r["processing_time"] for r in results) / len(results)
    print(f"\nEvaluation complete. Average processing time: {avg_time:.2f} seconds")
    
    # Save results if output path is provided
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")
    
    return results

def create_sample_questions():
    """Create a sample questions file for testing."""
    sample_questions = [
        {
            "question": "What was the company's total revenue for the last fiscal year?",
            "expected_answer": None  # This would be filled with ground truth if available
        },
        {
            "question": "What are the main risk factors mentioned in the report?",
            "expected_answer": None
        },
        {
            "question": "How has the gross margin changed compared to the previous year?",
            "expected_answer": None
        },
        {
            "question": "What is the company's strategy for the next year?",
            "expected_answer": None
        },
        {
            "question": "Who are the key executives mentioned in the report?",
            "expected_answer": None
        }
    ]
    
    with open('sample_questions.json', 'w') as f:
        json.dump(sample_questions, f, indent=2)
    
    print("Sample questions file created: sample_questions.json")

def main():
    parser = argparse.ArgumentParser(description="Evaluate the RAG system on financial documents")
    parser.add_argument("--document", "-d", type=str, help="Path to the document file (PDF or DOCX)")
    parser.add_argument("--questions", "-q", type=str, help="Path to the questions JSON file")
    parser.add_argument("--output", "-o", type=str, help="Path to save evaluation results")
    parser.add_argument("--create-sample", "-s", action="store_true", help="Create a sample questions file")
    
    args = parser.parse_args()
    
    if args.create_sample:
        create_sample_questions()
        return
    
    if not args.document or not args.questions:
        parser.print_help()
        return
    
    evaluate_system(args.document, args.questions, args.output)

if __name__ == "__main__":
    main()