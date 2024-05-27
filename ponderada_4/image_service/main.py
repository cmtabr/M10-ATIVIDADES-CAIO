import base64
import io
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
from rembg import remove

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class ImageRequest(BaseModel):
    base64_image: str

def remove_background_from_base64(base64_image: str) -> str:
    try:
        logger.info("Starting background removal process")
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))

        logger.info("Image successfully decoded and opened")
        result_image = remove(image)
        logger.info("Background successfully removed")

        buffered = io.BytesIO()
        result_image.save(buffered, format="PNG")
        base64_output_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        logger.info("Resulting image successfully encoded to base64")

        return base64_output_image
    except Exception as e:
        logger.error("Exception during background removal: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/remove-bg")
async def remove_bg(image_request: ImageRequest):
    logger.info("Remove background request received")
    try:
        base64_result = remove_background_from_base64(image_request.base64_image)
        return {"base64_image": base64_result}
    except Exception as e:
        logger.error("Error on image processing: %s", str(e))
        return HTTPException(status_code=500, detail=str(e))
