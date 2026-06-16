<h1 align="center">Quizly</h1>

<p align="center">
AI-powered quiz generation from YouTube videos using Django, Whisper AI and Gemini.
</p>

## Setup & Run Locally

### 1. Create and activate a virtual environment

```bash
python -m venv env
```

**Windows:**

```bash
env\Scripts\activate
```

**macOS/Linux:**

```bash
source env/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

FFmpeg is required for audio processing and Whisper transcription.

Verify installation:

```bash
ffmpeg -version
```

### 4. Environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your-gemini-api-key
```

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start the backend

```bash
python manage.py runserver
```

> The backend will be available at `http://127.0.0.1:8000/`.

### 8. Start the frontend

```bash
python -m http.server 5500
```

> The frontend will be available at `http://127.0.0.1:5500/`.

## Features

* User registration
* Login & logout
* JWT authentication via HTTP-only cookies
* Quiz generation from YouTube URLs
* Audio download with yt-dlp
* Audio transcription with Whisper AI
* AI-generated quiz questions using Gemini
* Quiz management (create, read, update, delete)
* Admin panel for quiz and question management

## Architecture

| Component           | Description                                        |
| ------------------- | -------------------------------------------------- |
| **Authentication**  | JWT authentication with access and refresh tokens. |
| **YouTube Service** | Downloads audio from YouTube videos using yt-dlp.  |
| **Whisper Service** | Converts audio into text transcripts.              |
| **Gemini Service**  | Generates quiz content from transcripts.           |
| **Quiz Service**    | Creates and stores quizzes and questions.          |

## Tech Stack

### Backend

* Python
* Django
* Django REST Framework
* Simple JWT
* Whisper AI
* Gemini API
* yt-dlp
* FFmpeg

### Frontend

* HTML
* CSS
* JavaScript
