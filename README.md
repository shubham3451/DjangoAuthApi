# Django Authentication API

## Overview

This Django Authentication API provides a robust solution for managing user authentication and authorization in your application. It includes endpoints for user registration, login, password management, and more, all built using Django and Django REST Framework.

## Features

- **User Registration:** Allows new users to register with email and password.
- **User Login:** Authenticates users and provides a JSON Web Token (JWT) for session management.
- **Password Reset:** Facilitates password reset via email.
- **Token Management:** Supports JWT authentication for secure API access.
- **User Profile:** Endpoints for retrieving and updating user profiles.

## Prerequisites

- Python 3.8+
- Django 4.0+
- Django REST Framework
- djangorestframework-simplejwt (for JWT authentication)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/shubham3451/DjangoAuthApi.git
   cd DjangoAuth
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the Requirements:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (optional, for admin access):**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**

   ```bash
   python manage.py runserver
   ```

## API Endpoints

### User Registration

- **Endpoint:** `POST /api/register/`
- **Description:** Register a new user and get a jwt token.
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Response:**
  ```json
  {
    "message": "User registered successfully."
  }
  {
    "refresh": "refresh_token",
    "access": "access_token"
  }
  ```

### User Login

- **Endpoint:** `POST /api/login/`
- **Description:** Authenticate a user and get a JWT token.
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Response:**
  ```json
  {
    "refresh": "refresh_token",
    "access": "access_token"
  }


### Send Password Reset Link

- **Endpoint:** `POST /api/sendresetlink/`
- **Description:** Request a password reset link to be sent via email.
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Password reset link sent to your email."
  }
  ```

### Reset Password

- **Endpoint:** `POST /api/resetpassword/<passwordresetlink>/`
- **Description:** Reset the password using the token received in the password reset email.
- **Request Body:**
  ```json
  {
    "token": "reset_token",
    "password": "newpassword"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Password has been reset successfully."
  }
  ```



## Configuration

Update your `settings.py` to configure the authentication backend and JWT settings:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

# Email settings
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_USE_TLS = True

}
```



