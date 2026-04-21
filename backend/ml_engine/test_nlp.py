
from ml_engine.nlp_processor import NLPProcessor
import time

def test_nlp():
    print("Starting NLP Processor initialization...")
    start_time = time.time()
    try:
        nlp = NLPProcessor()
        print(f"Models loaded successfully in {time.time() - start_time:.2f} seconds")
        
        test_text = "I am very excited about artificial intelligence and space exploration!"
        print(f"Testing sentiment analysis with: {test_text}")
        sentiment = nlp.analyze_sentiment(test_text)
        print(f"Sentiment result: {sentiment}")
        
    except Exception as e:
        print(f"Error during NLP test: {e}")

if __name__ == "__main__":
    test_nlp()
