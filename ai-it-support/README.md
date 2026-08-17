# AI IT Support

This project provides a basic AI-powered IT support system with:
- API backend built with FastAPI
- Streamlit frontend
- Knowledge base for common IT issues
- Routing and ticket creation modules

## Run the API

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run the frontend

```bash
streamlit run frontend/streamlit_app.py
```

## Structure

- `app/` contains the backend logic
- `frontend/` contains the UI
- `knowledge/` stores troubleshooting documents
- `scripts/` contains ingestion utilities
