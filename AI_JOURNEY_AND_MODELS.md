# The Journey of Ikigai AI: Model Training & Project Technical Review

## 1. The Journey & Vision
The "Ikigai AI" project was born from the need to help individuals find their "Reason for Being" in a rapidly changing job market. We moved beyond simple keyword matching to build a multi-layered AI system that understands **Passions**, **Abilities**, **Values**, and **Market Realities**.

The journey began with researching the Ikigai framework and identifying how to represent "What you love" vs. "What you are good at" mathematically. We then integrated modern LLM capabilities (Gemini) with traditional NLP (BERT/TF-IDF) to create a system that is both analytical and empathetic.

## 2. Model Architecture & Training
We employ a **hybrid model architecture** consisting of both specialized local models and large-scale cloud models.

### Models Used:
*   **Gemini 1.5 Flash (Google):** Our primary "brain" for complex reasoning, personalized career coaching, and generating deep insights from journal entries.
*   **BERT (Devlin et al.):** Used for **Named Entity Recognition (NER)** to extract specific skills and industries from user text.
*   **DistilBERT:** A lightweight BERT variant trained on the **SST-2 dataset** for high-speed **Sentiment Analysis** of daily mood logs.
*   **all-MiniLM-L6-v2 (Sentence-Transformers):** Converts text into 384-dimensional vectors. This allows us to calculate **Semantic Similarity** (using Cosine Similarity) between a user's hidden passions and career requirements.
*   **TF-IDF + Cosine Similarity:** A custom-trained machine learning layer (`tfidf_model.pkl`) that maps user input to our specific career database.
*   **DialoGPT (Microsoft):** A specialized conversational model used as a backup for the chatbot to maintain a "coaching" persona when offline.

### Training Process:
1.  **Preprocessing:** Data was cleaned by removing HTML (BeautifulSoup), lowering case, and filtering "stop words" (NLTK).
2.  **Vectorization:** We used `TfidfVectorizer` to learn the unique vocabulary of the career market.
3.  **Cross-Validation:** Models were tested against "Coaching Scenarios" (see `AI_COACHING_SCENARIOS.md`) to ensure the AI correctly identifies niche roles like "Health Informatics" from general healthcare/tech entries.

## 3. Data Sources & Datasets
Our models are grounded in high-quality, professional datasets:
*   **CareerVillage (Kaggle):** Thousands of Q&As between students and professionals were used to understand how people describe their jobs and passions.
*   **O*NET (Occupational Information Network):** Provided the structured "DNA" for careers (Tasks, Skills, Values, and RIASEC interests).
*   **Bureau of Labor Statistics (BLS):** Used for real-world salary data and "Bright Outlook" growth projections for 2030+.
*   **Custom Ikigai Dataset:** A specialized list of 12-20 future-oriented careers (AI Engineer, Sustainability Lead, etc.) curated to prioritize longevity and impact.

## 4. Chatbot Implementation
The Chatbot acts as an **AI Career Coach**.
*   **Context Awareness:** Unlike simple bots, ours pulls context from your **Profile** and your **last 3 Journal Entries**. It knows if you've been working on "React" or feeling "frustrated with clinic UIs."
*   **Intent Detection:** It uses keyword triggers for specific Ikigai concepts but falls back to Semantic Analysis for open-ended questions.
*   **Feedback Loop:** Chat conversations are analyzed to update your "Expert Pillars," which refine your career recommendations in real-time.

## 5. Performance & Accuracy
*   **Matching Accuracy:** Currently achieving high precision in top-5 career recommendations based on the `all-MiniLM-L6-v2` semantic overlap.
*   **Sentiment Precision:** ~91% accuracy (DistilBERT base) in detecting user frustration or excitement in journals.
*   **Latency:** The "Flash" version of Gemini and local TF-IDF models ensure responses are under 1.5 seconds.

## 6. Critical Review: The Good, The Bad, & The Better

### What is running best?
*   **Semantic Search:** The ability to find a career like "UX Designer" even if the user only mentions "drawing" and "making things easy for people."
*   **Framework Integration:** The mathematical mapping of the 4 Ikigai circles into a single "Match Score."

### What is still not best?
*   **Dataset Size:** While O*NET is great, our primary high-speed matching relies on a limited set of 20+ careers. Expanding this to 1000+ careers without losing recommendation "soul" is the next hurdle.
*   **Long-term Memory:** The bot remembers recent entries well but doesn't yet track progress over months of development.

### What could have been better?
*   **Fine-tuning vs. Prompting:** While Gemini is powerful, a dedicated fine-tuned LLaMA model on specific Ikigai counseling transcripts would likely provide a more distinct "human" coach feel compared to a general LLM.
*   **Cross-Platform Data:** Integrating LinkedIn or GitHub APIs directly would have provided higher accuracy for "Skills" (What you are good at) than manual user input.
