# __init__.py
import time
import requests
from pydantic import BaseModel
from typing import Optional


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthClient:
    def __init__(self, client_id: str, client_secret: str, base_url: str = "http://localhost:8000"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url.rstrip("/")

        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[float] = None

        self.login()

    def login(self):
        url = f"{self.base_url}/api/auth/auth-token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Login failed: {response.status_code} - {response.text}")

        data = AuthResponse(**response.json())
        self.access_token = data.access_token
        self.refresh_token = data.refresh_token
        self.token_expiry = self._decode_expiry(self.access_token)

    def _decode_expiry(self, token: str) -> float:
        import jwt
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get("exp", 0) - 30

    def refresh(self):
        url = f"{self.base_url}/api/auth/refresh-token"
        payload = {"refresh_token": self.refresh_token}
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Token refresh failed: {response.status_code} - {response.text}")

        data = response.json()
        self.access_token = data["access_token"]
        self.token_expiry = self._decode_expiry(self.access_token)

    def get_token(self) -> str:
        if self.access_token is None or time.time() >= self.token_expiry:
            self.refresh()
        return self.access_token

    def get_auth_header(self) -> dict:
        return {"Authorization": f"Bearer {self.get_token()}"}
