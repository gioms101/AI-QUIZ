# Quiz Generator API  📚🤖

## Overview 🚀
The **Quiz Generator API** is a Django REST Framework-based application that allows users to generate quizzes using OpenAI's GPT model. Users can create quizzes based on prompts, retrieve questions, save answers, compute quiz results, and view popular quiz topics.

## Features ✨
- **Generate a Quiz:** Users can generate quizzes based on a provided prompt.
- **Retrieve Questions:** Users can fetch specific quiz questions and their possible answers.
- **Save User Answers:** Answers given by users are stored in the database.
- **Compute Quiz Results:** The system evaluates user responses and returns quiz results.
- **Popular Quiz Topics:** Retrieves the most popular quiz topics.
- **AI Integration:** Uses OpenAI's GPT-4o model to generate quizzes dynamically.
- **Celery Tasks:** Implements background tasks for analytics and cleanup.

---

## Tech Stack 🛠️
- **Django** (Backend framework)
- **Django REST Framework** (API development)
- **OpenAI GPT-4o** (Quiz generation & evaluation)
- **SQLite3** (Database)
- **Celery** (Asynchronous task processing)
- **Redis** (Task queue for Celery)
- **Decouple** (Environment variable management)

---

## OpenAI GPT Integration 🧠

### Input Validation & Restrictions 🚨
Before generating a quiz, the API enforces the following restrictions:

### ✅ **Valid Quiz Topic Required**
- If the prompt is unrelated (e.g., `"Hello, World"`), the API returns:
  ```json
  {"message": "I am a Quiz Generator. Please provide a valid topic to generate a quiz for you!"}
  ```
### ✅ **Max 10 Questions**
- If the user requests more than **10 questions**, the API returns:
  ```json
  {"message": "The maximum number of questions I can generate is 10."}
  ```
### ✅ **Max 4 Possible Answers Per Question**
- If the user requests more than **4 possible answers**, the API returns:
  ```json
  {"message": "Maximum size of possible answers is 4."}
  ```
---
## Quiz Response Format 📋

### **Without Possible Answers** (Default Format)
If the user does not request multiple-choice options:
```json
{
  "Who discovered gravity?": [],
  "has_possible_answers": false,
  "topic_name": "Science"
}
```

### **With Possible Answers**
If the user requests multiple-choice options:
```json
{
  "What is 2+2?": ["1", "2", "3", "4"],
  "has_possible_answers": true,
  "topic_name": "Math"
}
```



---

## API Endpoints 📡

### 1. Generate a Quiz
**Endpoint:** `POST /generate_quiz/`
- Requires authentication.
- Accepts a `prompt` string.
- Returns the first generated question ID.

### 2. Retrieve a Question
**Endpoint:** `GET /questions/<pk>/`
- Requires authentication.
- Retrieves a specific question and its possible answers.

### 3. Save User Answer
**Endpoint:** `POST /save_answer/`
- Requires authentication.
- Saves the user's selected answer.

### 4. Compute Quiz Result
**Endpoint:** `POST /compute_quiz/`
- Requires authentication.
- Evaluates quiz performance and returns the score.

### 5. Popular Quiz Topics
**Endpoint:** `GET /popular_quiz_topics/`
- Returns the top 5 most popular quiz topics.

---

## Background Tasks
- **count_topics:** Tracks the popularity of quiz topics.
- **delete_generated_quiz:** Deletes a user's generated quiz data after computation.

---

## Installation ⚙️

### Prerequisites
- Python 3.x
- Redis
- Virtual Environment (recommended)

### Setup Instructions
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/gioms101/AI-QUIZ.git
   cd quiz
   ```

2. **Create and Activate Virtual Environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file and add the following:
   ```env
   OPEN_AI_KEY=<your_openai_api_key>
   ```

5. **Run Migrations:**
   ```sh
   python manage.py migrate
   ```

6. **Start Redis and Celery Workers:**
   ```sh
   redis-server &  # Start Redis
   celery -A quiz worker --loglevel=info  # Start Celery worker
   ```

7. **Run the Development Server:**
   ```sh
   python manage.py runserver
   ```

---