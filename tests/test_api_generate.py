import sys
import types

# Stub external dependencies before importing the app and TestClient

httpx_stub = types.ModuleType("httpx")
class ByteStream:
    def __init__(self, content: bytes):
        import io
        self.buffer = io.BytesIO(content)
    def read(self) -> bytes:
        return self.buffer.read()
class URL:
    def __init__(self, url: str):
        from urllib.parse import urlsplit
        p = urlsplit(url)
        self.scheme = p.scheme or "http"
        self.netloc = p.netloc.encode()
        self.path = p.path
        self.raw_path = self.path.encode()
        self.query = p.query.encode()
    def join(self, other: str) -> "URL":
        from urllib.parse import urljoin
        return URL(urljoin(self.render(), other))
    def render(self) -> str:
        q = f"?{self.query.decode()}" if self.query else ""
        return f"{self.scheme}://{self.netloc.decode()}{self.path}{q}"
class Request:
    def __init__(self, method: str, url: str, headers=None, content=None):
        self.method = method
        self.url = URL(url)
        self.headers = headers or {}
        self._content = content
    def read(self):
        if self._content is None:
            return b""
        if isinstance(self._content, bytes):
            return self._content
        if isinstance(self._content, str):
            return self._content.encode()
        import json
        return json.dumps(self._content).encode()
class Response:
    def __init__(self, status_code: int, headers=None, stream=None, request=None):
        self.status_code = status_code
        self.headers = dict(headers or [])
        self.stream = ByteStream(stream or b"") if not isinstance(stream, ByteStream) else stream
        self.request = request
    def read(self):
        return self.stream.read()
    @property
    def text(self):
        return self.read().decode()
    def json(self):
        import json
        return json.loads(self.text or "null")
class BaseTransport:
    def handle_request(self, request: Request) -> Response:
        raise NotImplementedError
class Client:
    def __init__(self, *, app=None, base_url="", transport=None, headers=None, follow_redirects=True, cookies=None):
        self.transport = transport
        self.base_url = URL(base_url) if base_url else None
    def request(self, method: str, url: str | URL, **kwargs):
        if isinstance(url, URL):
            full_url = url.render()
        else:
            full_url = url
            if self.base_url is not None:
                full_url = self.base_url.join(full_url).render()
        req = Request(method, full_url, headers=kwargs.get("headers"), content=kwargs.get("content") or (kwargs.get("json")))
        return self.transport.handle_request(req)
    def get(self, url: str, **kwargs):
        return self.request("GET", url, **kwargs)
    def post(self, url: str, **kwargs):
        return self.request("POST", url, **kwargs)
httpx_stub.ByteStream = ByteStream
httpx_stub.URL = URL
httpx_stub.Request = Request
httpx_stub.Response = Response
httpx_stub.BaseTransport = BaseTransport
httpx_stub.Client = Client
httpx_stub._types = types.SimpleNamespace(URLTypes=str, RequestContent=bytes, RequestFiles=None, HeaderTypes=dict, CookieTypes=None, QueryParamTypes=None, AuthTypes=None)
class UseClientDefault: pass
httpx_stub._client = types.SimpleNamespace(USE_CLIENT_DEFAULT=UseClientDefault(), UseClientDefault=UseClientDefault, CookieTypes=None, TimeoutTypes=None)
sys.modules.setdefault("httpx", httpx_stub)

from fastapi.testclient import TestClient

# Stub external dependencies before importing the app
anthropic_stub = types.ModuleType("anthropic")
class Anthropic:
    def __init__(self, api_key: str):
        pass
    class messages:
        @staticmethod
        def create(**kwargs):
            class M:
                content = [type("obj", (), {"text": "dummy"})()]
            return M()
anthropic_stub.Anthropic = Anthropic
sys.modules.setdefault("anthropic", anthropic_stub)

google_pkg = types.ModuleType("google")
genai_stub = types.ModuleType("google.generativeai")
class GenerativeModel:
    def __init__(self, model: str):
        self.model = model
    def generate_content(self, prompts):
        class R:
            text = "dummy"
        return R()
def configure(api_key: str):
    pass
genai_stub.GenerativeModel = GenerativeModel
genai_stub.configure = configure
sys.modules.setdefault("google.generativeai", genai_stub)
google_pkg.generativeai = genai_stub
sys.modules.setdefault("google", google_pkg)

pandas_stub = types.ModuleType("pandas")
class DataFrame:
    pass
def read_csv(path):
    return DataFrame()
pandas_stub.DataFrame = DataFrame
pandas_stub.read_csv = read_csv
sys.modules.setdefault("pandas", pandas_stub)

from main import app
from core.llm_client_base import LLMClient


class DummyLLM(LLMClient):
    def chat(self, system_prompt: str, user_prompt: str):
        # Return predictable text so sections can be parsed
        response = (
            "Interpretation of Risk Factors: INT\n"
            "Recommended Examinations: EXAMS\n"
            "Recommended Management: MGMT\n"
            "Follow-up Plan: PLAN\n"
            "Summary: SUM")
        return response, {"tokens": 1}


client = TestClient(app)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_generate_endpoint(monkeypatch):
    def fake_create_llm(model: str):
        return DummyLLM()

    # Patch the factory used in the endpoint
    monkeypatch.setattr("api.generate.create_llm", fake_create_llm)

    payload = {
        "stay_id": 1,
        "predicted_risk": 0.2,
        "features": {"age": 40},
        "shap_values": {"age": 0.1}
    }
    res = client.post("/generate", json=payload)
    assert res.status_code == 200
    data = res.json()
    # basic field checks
    assert data["stay_id"] == 1
    assert set(data.keys()) == {
        "stay_id",
        "risk_group",
        "predicted_risk_percent",
        "interpretation",
        "examination",
        "management",
        "follow_up",
        "summary",
        "tokens_used",
    }


def test_evaluate_endpoint(monkeypatch):
    def fake_create_llm(model: str):
        return DummyLLM()

    monkeypatch.setattr("api.evaluate.create_llm", fake_create_llm)

    payload = {"report": "dummy"}
    res = client.post("/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "review_notes" in data


def test_generate_multi_agent_report(monkeypatch):
    def fake_create_llm(model: str):
        return DummyLLM()

    monkeypatch.setattr("router.multi_agent.create_llm", fake_create_llm)

    payload = {
        "stay_id": 1,
        "predicted_risk": 0.1,
        "shap_explanation": "text",
    }
    res = client.post("/generate_multi_agent_report", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["stay_id"] == 1
    assert set(data.keys()) == {
        "stay_id",
        "final_report",
        "review_notes",
        "writer_tokens",
        "reviewer_tokens",
        "editor_tokens",
    }
