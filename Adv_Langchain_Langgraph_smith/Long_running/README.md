# Long Running Workflow Demo

Terminal 1:
python workflow.py

Terminal 2:
uvicorn approval_api:app --reload

1. Run workflow.py (it pauses waiting for approval)
2. Call http://127.0.0.1:8000/approve
3. Run workflow.py again (it resumes)
