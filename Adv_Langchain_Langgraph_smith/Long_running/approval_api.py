from fastapi import FastAPI
from db import init,set_value,get_value

init()
app=FastAPI(title="Approval API")

@app.get("/")
def home():
    return {"approval":get_value("approval")}

@app.get("/approve")
def approve():
    set_value("approval","approved")
    return {"message":"Workflow Approved"}

@app.get("/reject")
def reject():
    set_value("approval","rejected")
    return {"message":"Workflow Rejected"}
