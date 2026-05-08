# Data Sourcing Strategy for Ikigai Career Database

To enhance the `career_database.py` with high-quality, real-world data, we can leverage several authoritative sources.

## 1. Primary Data Sources

### A. O*NET (Occupational Information Network)
*   **Source:** [O*NET OnLine](https://www.onetonline.org/)
*   **Data Points:** Detailed task lists, required skills, work values, and interests (RIASEC).
*   **Import Strategy:**
    1.  Download the **O*NET Database** (SQL or Text format).
    2.  Use the `Skills` and `Work Styles` tables to populate `skill_keywords` and `value_keywords`.
    3.  Map O*NET "Interests" (Social, Investigative, etc.) to Ikigai "Passion" areas.

### B. CareerVillage Dataset
*   **Source:** [Kaggle - CareerVillage](https://www.kaggle.com/c/careervillage)
*   **Data Points:** Real-world questions from students and answers from professionals.
*   **Import Strategy:**
    1.  Use the `professionals.py` and `tags.csv` to identify trending career labels.
    2.  Perform NLP analysis on the `answers.csv` to extract typical "Day in the life" descriptions for `description` fields.

### C. Bureau of Labor Statistics (BLS)
*   **Source:** [U.S. BLS Occupational Outlook Handbook](https://www.bls.gov/ooh/)
*   **Data Points:** Salary ranges (`salary_range`), growth projections (`growth_potential`), and education requirements.
*   **Import Strategy:**
    1.  Scrape or API-fetch the 10-year growth projections.
    2.  Update the `market_demand` and `future_relevance` fields based on BLS "Bright Outlook" tags.

## 2. Implementation: `career_database.py` Update Pattern

When importing these datasets, use the following mapping pattern to maintain consistency with the Ikigai engine:

```python
{
    "id": "external_id_001",
    "title": "Data Scientist", # O*NET 'Title'
    "description": "...", # O*NET 'Report' or OOH 'Summary'
    "passion_keywords": [], # Derived from O*NET 'Interests'
    "skill_keywords": [], # Derived from O*NET 'Skills' table
    "value_keywords": [], # Derived from O*NET 'Work Values'
    "growth_potential": "Very High", # Derived from O*NET 'Outlook'
    "salary_range": (min, max), # Derived from BLS wage data
}
```

## 3. Recommended Automated Import Script
I recommend creating a `backend/ml_engine/data_importer.py` that:
1.  Downloads CSVs from the above sources.
2.  Parses them using `pandas`.
3.  Clusters similar professions.
4.  Appends them to `FUTURE_CAREERS` in `career_database.py`.
