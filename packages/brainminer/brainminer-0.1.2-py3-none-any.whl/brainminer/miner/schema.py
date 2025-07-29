from datetime import datetime

from sqlalchemy import String, DateTime, Double
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional

class Base(DeclarativeBase):
    pass

class AlphaTasks(Base):
    __tablename__ = 'alpha_tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    expression: Mapped[str] = mapped_column(String(8192), nullable=False)
    settings: Mapped[str] = mapped_column(String, nullable=False)
    batch_name: Mapped[str] = mapped_column(String, nullable=False)
    task_status: Mapped[str] = mapped_column(String, nullable=False)
    simulation_id: Mapped[str] = mapped_column(String, nullable=False)
    alpha_id: Mapped[Optional[str]] = mapped_column(String)
    submit_status: Mapped[Optional[str]] = mapped_column(String)
    alpha_result: Mapped[Optional[str]] = mapped_column(String)
    is_sharp: Mapped[Optional[float]] = mapped_column(Double)
    is_returns: Mapped[Optional[float]] = mapped_column(Double)
    is_turnover: Mapped[Optional[float]] = mapped_column(Double)
    is_fitness: Mapped[Optional[float]] = mapped_column(Double)
    is_drawdown: Mapped[Optional[float]] = mapped_column(Double)
    os_sharp: Mapped[Optional[float]] = mapped_column(Double)
    os_returns: Mapped[Optional[float]] = mapped_column(Double)
    os_turnover: Mapped[Optional[float]] = mapped_column(Double)
    os_fitness: Mapped[Optional[float]] = mapped_column(Double)
    os_drawdown: Mapped[Optional[float]] = mapped_column(Double)
    evaluation_level: Mapped[Optional[str]] = mapped_column(String)