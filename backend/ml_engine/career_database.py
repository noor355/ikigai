"""
Career Database - Future-Oriented Professions Catalog
Based on Ikigai framework and future job market trends
"""

FUTURE_CAREERS = [
    {
        "id": "ai_ml_engineer",
        "title": "AI/Machine Learning Engineer",
        "description": "Design, build, and deploy AI systems that solve real-world problems",
        "passion_keywords": ["automation", "innovation", "data", "problem-solving", "AI", "learning"],
        "skill_keywords": ["python", "tensorflow", "pytorch", "statistics", "mathematics", "data analysis"],
        "value_keywords": ["progress", "innovation", "creating", "impact", "continuous learning"],
        "growth_potential": "Very High",
        "market_demand": "Very High",
        "salary_range": (150000, 250000),
        "future_oriented": True,
        "future_relevance": "Essential for 2030+",
        "required_skills": ["Python", "TensorFlow/PyTorch", "Statistics", "Mathematics", "Data Engineering"],
        "learning_path": ["Python basics", "Statistics & Math", "ML libraries", "Advanced ML", "Deep Learning"],
    },
    {
        "id": "data_scientist",
        "title": "Data Scientist",
        "description": "Extract insights from data to drive business decisions and innovation",
        "passion_keywords": ["data", "analytics", "patterns", "insights", "visualization", "problem-solving"],
        "skill_keywords": ["python", "sql", "tableau", "statistics", "pandas", "analysis"],
        "value_keywords": ["insights", "impact", "evidence-based", "creativity", "discovery"],
        "growth_potential": "Very High",
        "market_demand": "Very High",
        "salary_range": (130000, 200000),
        "future_oriented": True,
        "future_relevance": "Critical role in AI era",
        "required_skills": ["Python", "SQL", "Statistics", "Data Visualization", "Big Data Tools"],
        "learning_path": ["Statistics", "Python", "SQL", "Data Viz", "ML Basics"],
    },
    {
        "id": "software_architect",
        "title": "Software Architect",
        "description": "Design scalable, secure, and efficient software systems",
        "passion_keywords": ["design", "systems", "architecture", "problem-solving", "scaling", "innovation"],
        "skill_keywords": ["system design", "cloud", "microservices", "databases", "coding"],
        "value_keywords": ["quality", "elegance", "impact", "responsibility", "mastery"],
        "growth_potential": "High",
        "market_demand": "High",
        "salary_range": (140000, 220000),
        "future_oriented": True,
        "future_relevance": "Always in demand",
        "required_skills": ["System Design", "Cloud (AWS/Azure)", "Microservices", "Databases", "Leadership"],
        "learning_path": ["Systems thinking", "Cloud basics", "Microservices", "Design patterns", "Leadership"],
    },
    {
        "id": "cybersecurity_specialist",
        "title": "Cybersecurity Specialist",
        "description": "Protect organizations from digital threats and vulnerabilities",
        "passion_keywords": ["security", "protection", "problem-solving", "risk", "defense", "technology"],
        "skill_keywords": ["networking", "security protocols", "cryptography", "penetration testing", "tools"],
        "value_keywords": ["safety", "responsibility", "trust", "protection", "excellence"],
        "growth_potential": "Very High",
        "market_demand": "Very High",
        "salary_range": (120000, 200000),
        "future_oriented": True,
        "future_relevance": "Critical in 2030+",
        "required_skills": ["Networking", "Security Protocols", "Penetration Testing", "Cryptography", "Tools"],
        "learning_path": ["Networking basics", "Security fundamentals", "Tools & techniques", "Pen testing", "Advanced"],
    },
    {
        "id": "product_manager_tech",
        "title": "Tech Product Manager",
        "description": "Lead the vision, strategy, and development of technology products",
        "passion_keywords": ["innovation", "user experience", "leadership", "strategy", "impact", "vision"],
        "skill_keywords": ["product strategy", "analytics", "user research", "communication", "leadership"],
        "value_keywords": ["impact", "user satisfaction", "innovation", "leadership", "vision"],
        "growth_potential": "High",
        "market_demand": "High",
        "salary_range": (140000, 210000),
        "future_oriented": True,
        "future_relevance": "Increasingly important",
        "required_skills": ["Product Strategy", "Analytics", "User Research", "Communication", "Leadership"],
        "learning_path": ["User research", "Analytics", "Product strategy", "Communication", "Leadership"],
    },
    {
        "id": "ux_designer",
        "title": "UX/UI Designer",
        "description": "Create beautiful, intuitive digital experiences that delight users",
        "passion_keywords": ["design", "user experience", "creativity", "aesthetics", "usability", "innovation"],
        "skill_keywords": ["design", "figma", "prototyping", "user research", "psychology", "tools"],
        "value_keywords": ["creativity", "user satisfaction", "aesthetics", "empathy", "impact"],
        "growth_potential": "High",
        "market_demand": "High",
        "salary_range": (100000, 160000),
        "future_oriented": True,
        "future_relevance": "Essential skill for all products",
        "required_skills": ["UI/UX Design", "Figma/Sketch", "Prototyping", "User Research", "Psychology"],
        "learning_path": ["Design fundamentals", "Tools", "User research", "Prototyping", "Advanced UX"],
    },
    {
        "id": "cloud_architect",
        "title": "Cloud Solutions Architect",
        "description": "Design and implement scalable cloud infrastructure solutions",
        "passion_keywords": ["infrastructure", "scalability", "cloud", "optimization", "problem-solving", "systems"],
        "skill_keywords": ["aws", "azure", "kubernetes", "devops", "architecture", "infrastructure"],
        "value_keywords": ["efficiency", "scalability", "innovation", "reliability", "mastery"],
        "growth_potential": "Very High",
        "market_demand": "Very High",
        "salary_range": (140000, 230000),
        "future_oriented": True,
        "future_relevance": "Critical infrastructure role",
        "required_skills": ["AWS/Azure", "Kubernetes", "DevOps", "Architecture", "Networking"],
        "learning_path": ["Cloud fundamentals", "Containerization", "Orchestration", "Infrastructure", "Advanced"],
    },
    {
        "id": "quantum_computing_dev",
        "title": "Quantum Computing Developer",
        "description": "Develop solutions using quantum computing technology for complex problems",
        "passion_keywords": ["innovation", "cutting-edge", "physics", "quantum", "problem-solving", "future"],
        "skill_keywords": ["quantum mechanics", "qiskit", "python", "physics", "mathematics"],
        "value_keywords": ["innovation", "progress", "challenge", "future", "discovery"],
        "growth_potential": "Extremely High",
        "market_demand": "Growing",
        "salary_range": (160000, 250000),
        "future_oriented": True,
        "future_relevance": "Next frontier technology",
        "required_skills": ["Quantum Mechanics", "Qiskit", "Python", "Physics", "Mathematics"],
        "learning_path": ["Quantum physics", "Qiskit basics", "Python", "Advanced quantum", "Research"],
    },
    {
        "id": "sustainability_tech_lead",
        "title": "Sustainability Technology Lead",
        "description": "Use technology to solve environmental and sustainability challenges",
        "passion_keywords": ["environment", "sustainability", "climate", "impact", "innovation", "purpose"],
        "skill_keywords": ["data analysis", "iot", "sensors", "software", "systems thinking"],
        "value_keywords": ["environment", "social impact", "future generation", "responsibility", "purpose"],
        "growth_potential": "Very High",
        "market_demand": "Very High",
        "salary_range": (110000, 180000),
        "future_oriented": True,
        "future_relevance": "Essential for 2030+ climate goals",
        "required_skills": ["Data Analysis", "IoT", "Software Development", "Systems Thinking", "Domain Knowledge"],
        "learning_path": ["Environmental basics", "IoT/sensors", "Data analysis", "Software", "Specialized"],
    },
    {
        "id": "biotech_engineer",
        "title": "Biotech/Bioinformatics Engineer",
        "description": "Apply technology and engineering to biological and medical challenges",
        "passion_keywords": ["biology", "healthcare", "innovation", "research", "problem-solving", "impact"],
        "skill_keywords": ["bioinformatics", "python", "data analysis", "biology", "statistics"],
        "value_keywords": ["healthcare", "research", "impact", "discovery", "helping people"],
        "growth_potential": "Very High",
        "market_demand": "High",
        "salary_range": (120000, 200000),
        "future_oriented": True,
        "future_relevance": "Critical for biotech revolution",
        "required_skills": ["Bioinformatics", "Python", "Statistics", "Biology", "Data Analysis"],
        "learning_path": ["Biology basics", "Python", "Bioinformatics tools", "Statistics", "Advanced"],
    },
    {
        "id": "ar_vr_developer",
        "title": "AR/VR Developer",
        "description": "Create immersive experiences using augmented and virtual reality",
        "passion_keywords": ["immersive", "3d", "innovation", "creativity", "gaming", "experience"],
        "skill_keywords": ["unity", "unreal", "3d programming", "graphics", "user experience"],
        "value_keywords": ["creativity", "innovation", "user experience", "cutting-edge", "impact"],
        "growth_potential": "High",
        "market_demand": "High",
        "salary_range": (110000, 180000),
        "future_oriented": True,
        "future_relevance": "Growing metaverse role",
        "required_skills": ["Unity/Unreal", "3D Programming", "Graphics", "Physics", "UX"],
        "learning_path": ["3D basics", "Game engine", "Programming", "Graphics", "Advanced VR"],
    },
    {
        "id": "blockchain_engineer",
        "title": "Blockchain Engineer",
        "description": "Build decentralized systems using blockchain and Web3 technologies",
        "passion_keywords": ["decentralization", "blockchain", "crypto", "innovation", "finance", "systems"],
        "skill_keywords": ["solidity", "ethereum", "web3", "cryptography", "smart contracts"],
        "value_keywords": ["decentralization", "innovation", "disruption", "future", "transparency"],
        "growth_potential": "High",
        "market_demand": "Growing",
        "salary_range": (120000, 220000),
        "future_oriented": True,
        "future_relevance": "Web3 and DeFi future",
        "required_skills": ["Solidity", "Ethereum", "Web3", "Cryptography", "Smart Contracts"],
        "learning_path": ["Blockchain basics", "Solidity", "Web3 tools", "Smart contracts", "Advanced"],
    },
]


def get_all_careers():
    """Get all available careers"""
    return FUTURE_CAREERS


def get_career_by_id(career_id):
    """Get specific career by ID"""
    for career in FUTURE_CAREERS:
        if career["id"] == career_id:
            return career
    return None


def search_careers_by_keyword(keyword):
    """Search careers matching a keyword"""
    results = []
    keyword_lower = keyword.lower()
    
    for career in FUTURE_CAREERS:
        title_match = keyword_lower in career["title"].lower()
        description_match = keyword_lower in career["description"].lower()
        
        if title_match or description_match:
            results.append(career)
    
    return results
