# Misconception Detector

A high-performance machine learning application built with FastAPI and PostgreSQL designed to detect, log, and analyze misconceptions or factual inaccuracies in text data.

## 🚀 Features

*   **FastAPI Backend**: High-performance, asynchronous REST API endpoints.
*   **Machine Learning Pipeline**: Integrated ML model for real-time text classification and analysis.
*   **PostgreSQL Storage**: Robust relational database storage for managing logged entries, detection history, and model metadata.
*   **Scalable Architecture**: Decoupled application layer ready for containerisation and cloud deployment.

## 🛠️ Tech Stack

*   **Language**: Python 100%
*   **Framework**: FastAPI
*   **Database**: PostgreSQL
*   **ORM / Migration**: SQLAlchemy / Alembic

## 📁 Repository Structure

```text
misconception-detector/
├── app/                  # Main application source code
│   ├── api/              # API routers and endpoints
│   ├── core/             # Configuration, security, and database connection
│   ├── models/           # SQLAlchemy / database models
│   ├── schemas/          # Pydantic validation schemas
│   └── services/         # Machine learning logic and core detection algorithms
├── .gitignore            # Git ignore configurations
└── README.md             # Project documentation
```

## ⚙️ Getting Started

### Prerequisites

*   Python 3.10+
*   PostgreSQL Database v18

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd misconception-detector
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the dependencies (ensure you create a `requirements.txt` or `pyproject.toml` file):
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file in the root directory and add your system configuration details:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/misconception_db
MODEL_PATH=app/services/models/your_model.pkl
SECRET_KEY=your_super_secret_key
```

### Running the Application

Start the local FastAPI development server using Uvicorn:

```bash
python -m fastapi dev app/main.py                                     
```

The application will be accessible at `http://127.0.0.1:8000`. You can explore the interactive Swagger API documentation at ` http://127.0.0.1:8000/docs`.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
