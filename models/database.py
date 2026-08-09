from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Select
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated, Optional
from datetime import datetime
from sqlalchemy import String, Text, Float, Integer, JSON, func

engine = create_async_engine("sqlite+aiosqlite:///logs.db")

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)

app = FastAPI()


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        return {"status": "ok"}


class BookAddSchema(BaseModel):
    title: str
    author: str


@app.post("/books")
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(title=data.title, author=data.author)
    session.add(new_book)
    await session.commit()
    return {"status": "ok"}

@app.get("/books")
async def get_books(session:SessionDep):
    query = Select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()



class RequestLog(Base):
    __tablename__ = "request_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        comment="Время поступления запроса"
    )
    method: Mapped[str] = mapped_column(String(10), comment="HTTP метод (GET, POST...)")
    path: Mapped[str] = mapped_column(String(255), comment="Путь запроса")
    headers: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, comment="Заголовки запроса")
    status_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="HTTP статус ответа")
    process_time: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Время выполнения в секундах")
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="Текст ошибки, если возникла")

    def __repr__(self) -> str:
        return f"<RequestLog(id={self.id}, method={self.method}, path={self.path})>"