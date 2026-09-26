from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, ForeignKey, Table, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


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

# Load Data
def load_data(dataset: list):
    # Create Engine
    engine = create_engine("sqlite:///data/data.db")

    # Create Tables
    Base.metadata.create_all(engine)

    # Create Session
    with Session(engine) as session:
        for item in dataset:
            # Updates if exists
            existing_record = session.get(Record, item["id"])
            if existing_record:
                existing_record.number = item["number"]
                existing_record.title = item["title"]
                existing_record.author = item["author"]
                existing_record.closed_by = item["closed_by"]
                existing_record.thumbs_up = item["thumbs_up"]
                existing_record.state = item["state"]
                existing_record.body = item["body"]
                existing_record.created_at = item["created_at"]
                existing_record.closed_at = item["closed_at"]
                existing_record.updated_at = item["updated_at"]
                existing_record.merged_at = item["merged_at"]
                existing_record.draft = item["draft"]
                existing_record.head_branch = item["head_branch"]
                existing_record.base_branch = item["base_branch"]
                existing_record.lead_time_days = item["lead_time_days"]
                existing_record.is_stale = item["is_stale"]
                existing_record.entity_type = item["entity_type"]

            # Inserts if new
            else:
                add_issue = Record(
                    id=item["id"],
                    number=item["number"],
                    title=item["title"],
                    author=item["author"],
                    closed_by=item["closed_by"],
                    thumbs_up=item["thumbs_up"],
                    state=item["state"],
                    body=item["body"],
                    created_at=item["created_at"],
                    closed_at=item["closed_at"],
                    updated_at=item["updated_at"],
                    merged_at=item["merged_at"],
                    draft=item["draft"],
                    head_branch=item["head_branch"],
                    base_branch=item["base_branch"],
                    lead_time_days=item["lead_time_days"],
                    is_stale=item["is_stale"],
                    entity_type=item["entity_type"]
                )

                session.add(add_issue)
                existing_record = add_issue

            # Add Labels
            for l in item["labels"]:
                stmt = select(Label).where(Label.name == l)
                label = session.scalars(stmt).first()

                if label is None:
                    label_obj = Label(name=l)
                    existing_record.labels.append(label_obj)

                else:
                    existing_record.labels.append(label)

        # Commit session
        session.commit()