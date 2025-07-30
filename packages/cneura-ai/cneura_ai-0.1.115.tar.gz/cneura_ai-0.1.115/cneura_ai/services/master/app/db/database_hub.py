import asyncpg
import motor.motor_asyncio
import redis.asyncio as redis
import aiosqlite
from chromadb import HttpClient as ChromaClient


class DatabaseHub:
    def __init__(self, config: dict):
        self.config = config
        self.postgres_pool = None
        self.mongo_client = None
        self.redis_client = None
        self.chroma_client = None
        self.sqlite_conn = None

    async def connect(self):
        await self._connect_postgres()
        await self._connect_mongodb()
        await self._connect_redis()
        await self._connect_sqlite()
        self._connect_chromadb()

    async def disconnect(self):
        await self._disconnect_postgres()
        await self._disconnect_mongodb()
        await self._disconnect_redis()
        await self._disconnect_sqlite()

    # ---------------- PostgreSQL ----------------
    async def _connect_postgres(self):
        self.postgres_pool = await asyncpg.create_pool(
            user=self.config["POSTGRES_USER"],
            password=self.config["POSTGRES_PASSWORD"],
            database=self.config["POSTGRES_DB"],
            host=self.config["POSTGRES_HOST"],
            port=self.config["POSTGRES_PORT"],
        )

    async def _disconnect_postgres(self):
        if self.postgres_pool:
            await self.postgres_pool.close()

    # ---------------- MongoDB ----------------
    async def _connect_mongodb(self):
        uri = f"mongodb://{self.config['MONGO_USER']}:{self.config['MONGO_PASSWORD']}@{self.config['MONGO_HOST']}:{self.config['MONGO_PORT']}"
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(uri)

    async def _disconnect_mongodb(self):
        if self.mongo_client:
            self.mongo_client.close()

    # ---------------- Redis ----------------
    async def _connect_redis(self):
        self.redis_client = redis.Redis(
            host=self.config["REDIS_HOST"],
            port=self.config["REDIS_PORT"],
            password=self.config.get("REDIS_PASSWORD"),
            decode_responses=True
        )

    async def _disconnect_redis(self):
        if self.redis_client:
            await self.redis_client.close()

    # ---------------- SQLite ----------------
    async def _connect_sqlite(self):
        self.sqlite_conn = await aiosqlite.connect(self.config["SQLITE_PATH"])

    async def _disconnect_sqlite(self):
        if self.sqlite_conn:
            await self.sqlite_conn.close()

    # ---------------- ChromaDB ----------------
    def _connect_chromadb(self):
        self.chroma_client = ChromaClient(
            host=self.config["CHROMADB_HOST"],
            port=self.config["CHROMADB_PORT"],
            headers={
                "Authorization": f"Bearer {self.config['CHROMADB_API_KEY']}"
            }
        )
