from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from models import User, UserProgress
from schemas import UserRegister, UserLogin, UserResponse, UserProgressResponse, UpdateProgressRequest, UserRankResponse
from auth import register_user, authenticate_user, get_current_user
from typing import List
from sqlalchemy import desc

app = FastAPI()

def initialize_user_progress(db: Session, user_id: int, tokens_earned: int = 0, experience_gained: int = 0):
    # Check if UserProgress already exists for the user
    user_progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()

    if user_progress:
        return user_progress  # UserProgress already exists, no need to add new one

    # If no progress exists, create a new UserProgress entry
    new_user_progress = UserProgress(
        user_id=user_id,
        tokens_earned=tokens_earned,
        experience=experience_gained,
        rank=1,  # Default rank
        level=1,  # Default level
        badge='Unbadged'  # Default badge
    )

    try:
        # Add the new UserProgress and commit
        db.add(new_user_progress)
        db.commit()  # Commit the transaction to save it to the database
        db.refresh(new_user_progress)  # Optional: refresh the object to get the latest data
        return new_user_progress
    except Exception as e:
        db.rollback()  # Rollback in case of error
        print(f"Error initializing user progress: {e}")
        return None  # Or handle the error as appropriate



    # Add the new progress entry to the session
    db.add(new_user_progress)
    db.commit()
    db.refresh(new_user_progress)

    return new_user_progress

# This function determines the badge based on experience.
def get_badge_based_on_experience(experience: int) -> str:
    if experience < 10:
        return "Unbadged"
    elif experience < 100:
        return "Noob"
    elif experience < 1000:
        return "Amateur"
    elif experience < 10000:
        return "Intermediate"
    elif experience < 100000:
        return "Expert"
    else:
        return "Master"


# Route to register a new user
@app.post("/register/")
def register(user: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, user.username, user.email, user.password, user.phone_number)
    
    # Initialize user progress after registration
    initialize_user_progress(db, user.id)  # Use the user id from the created user
    
    return {"message": "User created successfully", "username": user.username}

# Route to log in and get a token
@app.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user.username, user.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "User logged in successfully", "username": user.username}

# Route to get current user details (requires a valid token)
@app.get("/users/me")
def get_user_me(current_user: dict = Depends(get_current_user)):
    return current_user

# New Route to get all users
@app.get("/users/", response_model=List[UserProgressResponse])
def get_all_users_with_rank(db: Session = Depends(get_db)):
    # Query all users along with their progress (experience and rank) from the database
    users_with_progress = db.query(UserProgress).join(User).all()

    if not users_with_progress:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

    # Sort users by experience in descending order
    users_with_progress = sorted(users_with_progress, key=lambda x: x.experience, reverse=True)

    # Assign ranks based on sorted experience
    for rank, user_progress in enumerate(users_with_progress, start=1):
        user_progress.rank = rank  # Assign rank based on sorted experience
        user_progress.badge = get_badge_based_on_experience(user_progress.experience)

    # Return a list of users with their rank and experience
    return users_with_progress


# Route to get user progress by user_id
@app.post("/update_tokens/{user_id}")
async def update_tokens(user_id: int, progress: UpdateProgressRequest, db: Session = Depends(get_db)):
    # Try to find the user progress entry for the given user_id
    user_progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()

    if not user_progress:
        raise HTTPException(status_code=404, detail="User progress not found")

    # Increment the user's experience and tokens with the new data
    user_progress.tokens_earned += progress.tokens_earned  # Add the new tokens
    user_progress.experience += progress.experience_gained  # Add the new experience

    # Recalculate the badge based on the updated experience
    badge = get_badge_based_on_experience(user_progress.experience)
    user_progress.badge = badge

    # Commit the changes to the database
    db.commit()
    db.refresh(user_progress)

    # Now that the progress is updated, let's recalculate and update ranks for all users
    all_user_progress = db.query(UserProgress).all()

    # Sort all users by experience in descending order
    sorted_users = sorted(all_user_progress, key=lambda x: x.experience, reverse=True)

    # Reassign ranks to all users based on sorted experience
    for rank, user in enumerate(sorted_users, start=1):
        user.rank = rank
        db.commit()  # Commit each rank change

    # Refresh user progress after updating rank
    db.refresh(user_progress)

    return {"message": "User progress and rank updated successfully", "progress": user_progress}



# Function to get the leaderboard sorted by tokens_earned (can change to experience or rank if needed)

@app.get("/users_with_rank/", response_model=List[UserRankResponse])
def get_users_with_rank(db: Session = Depends(get_db)):
    # Query all users with their user progress (rank and experience)
    users = db.query(User, UserProgress).join(UserProgress, User.id == UserProgress.user_id).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

    # Prepare the response by extracting relevant details
    response = []
    for user, progress in users:
        response.append({
            "username": user.username,
            "experience_gained": progress.experience,
            "rank": progress.rank
        })

    return response


