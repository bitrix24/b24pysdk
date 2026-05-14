import json
from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse

from b24pysdk.credentials import OAuthPlacementData
from b24pysdk.integrations.fastapi.dependencies import placement_dependency
from tests.constants import OAUTH_DATA_FILE

app = FastAPI()

_BASE_DIR: Path = Path(__file__).resolve().parent
_HTML_FILE: Path = _BASE_DIR / "index.html"
_OAUTH_FILE: Path = _BASE_DIR.parent.parent / OAUTH_DATA_FILE


@app.post("/")
async def index(oauth_placement_data: Annotated[OAuthPlacementData, Depends(placement_dependency)]):
    with _OAUTH_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            oauth_placement_data.oauth_token.to_dict(),
            file,
            ensure_ascii=False,
            indent=4,
            default=str,
        )

    return FileResponse(
        path=_HTML_FILE,
        media_type="text/html",
    )


if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
        reload=True,
        log_level="info",
    )
