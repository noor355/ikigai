"""
NLP Processing Module for Ikigai Career Recommendations
Handles sentiment analysis, keyword extraction, NER, semantic similarity, and summarization
"""

from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import torch
from typing import List, Dict, Tuple
import numpy as np


class NLPProcessor:
    """Main NLP processor using HuggingFace Transformers"""
    
    def __init__(self):
        """Initialize NLP models - using smaller/faster models for production"""
        # Sentiment analysis
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        
        # Named Entity Recognition
        self.ner_pipeline = pipeline(
            "ner",
            model="dslim/bert-base-uncased-ner",
            aggregation_strategy="simple"
        )
        
        # Summarization (for longer texts)
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )
        
        # Semantic embeddings for similarity
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Zero-shot classification for keyword extraction
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
    
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
        Calculate semantic similarity between two texts (0-1)
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            float: Similarity score
        """
        if not text1 or not text2:
            return 0.0
        
        try:
            embeddings1 = self.embedding_model.encode(text1, convert_to_tensor=True)
            embeddings2 = self.embedding_model.encode(text2, convert_to_tensor=True)
            
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
        
        # Truncate very long texts (summarizer has limits)
        text = text[:1024]
        
        try:
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]["summary_text"]
        except Exception as e:
            print(f"Error in summarization: {e}")
            return text
    
    # ============ INTEGRATED PROCESSING ============
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
