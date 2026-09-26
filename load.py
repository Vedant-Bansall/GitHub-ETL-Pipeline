from __future__ import annotations

import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Load values
load_dotenv()

# Get params, Not permanent
pat_key = os.getenv("GITHUB_TOKEN")
owner = "pallets"
repo = "flask"
username = "Vedant-Bansall"
target_date_str = "2026-09-01T00:00:00Z"
target_dt = datetime.fromisoformat(target_date_str.replace("Z", "+00:00"))

# Base class
class Base(DeclarativeBase):
    pass

# Association Table
association_table = Table(
    "association_table",
    Base.metadata,
    Column("record_id", ForeignKey("record.id")),
    Column("label_id", ForeignKey("label.id"))
)

# ORM Table
class Record(Base):
    __tablename__ = "record"

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column()
    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    closed_by: Mapped[str | None] = mapped_column()
    thumbs_up: Mapped[int] = mapped_column()
    state: Mapped[str] = mapped_column()
    body: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime | None] = mapped_column()
    closed_at: Mapped[datetime | None] = mapped_column()
    updated_at: Mapped[datetime | None] = mapped_column()
    merged_at: Mapped[datetime | None] = mapped_column()
    draft: Mapped[bool] = mapped_column()
    head_branch: Mapped[str | None] = mapped_column()
    base_branch: Mapped[str | None] = mapped_column()
    lead_time_days: Mapped[float | None] = mapped_column()
    is_stale: Mapped[bool] = mapped_column()
    labels: Mapped[list[Label]] = relationship(secondary=association_table)
    entity_type: Mapped[str] = mapped_column()

# Label Table
class Label(Base):
    __tablename__ = "label"

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

def load_data(data_structure: list):
    pass
