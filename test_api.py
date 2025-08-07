#!/usr/bin/env python3
"""
Simple test script to verify API endpoints are working correctly.
Run this after starting the Django development server.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"


def test_registration():
    """Test user registration endpoint"""
    print("Testing user registration...")
    
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "role": "worker"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register/", json=data)
        if response.status_code == 201:
            print("✅ Registration successful")
            return response.json()
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(response.json())
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running on localhost:8000")
        return None


def test_login(email, password):
    """Test user login endpoint"""
    print(f"Testing login for email: {email}...")
    
    data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login/", json=data)
        if response.status_code == 200:
            print("✅ Login successful")
            return response.json()
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.json())
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running on localhost:8000")
        return None


def test_profile_access(access_token):
    """Test protected profile endpoint"""
    print("Testing profile access with JWT token...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/auth/profile/", headers=headers)
        if response.status_code == 200:
            print("✅ Profile access successful")
            print(f"User data: {response.json()}")
            return True
        else:
            print(f"❌ Profile access failed: {response.status_code}")
            print(response.json())
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure Django server is running on localhost:8000")
        return False


def main():
    print("=" * 50)
    print("Agnovat API Test Script")
    print("=" * 50)
    print("Make sure to start the Django server first:")
    print("python manage.py runserver")
    print("=" * 50)
    
    # Test registration
    registration_result = test_registration()
    if not registration_result:
        print("\nSkipping login test due to registration failure...")
        # Try with existing user instead
        login_result = test_login("test@example.com", "testpass123")
    else:
        # Use the newly registered user
        login_result = test_login("test@example.com", "testpass123")
    
    if login_result and "access" in login_result:
        access_token = login_result["access"]
        test_profile_access(access_token)
    else:
        print("Cannot test profile access without valid login")
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("Visit http://localhost:8000/swagger/ for interactive API docs")
    print("Visit http://localhost:8000/admin/ for Django admin")
    print("=" * 50)


if __name__ == "__main__":
    main()
