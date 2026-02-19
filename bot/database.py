import asyncpg


async def create_pool(database_url: str) -> asyncpg.Pool:
    return await asyncpg.create_pool(database_url)


async def create_tables(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS ideas (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                raw_text TEXT NOT NULL,
                source_type VARCHAR(10) NOT NULL DEFAULT 'text',
                created_at TIMESTAMPTZ DEFAULT now()
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS morning_logs (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                date DATE NOT NULL,
                summary TEXT,
                ideas_count INT DEFAULT 0,
                sent_at TIMESTAMPTZ
            )
        """)
