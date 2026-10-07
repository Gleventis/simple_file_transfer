from fastapi import APIRouter, Response, status
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/generic")


@router.get("/healthcheck")
def healthcheck():
    return Response(status_code=status.HTTP_200_OK)
