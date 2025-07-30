from fastapi import APIRouter, Depends
from app.dependencies import get_db_hub
from app.db.database_hub import DatabaseHub

router = APIRouter()

@router.get("/test-postgres")
async def test_postgres(db: DatabaseHub = Depends(get_db_hub)):
    return await db.postgres_pool.fetchval("SELECT 'Hello from Postgres'")

@router.get("/test-redis")
async def test_redis(db: DatabaseHub = Depends(get_db_hub)):
    await db.redis_client.set("message", "Hello Redis")
    return await db.redis_client.get("message")

@router.get("/test-sqlite")
async def test_sqlite(db: DatabaseHub = Depends(get_db_hub)):
    await db.sqlite_conn.execute("CREATE TABLE IF NOT EXISTS hello (msg TEXT)")
    await db.sqlite_conn.execute("INSERT INTO hello (msg) VALUES ('Hi')")
    await db.sqlite_conn.commit()
    cursor = await db.sqlite_conn.execute("SELECT msg FROM hello")
    rows = await cursor.fetchall()
    return [row[0] for row in rows]
