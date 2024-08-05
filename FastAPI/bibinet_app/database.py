import asyncpg


async def get_database_connection():
    return await asyncpg.connect("postgresql://postgres:postgres@db/postgres")
