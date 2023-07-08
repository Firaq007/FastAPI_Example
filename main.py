from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the USB Video Streaming App!"}

@app.get("/stream_video")
async def stream_video():
    video = cv2.VideoCapture(0)

    def generate_frames():
        while True:
            success, frame = video.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
