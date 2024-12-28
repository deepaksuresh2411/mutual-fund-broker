# Mutual Fund Broker Application

A Python-based application for managing and tracking mutual funds.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install required dependencies:

```bash
pip install -r requirements.txt
```


## Environment Setup

1. Create a `.env` file in the root directory:
```bash
touch .env
```
2. Add the following environment variables:
```
DEBUG=True
SECRET_KEY=your_secret_key_here
RAPID_API_KEY=your_rapid_api_key_here
RAPID_API_HOST=your_rapid_api_host
```

3. Get your RapidAPI key:
- Sign up at [RapidAPI](https://rapidapi.com/suneetk92/api/latest-mutual-fund-nav)
- Subscribe to the required API service
- Copy your API key and API host to the `.env` file

## Database Setup

1. Run migrations:
```bash
python manage.py migrate
```


## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the application at `http://localhost:8000`


## API Documentation & Postman Collection

The complete API documentation is available at:
 `https://documenter.getpostman.com/view/17816709/2sAYJ6CfTE#0c835608-39d3-4375-b051-8bb01436f3b1`