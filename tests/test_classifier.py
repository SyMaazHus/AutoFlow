import requests
import classifier

class FakeResp:
    """Stands in for the object requests.post returns."""
    def __init__(self, payload=None, status=200):
        self._payload, self.status_code = payload, status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"{self.status_code}")
    def json(self):
        return self._payload

def groq_reply(content: str):
    # the same nesting as the real response: choices[0].message.content
    return FakeResp({"choices": [{"message": {"content": content}}]})

def test_empty_inputs_return_empty_dict():
    assert classifier.groq_folder_match([], ["ML"]) == {}
    assert classifier.groq_folder_match(["a.pdf"], []) == {}

def test_valid_match(monkeypatch):
    monkeypatch.setattr(classifier, "GROQ_KEY", "fake")
    monkeypatch.setattr(classifier.requests, "post",
        lambda *a, **k: groq_reply('{"matches": {"nn.pdf": "ML", "holiday.png": null}}'))
    out = classifier.groq_folder_match(["nn.pdf", "holiday.png"], ["ML", "Lectures"])
    assert out == {"nn.pdf": "ML", "holiday.png": None}

def test_hallucinated_folder_is_rejected(monkeypatch):
    monkeypatch.setattr(classifier, "GROQ_KEY", "fake")
    monkeypatch.setattr(classifier.requests, "post",
        lambda *a, **k: groq_reply('{"matches": {"nn.pdf": "Machine Learning"}}'))
    assert classifier.groq_folder_match(["nn.pdf"], ["ML"]) == {"nn.pdf": None}