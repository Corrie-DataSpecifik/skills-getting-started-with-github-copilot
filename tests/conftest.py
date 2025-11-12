import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Outdoor soccer practices and weekend matches against other schools",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["alex@mergington.edu", "chris@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team with regular practices and league play",
            "schedule": "Mondays, Wednesdays, 5:00 PM - 7:00 PM",
            "max_participants": 15,
            "participants": ["nina@mergington.edu", "leo@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and mixed media projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu", "liam@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, play production, and stagecraft for school performances",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["zoe@mergington.edu", "ethan@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills; compete in debate tournaments",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["rachel@mergington.edu", "sam@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and science fairs, and STEM projects",
            "schedule": "Tuesdays, 3:45 PM - 5:15 PM",
            "max_participants": 20,
            "participants": ["oliver@mergington.edu", "ava@mergington.edu"]
        }
    }
    
    # Clear and repopulate activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Reset after test
    activities.clear()
    activities.update(original_activities)
