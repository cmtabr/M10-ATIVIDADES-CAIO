import base64
import io
import json

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from PIL import Image
from redis import Redis
from rembg import remove

from logs.logger import Logger
from helpers.decoder import decoder

redis = Redis(host="redis", port=6379, db=0, decode_responses=True)
logger = Logger(name="image_service").get_logger()

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

@app.post("/remove-bg", tags=["Image"], status_code=200)
async def remove_bg(image_request: ImageRequest, auth_id: str =  Header(...)):
    logger.info("Remove background request received")
    try:
        auth = json.loads(redis.get(auth_id))
        if not auth.get("access token"):
            logger.warning("Requisição feita com token inválido: %s", auth_id)
            return HTTPException(status_code=401, detail="Unauthorized request")
        base64_result = remove_background_from_base64(image_request.base64_image)
        return {"base64_image": base64_result}
    except Exception as e:
        logger.error("Error on image processing: %s", str(e))
        return HTTPException(status_code=500, detail=str(e))
