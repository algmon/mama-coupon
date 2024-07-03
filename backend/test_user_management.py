import hashlib
import pytest
import sqlite3

from user_management import register_user_to_db

@pytest.fixture
def mocker(request):
    return request.getfixturevalue("mocker")

@pytest.mark.parametrize(
    "username, password",
    [
        ("test_user1", "password1"),
        ("test_user2", "password2"),
        ("test_user3", "password3"),
    ],
)

def test_register_user_to_db_success(mocker, username, password):
    """
    TODO: Fix Test that the `register_user_to_db` function successfully registers a new user.
    """

    # Mock the sqlite3.connect function
    mocker.patch("sqlite3.connect")
    mocker.patch("sqlite3.Cursor")

    # Register a new user
    success = register_user_to_db("users.db", username, password)

    # Assert that the registration was successful
    assert success
    
    # Verify that the mocked database connection and cursor were called correctly
    cursor_mock = sqlite3.Cursor.return_value
    cursor_mock.execute.assert_called_once_with("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor_mock.fetchone()

    # Assert that the user data is correct
    assert user["username"] == username
    assert user["password"] == hashlib.sha256(password.encode()).hexdigest()
    assert user["last_active"] is not None