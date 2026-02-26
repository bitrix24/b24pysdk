import json
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import FileResponse, JSONResponse

from b24pysdk.credentials import OAuthPlacementData
from tests.constants import OAUTH_DATA_FILE

app = FastAPI()


@app.post("/")
async def index(request: Request):
    try:
        form_data = await request.form()

        placement_data = {**form_data, **request.query_params}
        oauth_placement_data = OAuthPlacementData.from_dict(placement_data)
        oauth_file_path = Path(__file__).parent.parent.parent / OAUTH_DATA_FILE

        with Path(oauth_file_path).open("w", encoding="utf-8") as file:
            json.dump(
                oauth_placement_data.oauth_token.to_dict(),
                file,
                ensure_ascii=False,
                indent=4,
                default=str,
            )

        return FileResponse(
            path="index.html",
            media_type="text/html",
        )

    except OAuthPlacementData.ValidationError as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "error": str(error),
            },
        )


if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
        reload=True,
        log_level="info",
    )
