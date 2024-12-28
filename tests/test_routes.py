import pytest
from flask import url_for
from models import EmailRequest

def test_homepage(client):
    """Test the homepage (GET /)."""
    response = client.get("/")
    assert response.status_code == 200
    # Check for specific content on the homepage
    assert b"Don Fox" in response.data
    assert b"A software developer with over 25 years of experience" in response.data


def test_resume_get(client):
    """Test accessing the resume page (GET /resume)."""
    response = client.get("/resume")
    assert response.status_code == 200
    # Assert key content from the page
    assert b"Resume" in response.data  # Check the page title
    assert b"Don Fox" in response.data  # Check the header
    assert b"Your Full Name" in response.data  # Check form label
    assert b"Email Address" in response.data  # Check form label
    assert b"Request Resume" in response.data  # Check button text


from unittest.mock import patch

def test_resume_post_valid(client, app):
    """Test submitting the resume form with valid data (POST /resume)."""
    data = {"name": "John Doe", "email": "johndoe@example.com"}

    # Mock the `send_email` function in the `routes` module to simulate success
    with patch("routes.send_email", return_value=(True, "Email sent successfully")):
        response = client.post("/resume", data=data, follow_redirects=True)

        # Check if the response indicates success
        assert response.status_code == 200
        assert b"Email sent successfully" in response.data

        # Verify the database record
        with app.app_context():
            from models import EmailRequest  # Import within the context
            record = EmailRequest.query.filter_by(email="johndoe@example.com").first()
            assert record is not None
            assert record.name == "John Doe"


    # Verify database record
    with app.app_context():
        record = EmailRequest.query.filter_by(email="johndoe@example.com").first()
        assert record is not None
        assert record.name == "John Doe"

def test_resume_post_invalid(client):
    """Test submitting the resume form with invalid data (POST /resume)."""
    data = {"name": "John Doe", "email": "invalid-email"}
    response = client.post("/resume", data=data, follow_redirects=True)
    
    # Check if the response indicates an error
    assert response.status_code == 200
    assert b"Please provide a valid email address!" in response.data  # Check for the flash message


def test_books(client):
    """Test accessing the books page (GET /books)."""
    response = client.get("/books")
    assert response.status_code == 200
    
    # Assert unique content from the books page
    assert b"<h3 class=\"name-header\">Books Related to Computing</h3>" in response.data
    assert b"<h2>Favorite Books Related to Computing</h2>" in response.data