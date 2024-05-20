import base64
import io
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
from rembg import remove
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

class ImageRequest(BaseModel):
    base64_image: str

def remove_background_from_base64(base64_image: str) -> str:
    try:
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))

        result_image = remove(image)

        buffered = io.BytesIO()
        result_image.save(buffered, format="PNG")
        base64_output_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return base64_output_image
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/remove-bg")
async def remove_bg(image_request: ImageRequest):
    try:
        base64_result = remove_background_from_base64(image_request.base64_image)
        return {"base64_image": base64_result}
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
