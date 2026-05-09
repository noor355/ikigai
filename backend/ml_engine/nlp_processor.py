"""
NLP Processing Module for Ikigai Career Recommendations
Handles sentiment analysis, keyword extraction, NER, semantic similarity, and summarization
"""

from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import torch
from typing import List, Dict, Tuple, Any
import numpy as np
from google import genai
from google.genai import types
import os
from config import settings


class NLPProcessor:
    """Main NLP processor using HuggingFace Transformers with Gemini for core chat"""
    
    def __init__(self):
        """Initialize NLP models - EAGER LOADING for production/demo"""
        # Type hints for Pylance
        self.sentiment_pipeline: Any
        self.embedding_model: SentenceTransformer
        self.ner_pipeline: Any
        self.summarizer: Any
        self.classifier: Any
        self.generator: Any
        self.gemini_client: Any = None
        self.cache: Dict[str, Any] = {}

        # Initialize Gemini if API key is present
        api_key = settings.GOOGLE_API_KEY
        if api_key:
            print(f"[NLP] Initializing Gemini API with key: {api_key[:10]}...")
            try:
                # Set GEMINI_API_KEY to match the docs for automatic pickup
                os.environ["GEMINI_API_KEY"] = api_key
                # The client gets the API key from the environment variable `GEMINI_API_KEY`.
                self.gemini_client = genai.Client()
                print("[NLP] Gemini API (gemini-2.0-flash) initialized successfully")
            except Exception as e:
                print(f"[NLP] Gemini initialization failed: {e}")

        print("[NLP] Loading sentiment analysis model...")
        try:
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",  # type: ignore
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1
            )
            print("[NLP] Sentiment model loaded")
        except Exception as e:
            print(f"[NLP] Sentiment model failed: {e}")
            self.sentiment_pipeline = None
        
        print("[NLP] Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        print("[NLP] Embedding model loaded")
        
        # Named Entity Recognition
        try:
            print("[NLP] Loading NER model...")
            self.ner_pipeline = pipeline(
                "ner",  # type: ignore
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                aggregation_strategy="simple",
                device=-1
            )
            print("[NLP] NER model loaded")
        except Exception as e:
            print(f"[NLP] NER Model failed to load: {e}")
            self.ner_pipeline = None
        
        # Zero-shot classification
        try:
            print("[NLP] Loading zero-shot classifier...")
            self.classifier = pipeline(
                "zero-shot-classification",  # type: ignore
                model="facebook/bart-large-mnli",
                device=-1
            )
            print("[NLP] Zero-shot classifier loaded")
        except Exception as e:
            print(f"[NLP] Classifier failed to load: {e}")
            self.classifier = None
        
        # Text Generation for Chatbot - Using DialoGPT (Pre-trained for conversation)
        try:
            print("[NLP] Loading DialoGPT-medium for better chatting...")
            self.generator = pipeline(
                "text-generation",  # type: ignore
                model="microsoft/DialoGPT-medium",
                device=-1,  # Force CPU for stability
                torch_dtype=torch.float32  # Ensure float32 to prevent dtype mismatches
            )
            print("[NLP] DialoGPT loaded successfully")
        except Exception as e:
            print(f"[NLP] DialoGPT failed: {e}. Falling back to GPT2...")
            try:
                self.generator = pipeline("text-generation", model="gpt2")
            except:
                self.generator = None
        
        # Load Summarizer specifically for long journal entries
        try:
            print("[NLP] Loading summarization model (DistilBART)...")
            self.summarizer = pipeline(
                "summarization",  # type: ignore
                model="sshleifer/distilbart-cnn-12-6",
                device=-1
            )
            print("[NLP] Summarization model loaded")
        except Exception as e:
            print(f"[NLP] Summarization failed to load: {e}")
            self.summarizer = None
        
        print("[NLP] All models loaded successfully!")
    
    # ============ CACHING LOGIC ============
    def get_cached_embedding(self, text: str):
        if text in self.cache:
            return self.cache[text]
        embedding = self.embedding_model.encode(text, convert_to_tensor=True)
        # Limit cache size to 1000 items
        if len(self.cache) < 1000:
            self.cache[text] = embedding
        return embedding

    # ============ TEXT GENERATION ============
    def generate_coach_response(self, user_message: str, context: str = "") -> str:
        """
        Generate a coaching response using Gemini AI or fallback NLP models.
        """
        # 1. Try Gemini API first (much higher quality)
        if self.gemini_client:
            try:
                # Expert Career Coach Persona with Ikigai Focus
                system_prompt = (
                    "You are the 'Ikigai Expert Coach', a world-class career strategist and empathetic life mentor. "
                    "Your goal is to help the user find their Ikigai (the intersection of what they love, what they are good at, "
                    "what the world needs, and what they can be paid for).\n\n"
                    "GUIDELINES:\n"
                    "- PERSONALIZATION: Use the provided context about the user's profile and activities to make responses specific. "
                    "If the user is struggling (e.g., 'staring at walls'), be deeply empathetic but gently transition to discovery.\n"
                    "- EXPERT INSIGHT: Don't just agree. Offer professional career perspectives. If they mention a hobby, suggest how it "
                    "could be a skill or a profession.\n"
                    "- CONVERSATION: Keep it natural. Ask ONE thoughtful follow-up question to keep the discovery process moving.\n"
                    "- BREVITY: Keep responses under 3-4 sentences unless explaining a complex concept.\n"
                    "- NEVER repeat the user's input back to them verbatim. Avoid 'I understand you said...'\n"
                    "- CAREER & SALARY: If the user asks about combinations, career paths, or roles, ALWAYS provide 2-3 specific profession "
                    "titles, explaining WHY they fit, and suggest estimated yearly salary ranges (e.g., '$80k - $120k') based on current global/local market trends.\n"
                )
                
                full_prompt = f"{system_prompt}\n\nUSER CONTEXT: {context}\n\nUSER MESSAGE: {user_message}\n\nEXPERT COACH RESPONSE:"
                
                # Using the new SDK 1.0.0 client.models.generate_content method
                # Using 2.5-flash which is the stable high-quota entry
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=full_prompt
                )
                
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[NLP] Gemini generation failed, falling back: {e}")

        # 2. Local Fallback logic starts here
        if not self.generator:
            return "I'm currently in rule-based mode as my brain is still loading. How can I help?"

        user_message_lower = user_message.lower()
        
        # Enhanced keyword responses for better domain knowledge
        if "doctor" in user_message_lower:
            return "Medicine is a noble path! It strongly hits the 'What the world needs' part of Ikigai. What draws you to being a doctor? Is it the science, the helping others, or the challenge?"
        
        if "engineer" in user_message_lower:
            return "Engineering is all about problem-solving. Whether it's software or structural, it requires a unique mindset. Do you enjoy the process of building systems from scratch?"

        if "creative" in user_message_lower or "art" in user_message_lower:
            return "Creativity is a powerful engine for Ikigai. How do you feel when you're in 'the flow' of creating something new? Could you see yourself doing that every day?"

        # Fallback to Pre-trained Chatting System (DialoGPT)
        try:
            # We want to ensure we're using float32 to avoid dtype mismatches (Half vs Float)
            # This is common on CPUs when models are loaded in Half precision by default
            responses = self.generator(
                user_message,
                max_new_tokens=50,
                num_return_sequences=1,
                no_repeat_ngram_size=3,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=50256,
                clean_up_tokenization_spaces=True
            )
            reply = responses[0]['generated_text'].replace(user_message, "").strip()
            
            if not reply or len(reply) < 5:
                return f"As your Ikigai coach, I want to dig deeper into '{user_message}'. How does this specific interest make you feel when you engage with it?"
                
            return reply
        except Exception as e:
            print(f"Error in generation: {e}")
            return f"That sounds like a unique part of your journey. How has '{user_message}' shaped your view on what you want to achieve financially?"

    # ============ SENTIMENT ANALYSIS ============
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text (positive/negative)
        
        Args:
            text: Text to analyze
            
        Returns:
            dict: Sentiment label and score
        """
        if not text or len(text.strip()) == 0:
            return {"label": "NEUTRAL", "score": 0.5}
        
        # Truncate long texts
        text = text[:512]
        
        try:
            result = self.sentiment_pipeline(text)[0]
            return {
                "label": result["label"],
                "score": result["score"],
                "sentiment_type": "positive" if result["label"] == "POSITIVE" else "negative"
            }
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {"label": "NEUTRAL", "score": 0.5}
    
    def batch_sentiment_analysis(self, texts: List[str]) -> List[Dict]:
        """Analyze sentiment for multiple texts"""
        return [self.analyze_sentiment(text) for text in texts]
    
    # ============ KEYWORD EXTRACTION ============
    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """
        Extract keywords using zero-shot classification on ngrams
        
        Args:
            text: Text to extract keywords from
            top_k: Number of keywords to return
            
        Returns:
            list: Top keywords found in text
        """
        if not text or len(text.strip()) == 0:
            return []
        
        # Simple keyword extraction by finding important words
        words = text.lower().split()
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
        
        filtered_words = [w.strip('.,!?;:') for w in words if w.lower() not in stop_words and len(w) > 3]
        
        # Return top unique words
        unique_keywords = list(dict.fromkeys(filtered_words))
        return unique_keywords[:top_k]
    
    # ============ NAMED ENTITY RECOGNITION ============
    def extract_skills_and_entities(self, text: str) -> Dict[str, List]:
        """
        Extract named entities including skills, tools, technologies
        
        Args:
            text: Text to analyze
            
        Returns:
            dict: Categorized entities
        """
        if not text or len(text.strip()) == 0:
            return {"entities": [], "skills": [], "technologies": []}
        
        text = text[:512]  # Truncate for processing
        
        try:
            entities = self.ner_pipeline(text)
            
            # Organize entities by type
            result = {
                "entities": entities,
                "skills": [],
                "technologies": [],
                "organizations": [],
                "people": []
            }
            
            for entity in entities:
                label = entity.get("entity_group", "")
                value = entity.get("word", "").strip()
                
                if label == "PER":
                    result["people"].append(value)
                elif label == "ORG":
                    result["organizations"].append(value)
                elif label == "MISC":
                    # MISC can contain technologies/skills
                    result["technologies"].append(value)
            
            # Additional skill detection based on keywords
            tech_keywords = ['python', 'java', 'javascript', 'react', 'angular', 'sql', 'mongodb',
                           'aws', 'docker', 'kubernetes', 'machine', 'learning', 'ai', 'ml', 
                           'data', 'science', 'deep', 'neural', 'nlp', 'cv']
            
            keywords = self.extract_keywords(text)
            result["skills"] = [kw for kw in keywords if any(tk in kw.lower() for tk in tech_keywords)]
            
            return result
        except Exception as e:
            print(f"Error in NER: {e}")
            return {"entities": [], "skills": [], "technologies": []}
    
    # ============ SEMANTIC SIMILARITY ============
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts (0-1) with caching
        """
        if not text1 or not text2:
            return 0.0
        
        try:
            embeddings1 = self.get_cached_embedding(text1)
            embeddings2 = self.get_cached_embedding(text2)
            
            similarity = util.pytorch_cos_sim(embeddings1, embeddings2)
            return float(similarity[0][0])
        except Exception as e:
            print(f"Error in similarity calculation: {e}")
            return 0.0
    
    def find_most_similar(self, query: str, documents: List[str]) -> List[Tuple[str, float]]:
        """
        Find most similar documents to query text
        
        Args:
            query: Query text
            documents: List of documents to compare
            
        Returns:
            list: Sorted list of (document, similarity_score) tuples
        """
        if not query or not documents:
            return []
        
        try:
            query_embedding = self.embedding_model.encode(query, convert_to_tensor=True)
            doc_embeddings = self.embedding_model.encode(documents, convert_to_tensor=True)
            
            similarities = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0]
            
            ranked = [(documents[i], float(similarities[i])) for i in range(len(documents))]
            ranked.sort(key=lambda x: x[1], reverse=True)
            
            return ranked
        except Exception as e:
            print(f"Error in similarity ranking: {e}")
            return []
    
    # ============ TEXT SUMMARIZATION ============
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """
        Summarize long text using BART
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            str: Summarized text
        """
        if not text or len(text.strip()) < 100:
            return text  # Too short to summarize
        
        # --- NEW: Use Gemini if available for much better summaries ---
        if self.gemini_client:
            try:
                prompt = (
                    f"Summarize the following text concisely (under {max_length} words). "
                    "Focus on identifying the core interests or skills mentioned.\n\n"
                    f"TEXT: {text}"
                )
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[NLP] Gemini summarization failed: {e}")

        # Fallback if summarizer model is missing
        if self.summarizer is None:
            # Simple extractive summary: first 2 sentences
            sentences = [s.strip() + "." for s in text.split(".") if len(s.strip()) > 5]
            if len(sentences) > 2:
                return " ".join(sentences[:2])
            return text
        
        # Truncate very long texts (summarizer has limits)
        text = text[:1024]
        
        try:
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]["summary_text"]
        except Exception as e:
            print(f"Error in summarization: {e}")
            return text
    
    # ============ INTEGRATED PROCESSING ============
    def analyze_career_pillars(self, chat_history: List[str]) -> Dict[str, List[str]]:
        """
        Use Gemini to perform Semantic Analysis of the entire chat history.
        Identifies 3 core Ikigai pillars as 'Expert Overrides'.
        """
        if not self.gemini_client:
            return {"passions": [], "skills": [], "values": []}

        try:
            history_text = "\n".join(chat_history[-15:]) # Analyze last 15 exchanges
            prompt = (
                "Task: Analyze the following career coaching chat history and identify exactly 3 core Ikigai pillars "
                "representing the user's deepest passions, strongest skills, and non-negotiable values.\n\n"
                "CHAT HISTORY:\n"
                f"{history_text}\n\n"
                "Output ONLY a valid JSON object with the following structure:\n"
                "{\n"
                "  \"passions\": [\"keyword1\", \"keyword2\", \"keyword3\"],\n"
                "  \"skills\": [\"keyword1\", \"keyword2\", \"keyword3\"],\n"
                "  \"values\": [\"keyword1\", \"keyword2\", \"keyword3\"]\n"
                "}"
            )

            # Using the new SDK 1.0.0 client.models.generate_content method
            response = self.gemini_client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )

            if response and response.text:
                import json
                # Strip potential markdown code blocks if Gemini returns them
                content = response.text.strip()
                if content.startswith("```json"):
                    content = content[7:-3]
                elif content.startswith("```"):
                    content = content[3:-3]
                
                return json.loads(content.strip())
        except Exception as e:
            print(f"[NLP] Pillar Analysis failed: {e}")
            
        return {"passions": [], "skills": [], "values": []}

    def process_user_input(self, text: str) -> Dict:
        """
        Complete processing of user input text
        
        Args:
            text: User input text to process
            
        Returns:
            dict: Comprehensive analysis results
        """
        if not text:
            return {
                "sentiment": None,
                "keywords": [],
                "entities": {},
                "summary": ""
            }
        
        return {
            "sentiment": self.analyze_sentiment(text),
            "keywords": self.extract_keywords(text),
            "entities": self.extract_skills_and_entities(text),
            "summary": self.summarize_text(text) if len(text) > 100 else text,
            "raw_text_length": len(text.split())
        }
    
    def profile_similarity_with_career(self, user_profile: str, career_description: str) -> Dict:
        """
        Calculate comprehensive similarity between user profile and career
        
        Args:
            user_profile: User's profile/bio text
            career_description: Career description
            
        Returns:
            dict: Detailed similarity analysis
        """
        base_similarity = self.calculate_similarity(user_profile, career_description)
        
        # Extract keywords from both
        user_keywords = self.extract_keywords(user_profile)
        career_keywords = self.extract_keywords(career_description)
        
        # Calculate keyword overlap
        user_set = set(user_keywords)
        career_set = set(career_keywords)
        
        overlap = user_set.intersection(career_set)
        overlap_ratio = len(overlap) / max(len(user_set.union(career_set)), 1)
        
        # Extract entities/skills
        user_skills = self.extract_skills_and_entities(user_profile)
        career_skills = self.extract_skills_and_entities(career_description)
        
        return {
            "semantic_similarity": base_similarity,
            "keyword_overlap": overlap_ratio,
            "overlapping_keywords": list(overlap),
            "user_keywords": user_keywords,
            "career_keywords": career_keywords,
            "user_skills": user_skills.get("skills", []),
            "career_skills": career_skills.get("skills", []),
            "combined_score": (base_similarity + overlap_ratio) / 2
        }


# Singleton instance for efficiency
_nlp_processor = None

def get_nlp_processor() -> NLPProcessor:
    """Get or create the NLP processor singleton"""
    global _nlp_processor
    if _nlp_processor is None:
        _nlp_processor = NLPProcessor()
    return _nlp_processor
