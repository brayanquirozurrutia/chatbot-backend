# Chatbot Backend

A powerful backend system for a chatbot that integrates Artificial Intelligence (AI), Natural Language Processing (NLP), and caching for enhanced performance and scalability. This backend is built with FastAPI, SQLAlchemy, Redis, and PostgreSQL.

## Features

- **AI-Powered Chat:** Integrates the Gemini API to generate AI-driven responses.
- **Natural Language Processing (NLP):** Extracts keywords using spaCy to improve response accuracy.
- **Caching:** Utilizes Redis to cache responses and reduce latency.
- **FAQ Management:** Allows adding, retrieving, and managing frequently asked questions (FAQs) through a database.
- **WebSocket Support:** Real-time communication between the user and the chatbot.
- **Multi-Platform Integration:** Provides links to WhatsApp for further user engagement.

---

## Installation

### Prerequisites

- **Docker** and **Docker Compose**
- **Python 3.10+**
- **PostgreSQL**

### Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/brayanquirozurrutia/chatbot-backend.git
   cd chatbot-backend
   ```

2. **Configure Environment Variables**
   Create a `.env` file in the project root directory with the following variables:
   ```env
   GEMINI_API_KEY=your-gemini-api-key
   WHATSAPP_PHONE=your-whatsapp-number
   ```

3. **Build and Run with Docker**
   ```bash
   docker-compose up --build
   ```

   This will set up the backend, database, and Redis containers.

4. **Access the Application**
   The FastAPI application will run at `http://localhost:8000`. You can explore the API documentation at `http://localhost:8000/docs`.

---

## API Endpoints

### Chat Endpoints
- `POST /chat/`: Generate a response for user input.
- `GET /chat/ws/{client_id}`: WebSocket endpoint for real-time chat.

### FAQ Endpoints
- `POST /faqs/`: Add a new FAQ.
- `GET /faqs/`: Retrieve all FAQs.

### Cache Endpoints
- `POST /cache/clear_cache`: Clear all cached responses.

---

## Architecture

### Tech Stack
- **FastAPI:** Web framework for building APIs.
- **PostgreSQL:** Relational database for persistent storage.
- **Redis:** In-memory database for caching.
- **spaCy:** NLP library for extracting keywords.
- **Docker:** Containerization for portability and scalability.

### Directory Structure
```
├── app
│   ├── routers
│   │   ├── chat.py
│   │   ├── faqs.py
│   │   ├── cache.py
│   ├── services
│   │   ├── chat_ai.py
│   │   ├── nlp.py
│   │   ├── redis_cache.py
│   ├── database.py
│   ├── models.py
│   ├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

## Development

### Install Dependencies

If you want to run the project locally without Docker:

1. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations:**
   ```bash
   python -m app.database
   ```

4. **Run the Application:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Tests

To add tests, use a testing library like **pytest**. Place test files in the `tests` directory and run:

```bash
pytest
```

---

## Author

Developed with ❤️ by [Brayan Nicolas Quiroz Urrutia](https://www.brayanquiroz.cl/).

