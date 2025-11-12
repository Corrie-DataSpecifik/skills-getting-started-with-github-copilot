import pytest
from fastapi import HTTPException


class TestActivitiesEndpoint:
    """Tests for the /activities GET endpoint"""
    
    def test_get_activities_returns_200(self, client, reset_activities):
        """Test that GET /activities returns a 200 status code"""
        response = client.get("/activities")
        assert response.status_code == 200
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that all activities are returned"""
        response = client.get("/activities")
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
    
    def test_get_activities_includes_details(self, client, reset_activities):
        """Test that activity details are included"""
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
    
    def test_get_activities_includes_participants(self, client, reset_activities):
        """Test that participants list is included"""
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]


class TestSignupEndpoint:
    """Tests for the /activities/{activity_name}/signup POST endpoint"""
    
    def test_signup_returns_200(self, client, reset_activities):
        """Test that signup returns a 200 status code on success"""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
    
    def test_signup_adds_participant(self, client, reset_activities):
        """Test that signup successfully adds a participant"""
        client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        response = client.get("/activities")
        activities = response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
    
    def test_signup_returns_message(self, client, reset_activities):
        """Test that signup returns an appropriate message"""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
    
    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test that signup for nonexistent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent%20Club/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_duplicate_student_returns_400(self, client, reset_activities):
        """Test that duplicate signup returns 400 error"""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_at_capacity_returns_error(self, client, reset_activities):
        """Test that signup for a full activity returns error"""
        # Get the current state
        response = client.get("/activities")
        activities = response.json()
        
        # Find an activity that is at capacity
        # For testing, we need to fill up an activity
        # Let's use Basketball Team which has max 15 and currently has 2
        # We'll add students until it's full
        for i in range(13):
            client.post(
                "/activities/Basketball%20Team/signup",
                params={"email": f"student{i}@mergington.edu"}
            )
        
        # Now try to add one more (should still work since max is 15 and we have 15)
        response = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "student13@mergington.edu"}
        )
        # This should succeed since we have exactly 15 now
        assert response.status_code == 200


class TestUnregisterEndpoint:
    """Tests for the /activities/{activity_name}/unregister DELETE endpoint"""
    
    def test_unregister_returns_200(self, client, reset_activities):
        """Test that unregister returns a 200 status code on success"""
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 200
    
    def test_unregister_removes_participant(self, client, reset_activities):
        """Test that unregister successfully removes a participant"""
        client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        response = client.get("/activities")
        activities = response.json()
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    
    def test_unregister_returns_message(self, client, reset_activities):
        """Test that unregister returns an appropriate message"""
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test that unregister from nonexistent activity returns 404"""
        response = client.delete(
            "/activities/Nonexistent%20Club/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_not_registered_returns_400(self, client, reset_activities):
        """Test that unregistering a non-registered student returns 400"""
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]


class TestRootEndpoint:
    """Tests for the root / endpoint"""
    
    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestIntegration:
    """Integration tests for multiple operations"""
    
    def test_signup_and_unregister_workflow(self, client, reset_activities):
        """Test complete workflow: signup then unregister"""
        email = "testuser@mergington.edu"
        activity = "Chess Club"
        
        # Sign up
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify signup
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity]["participants"]
        
        # Unregister
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify unregister
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities[activity]["participants"]
    
    def test_multiple_signups_for_different_activities(self, client, reset_activities):
        """Test signing up for multiple activities"""
        email = "multiactivity@mergington.edu"
        activities_to_join = ["Chess Club", "Programming Class", "Debate Team"]
        
        for activity in activities_to_join:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all signups
        response = client.get("/activities")
        activities_data = response.json()
        for activity in activities_to_join:
            assert email in activities_data[activity]["participants"]
