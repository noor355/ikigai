from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# ==================== Auth Schemas ====================
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# ==================== User Schemas ====================
class UserProfileCreate(BaseModel):
    age: Optional[int] = None
    education_level: Optional[str] = None
    work_experience_years: int = 0
    bio: Optional[str] = None
    interests: List[str] = []
    skills: List[str] = []
    values: List[str] = []
    passion_areas: List[str] = []
    location: Optional[str] = None


class UserProfileUpdate(BaseModel):
    age: Optional[int] = None
    education_level: Optional[str] = None
    work_experience_years: Optional[int] = None
    bio: Optional[str] = None
    interests: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    values: Optional[List[str]] = None
    passion_areas: Optional[List[str]] = None
    location: Optional[str] = None


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    age: Optional[int]
    education_level: Optional[str]
    work_experience_years: int
    bio: Optional[str]
    interests: List[str]
    skills: List[str]
    values: List[str]
    passion_areas: List[str]
    location: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    profile: Optional[UserProfileResponse] = None
    
    class Config:
        from_attributes = True


# ==================== Quiz Schemas ====================
class QuizResponseCreate(BaseModel):
    question_id: str
    category: str  # ability, interest, values
    response: str
    score: Optional[float] = None


class QuizResponseData(BaseModel):
    id: int
    user_id: int
    question_id: str
    category: str
    response: str
    score: Optional[float]
    date: datetime
    
    class Config:
        from_attributes = True


# ==================== Recommendation Schemas ====================
class RecommendationCreate(BaseModel):
    career_title: str
    description: str
    match_score: float
    reasoning: dict
    required_skills: List[str]
    growth_potential: str
    market_demand: str
    salary_range_min: Optional[float] = None
    salary_range_max: Optional[float] = None
    future_oriented: bool = True


class RecommendationResponse(BaseModel):
    id: int
    user_id: int
    career_title: str
    description: str
    match_score: float
    reasoning: dict
    required_skills: List[str]
    growth_potential: str
    market_demand: str
    salary_range_min: Optional[float]
    salary_range_max: Optional[float]
    future_oriented: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Daily Entry Schemas ====================
class DailyEntryCreate(BaseModel):
    activities: List[str]
    learnings: Optional[str] = None
    interests_explored: List[str] = []
    challenges: Optional[str] = None
    mood: Optional[str] = None
    notes: Optional[str] = None


class DailyEntryResponse(BaseModel):
    id: int
    user_id: int
    date: datetime
    activities: List[str]
    learnings: Optional[str]
    interests_explored: List[str]
    challenges: Optional[str]
    mood: Optional[str]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
