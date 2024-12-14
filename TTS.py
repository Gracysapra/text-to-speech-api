from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from gtts import gTTS
from fastapi.responses import FileResponse
import os
import uuid

app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    language: str = "en" 

# Cleanup function to delete the file after it is used
def cleanup_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)

@app.post("/text-to-speech/")
async def text_to_speech(request: TTSRequest, background_tasks: BackgroundTasks):
    try:
        # Generate a unique filename for the output audio file
        file_name = f"audio_{uuid.uuid4().hex}.mp3"
        output_file_path = os.path.join("temp_files", file_name)

        # Ensure the output directory exists
        os.makedirs("temp_files", exist_ok=True)

        # Generate the audio file using gTTS
        tts = gTTS(text=request.text, lang=request.language)
        tts.save(output_file_path)

        # Return the file as a response
        return FileResponse(output_file_path, media_type="audio/mpeg", filename=file_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")

# Run FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
