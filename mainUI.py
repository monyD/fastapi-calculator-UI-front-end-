from fastapi import FastAPI, HTTPException, Request, Form
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title="FastAPI Calculator (with UI)")

# Serve the existing `static/` and `templates/` folders — no changes to your current main.py
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class CalcResult(BaseModel):
    result: float

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Render the server-side template located at templates/index.html."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def index_post(request: Request, a: str = Form(...), b: str = Form(...), op: str = Form(...)):
    """Handle form submissions from templates/index.html and return the rendered template with result."""
    # parse inputs
    try:
        a_val = float(a)
        b_val = float(b)
    except ValueError:
        return templates.TemplateResponse("index.html", {"request": request, "result": "Invalid input"})

    # perform operation
    op = (op or "").lower()
    if op == "add":
        res = a_val + b_val
    elif op == "sub":
        res = a_val - b_val
    elif op == "mul":
        res = a_val * b_val
    elif op == "div":
        if b_val == 0:
            return templates.TemplateResponse("index.html", {"request": request, "result": "Cannot divide by zero"})
        res = a_val / b_val
    else:
        return templates.TemplateResponse("index.html", {"request": request, "result": "Unknown operation"})

    return templates.TemplateResponse("index.html", {"request": request, "result": res})

@app.get("/api/add", response_model=CalcResult)
def add(a: float, b: float):
    return {"result": a + b}

@app.get("/api/subtract", response_model=CalcResult)
def subtract(a: float, b: float):
    return {"result": a - b}

@app.get("/api/multiply", response_model=CalcResult)
def multiply(a: float, b: float):
    return {"result": a * b}

@app.get("/api/divide", response_model=CalcResult)
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": a / b}

# Optional consolidated endpoint
@app.get("/api/calculate", response_model=CalcResult)
def calculate(op: str, a: float, b: float):
    op = op.lower()
    if op in ("add", "+"):
        return {"result": a + b}
    if op in ("sub", "-", "subtract"):
        return {"result": a - b}
    if op in ("mul", "*", "multiply"):
        return {"result": a * b}
    if op in ("div", "/", "divide"):
        if b == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        return {"result": a / b}
    raise HTTPException(status_code=400, detail="Unknown operation")