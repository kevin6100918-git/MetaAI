import pytest
from httpx import AsyncClient
import json
import asyncio
import logging
from os import getenv


logger = logging.getLogger(__name__)

testEndPoint = getenv("TEST_ENDPOINT", "http://localhost:8000")
testEvent = json.load(open("./test/events/prompt.json", "r", encoding="utf-8"))

@pytest.mark.asyncio
async def test_create_one_session():
    async with AsyncClient(base_url=testEndPoint) as client:
        response = await client.get("/session/create", timeout=120)
        responseData:dict = response.json()
    sessionID = responseData.get("result").get("sessionID")
    print("create_one_session", sessionID)
    assert response.status_code == 200
    assert responseData.get("code") == "OK000"
    assert responseData.get("detail") == ""
    assert sessionID is not None

# test asynchronous multiple session creation
@pytest.mark.asyncio
async def test_create_multiple_sessions():
    async with AsyncClient(base_url=testEndPoint) as client:
        tasks = []
        for _ in range(10):
            tasks.append(client.get("/session/create"))
        responses = await asyncio.gather(*tasks)
        sessionIDs = []
        for response in responses:
            responseData:dict = response.json()
            sessionID = responseData.get("result").get("sessionID")
            print("create_multiple_sessions responseData", responseData)
            assert response.status_code == 200
            assert responseData.get("code") == "OK000"
            assert responseData.get("detail") == ""
            assert sessionID is not None
            assert sessionID not in sessionIDs
            sessionIDs.append(sessionID)
