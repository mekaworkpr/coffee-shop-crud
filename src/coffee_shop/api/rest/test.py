from fastapi import APIRouter

test_router = APIRouter()

@test_router.get('/')
def test_router_endpoint():
    return {"message": "Hello, world!"}