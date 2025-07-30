import io
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
import stlog

from stlog_fastapi_middlewares.access_log import AccessLogMiddleware


app = FastAPI()
logger = stlog.getLogger("test")
app.add_middleware(AccessLogMiddleware, logger=logger)
client = TestClient(app)


@app.get("/foo")
async def foo():
    return {"hello", "world"}


def test_access_log(log_output: io.StringIO):
    response = client.get("/foo")
    assert response.status_code == 200
    print(log_output.getvalue())
    decoded = json.loads(log_output.getvalue())
    assert decoded["full_path"] == "/foo"
    assert decoded["status_code"] == 200
    assert decoded["method"] == "GET"
    assert decoded["level"] == "INFO"
    assert decoded["message"] == "access log"
