from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import subprocess
import logging

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return JSONResponse(content={"message": "Welcome to AI Web Chat. Go to /static/index.html to chat."})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    
    if not user_message:
        return JSONResponse(content={"error": "No message provided"}, status_code=400)

    try:
        # Try to run with --resume latest and use Flash model
        cmd = ["gemini", user_message, "--resume", "latest", "--model", "gemini-2.5-flash"]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        # If it failed, it might be because there is no session to resume.
        # We can try again without --resume if the error suggests it (or just blindly retry for now if return code is non-zero and not a quota error).
        # However, distinguishing errors is tricky.
        # A simple heuristic: if stderr contains "session" and "not found" or similar, retry.
        # Or simpler: if it fails, try creating a new session.
        # But we don't want to retry if it's a quota error.
        
        if result.returncode != 0 and "quota" not in result.stderr.lower() and "exhausted" not in result.stderr.lower():
             logging.info("Failed to resume session, trying new session...")
             cmd = ["gemini", user_message, "--model", "gemini-2.5-flash"]
             result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

        response_text = result.stdout
        
        # Log stderr for debugging but don't send to user unless it's an error exit code
        if result.stderr:
            logging.info(f"Gemini CLI Stderr: {result.stderr}")
            
        if result.returncode != 0:
             response_text += f"\n[Error]: {result.stderr}"
             
        return JSONResponse(content={"response": response_text})

    except Exception as e:
        logging.error(f"Error executing copilot: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
