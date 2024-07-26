from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.responses import Response
from database.mixed import MixImage
from database.schemas import SImage

app = FastAPI()


@app.get(
    "/get_random_picture",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def get_random_picture():
    image_db = await MixImage.get_random()

    return Response(content=image_db.image, media_type="image/png")


@app.post("/upload_picture")
async def upload_picture(picture: UploadFile = File(...)):
    await MixImage.save(data=SImage(image=picture.file.read()))

    return {"status": "ok"}
