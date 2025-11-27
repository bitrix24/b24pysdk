import json
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import FileResponse, JSONResponse

from b24pysdk.bitrix_api.credentials import OAuthPlacementData

app = FastAPI()

_CURRENT_DIR_PATH: Path = Path(__file__).parent
_HTML_FILE_PATH: Path = _CURRENT_DIR_PATH / "index.html"
_OAUTH_FILE_PATH: Path = _CURRENT_DIR_PATH.parent / "oauth_data.json"


@app.post("/")
async def index(request: Request):
    try:
        form_data = await request.form()

        placement_data = {**form_data, **request.query_params}
        oauth_placement_data = OAuthPlacementData.from_dict(placement_data)

        with Path.open(_OAUTH_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(
                oauth_placement_data.oauth_token.to_dict(),
                file,
                ensure_ascii=False,
                indent=4,
                default=str,
            )

        return FileResponse(
            path=_HTML_FILE_PATH,
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
