from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    quiz_responses = relationship("QuizResponse", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    age = Column(Integer, nullable=True)
    education_level = Column(String(100), nullable=True)
    work_experience_years = Column(Integer, default=0)
    bio = Column(Text, nullable=True)
    interests = Column(JSON, default=list)  # e.g., ["coding", "design", "marketing"]
    skills = Column(JSON, default=list)      # e.g., ["Python", "JavaScript", "UI Design"]
    values = Column(JSON, default=list)      # e.g., ["helping people", "creativity", "stability"]
    passion_areas = Column(JSON, default=list)  # e.g., ["AI", "Web Dev", "Data Science"]
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profile")


class QuizResponse(Base):
    __tablename__ = "quiz_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(String(100))
    category = Column(String(50))  # e.g., "ability", "interest", "values"
    response = Column(String(500))  # User's answer or categorical choice
    score = Column(Float, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="quiz_responses")


class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    career_title = Column(String(255))
    description = Column(Text)
    match_score = Column(Float)  # 0-100% match
    reasoning = Column(JSON)  # Why this career matches
    required_skills = Column(JSON, default=list)
    growth_potential = Column(String(50))  # High, Medium, Low
    market_demand = Column(String(50))  # High, Medium, Low
    salary_range_min = Column(Float, nullable=True)
    salary_range_max = Column(Float, nullable=True)
    future_oriented = Column(Boolean, default=True)  # Is this a future-oriented career?
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="recommendations")


class DailyEntry(Base):
    __tablename__ = "daily_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    activities = Column(JSON)  # Activities done today
    learnings = Column(Text, nullable=True)  # What did they learn?
    interests_explored = Column(JSON, default=list)  # New interests discovered
    challenges = Column(Text, nullable=True)  # What was challenging?
    mood = Column(String(50), nullable=True)  # happy, neutral, sad, etc.
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
