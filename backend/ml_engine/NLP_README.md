# NLP Integration for Ikigai Career Guidance System

## Overview

The Ikigai system now includes comprehensive Natural Language Processing (NLP) capabilities using HuggingFace Transformers. This allows for deeper understanding of user preferences, skills, and career goals from their text inputs.

## NLP Features

### 1. **Sentiment Analysis**
Analyzes the emotional tone of user inputs to better understand passion levels.
- Model: `distilbert-base-uncased-finetuned-sst-2-english`
- Use Case: Score passion from daily entry sentiments

```python
nlp = get_nlp_processor()
sentiment = nlp.analyze_sentiment("I really enjoyed solving this challenging problem today!")
# Returns: {"label": "POSITIVE", "score": 0.99, "sentiment_type": "positive"}
```

### 2. **Keyword Extraction**
Extracts important keywords from text to identify user interests and themes.
- Method: Stop-word filtering + frequency analysis
- Returns: Top 10 unique meaningful words

```python
keywords = nlp.extract_keywords("I love Python, Django, and building REST APIs")
# Returns: ['python', 'django', 'building', 'rest', 'apis', ...]
```

### 3. **Named Entity Recognition (NER)**
Identifies specific entities like skills, technologies, tools, and organizations.
- Model: `dslim/bert-base-uncased-ner`
- Detects: Technologies, Skills, People, Organizations

```python
entities = nlp.extract_skills_and_entities("I worked with TensorFlow and AWS at Google")
# Returns: {
#     "skills": ["tensorflow", "aws"],
#     "organizations": ["Google"],
#     "technologies": ["tensorflow", "aws"]
# }
```

### 4. **Semantic Similarity**
Measures how similar two texts are conceptually using embeddings.
- Model: `all-MiniLM-L6-v2` (lightweight, fast)
- Returns: Similarity score 0-1

```python
user_profile = "I'm interested in AI and machine learning"
job_desc = "Build intelligent systems using deep learning"
similarity = nlp.calculate_similarity(user_profile, job_desc)
# Returns: 0.87 (high semantic similarity)
```

### 5. **Text Summarization**
Condenses long texts into concise summaries.
- Model: `facebook/bart-large-cnn`
- Use Case: Summarize daily entries or job descriptions

```python
long_text = "Today I worked on... [long entry]"
summary = nlp.summarize_text(long_text, max_length=150)
```

## Installation

The required packages have been added to `requirements.txt`:

```bash
pip install -r requirements.txt
```

Main dependencies:
- `transformers>=4.35.0` - HuggingFace models
- `torch>=2.0.0` - Deep learning backbone
- `sentence-transformers>=2.2.0` - Semantic embeddings

## Integration Points

### In Recommendation Engine

The `IkigaiRecommendationEngine` now uses NLP for:

1. **Enhanced Passion Scoring**: Analyzes daily entry content sentiment instead of just mood tags
2. **Better Skill Detection**: Extracts skills mentioned in text, not just predefined lists
3. **NLP-Enhanced Career Matching**: Combines ML scoring with semantic similarity

```python
engine = IkigaiRecommendationEngine()

# Calculate match using both ML and NLP
user_profile = {"skills": ["Python"], "experience": 3}
user_bio = "I love building AI solutions"
career = {"title": "ML Engineer", "description": "..."}

match_result = engine.calculate_nlp_enhanced_career_match(
    user_profile, 
    user_bio, 
    career
)
# Returns traditional scores + NLP insights
```

## Usage Examples

### Example 1: Complete User Analysis

```python
from ml_engine.nlp_processor import get_nlp_processor

nlp = get_nlp_processor()

user_text = "I am passionate about Python and AI. Recently completed a TensorFlow course."
analysis = nlp.process_user_input(user_text)

print(analysis)
# {
#     "sentiment": {...},
#     "keywords": ["python", "ai", "tensorflow", ...],
#     "entities": {"skills": ["tensorflow"], "technologies": ["python"]},
#     "summary": "Passionate about Python and AI with recent TensorFlow training",
#     "raw_text_length": 12
# }
```

### Example 2: Career Matching

```python
engine = IkigaiRecommendationEngine()

user_profile = {
    "skills": ["Python", "SQL"],
    "education": "Bachelor",
    "experience": 3
}
user_bio = "Data-driven problem solver interested in ML and analytics"

careers = [
    {"id": 1, "title": "Data Scientist", "description": "Use ML..."},
    {"id": 2, "title": "Backend Developer", "description": "Build APIs..."},
]

for career in careers:
    match = engine.calculate_nlp_enhanced_career_match(user_profile, user_bio, career)
    print(f"{career['title']}: {match['overall_score']:.1f}%")
```

### Example 3: Daily Entry Analysis

```python
from ml_engine.nlp_integration_examples import analyze_daily_entries_nlp

daily_entries = [
    {"date": "2024-01-01", "content": "Excited to learn PyTorch today!"},
    {"date": "2024-01-02", "content": "Finished TensorFlow tutorial, feeling proud"},
]

insights = analyze_daily_entries_nlp(daily_entries)
print(f"Sentiment: {insights['sentiment_distribution']['positive_ratio']:.1%}")
print(f"Skills detected: {insights['detected_skills']}")
```

## Performance Considerations

### Model Downloads
Models are automatically downloaded on first use:
- `distilbert-base-uncased-finetuned-sst-2-english` (~250MB)
- `dslim/bert-base-uncased-ner` (~500MB)
- `facebook/bart-large-cnn` (~1.2GB)
- `all-MiniLM-L6-v2` (~100MB)

Total: ~2GB

### Optimization
- Models are cached locally after first download
- Singleton pattern ensures models loaded only once
- Lightweight models chosen for production use
- Text truncation prevents long processing times

### API Response Times
- Sentiment: ~100-200ms
- Keyword extraction: ~50ms
- NER: ~200-300ms
- Similarity: ~100ms
- Summarization: ~1-2s (slower, use judiciously)

## API Integration Examples

### Route 1: Enhanced Career Recommendations

```python
from fastapi import APIRouter, HTTPException
from ml_engine.recommendation_engine import IkigaiRecommendationEngine

router = APIRouter()

@router.post("/api/v1/recommendations/enhanced")
async def get_enhanced_recommendations(
    user_id: int,
    bio: str,
    career_filters: dict = None
):
    # Fetch user profile from DB
    user_profile = await get_user_profile(user_id)
    
    # Get available careers
    careers = await get_careers_from_db(filters=career_filters)
    
    engine = IkigaiRecommendationEngine()
    
    recommendations = []
    for career in careers:
        match = engine.calculate_nlp_enhanced_career_match(user_profile, bio, career)
        recommendations.append({
            "career_id": career["id"],
            "title": career["title"],
            "match_score": match["overall_score"],
            "keywords": match.get("matching_keywords", [])
        })
    
    return sorted(recommendations, key=lambda x: x["match_score"], reverse=True)
```

### Route 2: Daily Entry Analysis

```python
@router.post("/api/v1/entries/analyze")
async def analyze_entry(
    user_id: int,
    content: str
):
    nlp = get_nlp_processor()
    
    analysis = nlp.process_user_input(content)
    
    # Store insights in DB
    await save_entry_insights(user_id, analysis)
    
    return analysis
```

## Error Handling

The NLP processor gracefully handles errors:

```python
engine = IkigaiRecommendationEngine()

# If NLP initialization fails, engine.nlp_enabled = False
# Falls back to traditional ML scoring

if engine.nlp_enabled:
    # Use NLP features
    match = engine.calculate_nlp_enhanced_career_match(...)
else:
    # Use traditional scoring
    match = engine.calculate_career_match(...)
```

## Future Enhancements

1. **Custom Fine-tuning**: Fine-tune models on career-specific vocabulary
2. **Multi-language Support**: Add non-English language support
3. **Real-time Streaming**: Process daily entries as users type
4. **Caching**: Cache embeddings for frequently analyzed careers
5. **Ensemble Methods**: Combine multiple NLP models for better accuracy

## Troubleshooting

### Models not downloading
- Check internet connection
- Clear cache: `rm -rf ~/.cache/huggingface`
- Increase timeout: Set `HF_HUB_TIMEOUT=60` environment variable

### Out of memory
- Use CPU only: Set `CUDA_VISIBLE_DEVICES=""`
- Use smaller models (already done with `all-MiniLM-L6-v2`)

### Slow performance
- Pre-load models at startup
- Use batch processing for multiple texts
- Cache embeddings in database

## References

- [HuggingFace Transformers](https://huggingface.co/transformers/)
- [Sentence Transformers](https://www.sbert.net/)
- [BART Summarization](https://huggingface.co/facebook/bart-large-cnn)
- [BERT NER](https://huggingface.co/dslim/bert-base-uncased-ner)
