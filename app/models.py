from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey  # Importing ForeignKey and Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DATABASE_URL = "sqlite:///./test.db"  # SQLite database URL

Base = declarative_base()

# Table for User Authentication and Profile Data
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Hashed password will be stored here
    phone_number = Column(String)
    
    # One-to-many relationship with user progress (user can have multiple progress records)
    progress = relationship("UserProgress", back_populates="user")
    
    # One-to-many relationship with courses enrolled (user can enroll in multiple courses)
    courses = relationship("CourseEnrollment", back_populates="user")

class UserProgress(Base):
    __tablename__ = 'user_progress'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    experience = Column(Integer)
    tokens_earned = Column(Integer)
    rank = Column(Integer)
    level = Column(Integer)
    badge = Column(String)  # badge column
    
    user = relationship('User', back_populates='progress')



# Table for Course Enrollment and Progress
class CourseEnrollment(Base):
    __tablename__ = 'course_enrollments'
    
    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String)
    progress_percentage = Column(Float)  # % of course progress
    
    # Foreign key to User
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship("User", back_populates="courses")

# Table for Recommended YouTube Playlists
class YouTubePlaylist(Base):
    __tablename__ = 'youtube_playlists'
    
    id = Column(Integer, primary_key=True, index=True)
    playlist_url = Column(String)  # URL of the YouTube playlist
    description = Column(String)  # Short description of the playlist

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the session
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the database (if they don't already exist)
Base.metadata.create_all(bind=engine)

