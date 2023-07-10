from fastapi import APIRouter, Depends, HTTPException, Query, status

router = APIRouter()


@router.get("/",status_code=status.HTTP_200_OK)
def main():
    return {
      "status_code": 200,
      "detail": "ok",
      "result": "working"
    }