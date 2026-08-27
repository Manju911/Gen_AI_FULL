

# AI Chat Application – Deploy to Google Cloud Run

A simple AI chat application built with **Python, Streamlit, and OpenAI**, deployed using **Docker and Google Cloud Run**.

## Architecture

```text
User
  |
  v
Cloud Run
  |
  v
Streamlit Application
  |
  v
OpenAI API
  |
  v
AI Response
```

The application runs as a container on Cloud Run.

---

# 1. Prerequisites

Make sure you have:

* A Google Cloud account
* A Google Cloud Project
* Billing enabled
* OpenAI API key
* Google Cloud SDK / Cloud Shell

You can deploy directly from **Google Cloud Shell**.

---

# 2. Project Structure

Your project should look similar to this:

```text
Cloud-run/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .env
└── .gitignore
```

Example:

```text
Cloud-run
│
├── app.py
├── requirements.txt
├── Dockerfile
└── .env
```

---

# 3. Create the Streamlit Application

## `app.py`

```python
import os

import streamlit as st
from openai import OpenAI


st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖"
)

st.title("🤖 AI Chat Application")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


question = st.text_input(
    "Ask me anything"
)


if st.button("Ask"):

    if question:

        with st.spinner("Thinking..."):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            answer = response.choices[0].message.content

            st.success(answer)

    else:

        st.warning(
            "Please enter a question"
        )
```

---

# 4. Create `requirements.txt`

```txt
streamlit
openai
```

---

# 5. Create the Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD streamlit run app.py \
    --server.address=0.0.0.0 \
    --server.port=$PORT
```

## Important

Cloud Run automatically provides the `PORT` environment variable.

Usually:

```text
PORT=8080
```

So Streamlit must listen on:

```text
0.0.0.0:$PORT
```

Do not hardcode the port as `8501` for Cloud Run.

---

# 6. Create `.env`

For local development:

```env
OPENAI_API_KEY=your_openai_api_key
```

Do **not** upload this file to GitHub.

Add `.env` to `.gitignore`.

---

# 7. Create `.gitignore`

```txt
.env

__pycache__/

*.pyc

.venv/

venv/
```

---

# 8. Test Locally

First build the Docker image:

```bash
docker build -t ai-chat .
```

Check whether the image exists:

```bash
docker images
```

You should see something similar to:

```text
REPOSITORY    TAG       IMAGE ID
ai-chat       latest    xxxxxxxx
```

Now run it:

```bash
docker run \
  -p 8080:8080 \
  --env-file .env \
  -e PORT=8080 \
  ai-chat
```

Open:

```text
http://localhost:8080
```

---

# 9. Open Google Cloud Shell

Go to Google Cloud Console and open **Cloud Shell**.

Check your active project:

```bash
gcloud config get-value project
```

If needed:

```bash
gcloud config set project YOUR_PROJECT_ID
```

For example:

```bash
gcloud config set project ai-it-support-prod
```

Verify:

```bash
gcloud config get-value project
```

---

# 10. Enable Required APIs

Run:

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  storage.googleapis.com
```

These services are used for:

```text
Cloud Run
    ↓
Cloud Build builds your container
    ↓
Artifact Registry stores the image
    ↓
Cloud Run runs the image
```

---

# 11. Understanding Your IAM Error

You received this error:

```text
Permission 'storage.objects.get' denied
```

The error mentioned:

```text
590191520261-compute@developer.gserviceaccount.com
```

This is the **Compute Engine default service account** used during the deployment/build process.

It was trying to access your uploaded source code from a Google Cloud Storage bucket:

```text
run-sources-ai-it-support-prod-asia-south1
```

But it did not have permission to read the object.

That is why the deployment failed.

---

# 12. Get Your Project Number

Run:

```bash
PROJECT_ID=$(gcloud config get-value project)

PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID \
  --format="value(projectNumber)")
```

Check it:

```bash
echo $PROJECT_ID

echo $PROJECT_NUMBER
```

You should see something like:

```text
ai-it-support-prod
590191520261
```

---

# 13. Identify the Compute Service Account

The default Compute Engine service account follows this format:

```text
PROJECT_NUMBER-compute@developer.gserviceaccount.com
```

Create a variable:

```bash
COMPUTE_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
```

Check it:

```bash
echo $COMPUTE_SA
```

Example:

```text
590191520261-compute@developer.gserviceaccount.com
```

---

# 14. Grant Storage Permission

To fix the error, grant the service account permission to access objects.

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$COMPUTE_SA" \
  --role="roles/storage.objectViewer"
```

This gives permission to:

```text
storage.objects.get
```

The service account can now read the uploaded source archive.

---

# 15. Grant Cloud Build Permissions

For deployments from source, make sure the relevant service accounts have the necessary build permissions.

Get the Cloud Build service account:

```bash
CLOUD_BUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"
```

Grant Cloud Build permissions:

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/cloudbuild.builds.builder"
```

Also allow it to work with Artifact Registry:

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/artifactregistry.writer"
```

---

# 16. Recommended IAM Setup

For your simple student project, the important permissions are:

| Service Account                   | Role                               | Purpose              |
| --------------------------------- | ---------------------------------- | -------------------- |
| Compute Default Service Account   | Storage Object Viewer              | Read uploaded source |
| Cloud Build Service Account       | Cloud Build Builder                | Build application    |
| Cloud Build Service Account       | Artifact Registry Writer           | Push Docker image    |
| Cloud Run Runtime Service Account | Cloud Run Invoker/User as required | Run/access service   |

For simple learning projects, project-level permissions are easier to understand.

For production, permissions should follow the **principle of least privilege**.

---

# 17. Deploy to Cloud Run

Go to your project directory:

```bash
cd ~/Cloud-run
```

Check the files:

```bash
ls
```

You should see:

```text
app.py
requirements.txt
Dockerfile
```

Now deploy:

```bash
gcloud run deploy ai-chat \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

Cloud Run will:

```text
1. Upload your source code
        ↓
2. Cloud Build builds Docker image
        ↓
3. Image stored in Artifact Registry
        ↓
4. Cloud Run creates revision
        ↓
5. Container starts
        ↓
6. Cloud Run provides public URL
```

At the end, you will get something like:

```text
Service [ai-chat] revision [ai-chat-00001-xxx]
has been deployed and is serving 100 percent of traffic.

Service URL:
https://ai-chat-xxxxx-uc.a.run.app
```

Open that URL in your browser.

---

# 18. Better Approach: Use Secret Manager

Instead of exposing the API key directly using:

```bash
--set-env-vars OPENAI_API_KEY=YOUR_KEY
```

For production, use Google Secret Manager.

Enable the API:

```bash
gcloud services enable secretmanager.googleapis.com
```

Create the secret:

```bash
echo -n "YOUR_OPENAI_API_KEY" | \
gcloud secrets create openai-api-key \
  --data-file=-
```

If the secret already exists:

```bash
echo -n "YOUR_OPENAI_API_KEY" | \
gcloud secrets versions add openai-api-key \
  --data-file=-
```

---

# 19. Grant Cloud Run Access to the Secret

Get the default Compute service account:

```bash
COMPUTE_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
```

Grant access:

```bash
gcloud secrets add-iam-policy-binding openai-api-key \
  --member="serviceAccount:$COMPUTE_SA" \
  --role="roles/secretmanager.secretAccessor"
```

---

# 20. Deploy Using Secret Manager

Now deploy:

```bash
gcloud run deploy ai-chat \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest
```

Your architecture now becomes:

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Cloud Run    │
                    │                 │
                    │ Streamlit App   │
                    └────────┬────────┘
                             │
                 Reads Secret │
                             ▼
                    ┌─────────────────┐
                    │ Secret Manager  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   OpenAI API    │
                    └─────────────────┘
```

---

# 21. Check Cloud Run Service

List services:

```bash
gcloud run services list \
  --region asia-south1
```

Describe the service:

```bash
gcloud run services describe ai-chat \
  --region asia-south1
```

Get the URL:

```bash
gcloud run services describe ai-chat \
  --region asia-south1 \
  --format="value(status.url)"
```

---

# 22. View Logs

View recent logs:

```bash
gcloud run services logs read ai-chat \
  --region asia-south1
```

Stream logs:

```bash
gcloud run services logs tail ai-chat \
  --region asia-south1
```

You can also view logs in:

**Google Cloud Console → Cloud Run → ai-chat → Logs**

---

# 23. Deploy Updates

When you change your code:

```bash
gcloud run deploy ai-chat \
  --source . \
  --region asia-south1
```

Cloud Run automatically:

```text
New Code
   ↓
New Docker Image
   ↓
New Cloud Run Revision
   ↓
Traffic moved to new revision
```

Your old revision can still exist for rollback.

---

# 24. Troubleshooting

## Error: Permission denied

Example:

```text
storage.objects.get denied
```

Fix:

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$COMPUTE_SA" \
  --role="roles/storage.objectViewer"
```

---

## Error: Container failed to start

Check:

```bash
gcloud run services logs tail ai-chat \
  --region asia-south1
```

Make sure your Dockerfile uses:

```dockerfile
--server.port=$PORT
```

And:

```dockerfile
--server.address=0.0.0.0
```

---

## Error: OpenAI API Key Missing

Make sure the environment variable exists:

```text
OPENAI_API_KEY
```

If using Secret Manager:

```bash
gcloud run services describe ai-chat \
  --region asia-south1
```

Check the environment configuration.

---

# Complete Deployment Commands

For your project, the end-to-end flow can be:

```bash
# Set project

gcloud config set project ai-it-support-prod


# Enable APIs

gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  storage.googleapis.com \
  secretmanager.googleapis.com


# Get project information

PROJECT_ID=$(gcloud config get-value project)

PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID \
  --format="value(projectNumber)")


# Compute service account

COMPUTE_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"


# Cloud Build service account

CLOUD_BUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"


# Fix Storage permission

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$COMPUTE_SA" \
  --role="roles/storage.objectViewer"


# Cloud Build permissions

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/cloudbuild.builds.builder"


gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$CLOUD_BUILD_SA" \
  --role="roles/artifactregistry.writer"


# Create OpenAI secret

echo -n "YOUR_OPENAI_API_KEY" | \
gcloud secrets create openai-api-key \
  --data-file=-


# Give runtime service account access

gcloud secrets add-iam-policy-binding openai-api-key \
  --member="serviceAccount:$COMPUTE_SA" \
  --role="roles/secretmanager.secretAccessor"


# Deploy

gcloud run deploy ai-chat \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest
```

## Simple explanation for students

You can explain the whole deployment in **one flow**:

```text
Developer writes Python + Streamlit application
                    ↓
Dockerfile packages the application
                    ↓
gcloud run deploy --source .
                    ↓
Source code uploaded to Google Cloud Storage
                    ↓
Cloud Build builds Docker image
                    ↓
Artifact Registry stores the image
                    ↓
Cloud Run starts the container
                    ↓
Cloud Run gives a public HTTPS URL
                    ↓
User asks a question
                    ↓
Application calls OpenAI API
                    ↓
AI response displayed in Streamlit UI
```

The IAM error you encountered happened specifically at this stage:

```text
Source Upload
     ↓
Cloud Storage
     ❌ Permission denied
     ↓
storage.objects.get
```

Granting the required service account access allows the deployment pipeline to continue.
