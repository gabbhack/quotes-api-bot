from typing import List, Optional

from aiohttp import ClientSession
from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    telegram_id: int
    api_key: str


class Author(BaseModel):
    id: str
    name: str


class Quote(BaseModel):
    id: str
    text: str
    created_at: str
    author: Author


class Api:
    def __init__(self, host: str, key: str) -> None:
        self.host = host
        self.key = key
        self.headers = {"x-api-key": key, "Content-Type": "application/json"}
        self.session: Optional[ClientSession] = None

    def make_url(self, method: str) -> str:
        return f"https://{self.host}/{method}"

    async def create_session(self) -> ClientSession:
        if self.session is None or self.session.closed:
            self.session = ClientSession()
        return self.session

    async def create_user(self, name: str, telegram_id: int) -> User:
        session = await self.create_session()
        request = {"name": name, "telegram_id": telegram_id}

        async with session.post(
            self.make_url("internal/users/"), json=request, headers=self.headers
        ) as resp:
            return User(**await resp.json())

    async def get_user(self, telegram_id: int) -> User:
        session = await self.create_session()

        async with session.get(
            self.make_url(f"internal/users/{telegram_id}/"), headers=self.headers
        ) as resp:
            json = await resp.json()
            return User(**json)

    async def update_user(self, name: str, telegram_id: int) -> User:
        session = await self.create_session()
        request = {"name": name, "telegram_id": telegram_id}

        async with session.put(
            self.make_url(f"internal/users/{telegram_id}"),
            json=request,
            headers=self.headers,
        ) as resp:
            return User(**await resp.json())

    async def delete_user(self, telegram_id: int) -> True:
        session = await self.create_session()

        async with session.delete(
            self.make_url(f"internal/users/{telegram_id}/"), headers=self.headers
        ):
            return True

    async def revoke_api_key(self, telegram_id: int) -> User:
        session = await self.create_session()

        async with session.post(
            self.make_url(f"internal/users/{telegram_id}/revoke-api-key/"),
            headers=self.headers,
        ) as resp:
            return User(**await resp.json())

    async def quotes(self, offset: int = 0, limit: int = 10) -> List[Quote]:
        session = await self.create_session()
        params = {"offset": offset, "limit": limit}

        async with session.get(
            self.make_url(f"quotes/"), params=params, headers=self.headers
        ) as resp:
            quotes_raw = await resp.json()

            return [Quote(**quote) for quote in quotes_raw]
    
    async def add_quote(self, text: str, key: str) -> Quote:
        session = await self.create_session()

        request = {"text": text}
        headers = {**self.headers}
        headers["x-api-key"] = key

        async with session.post(self.make_url("quotes/"), json=request, headers=headers) as resp:
            return Quote(** await resp.json())
