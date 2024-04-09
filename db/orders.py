import sqlalchemy as sa
import typing as t

from datetime import datetime


from db.base import METADATA, begin_connection
from config import config


class OrderRow(t.Protocol):
    id: int
    created_at: datetime
    chat_id: int
    target: str
    title: str


OrderTable = sa.Table(
    'orders',
    METADATA,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('created_at', sa.DateTime),
    sa.Column('chat_id', sa.Integer),
    sa.Column('target', sa.String(255)),
    sa.Column('title', sa.String(255)),
)


# добавляет заказ
async def add_order(chat_id: int, target: str, title: str):
    async with begin_connection() as conn:
        await conn.execute(
            OrderTable.insert().values(
                created_at=datetime.now (config.tz).replace(microsecond=0),
                chat_id=chat_id,
                target=target,
                title=title
            ))


# удаляет заказ
async def del_order(chat_id: int, target: str):
    async with begin_connection() as conn:
        await conn.execute(OrderTable.delete().where(
            OrderTable.c.chat_id == chat_id,
            OrderTable.c.target == target,
        ))


# возвращает список заказов
async def get_orders(chat_id: int = None) -> tuple[OrderRow]:
    query = OrderTable.select()

    if chat_id:
        query = query.where(OrderTable.c.chat_id == chat_id)

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()
