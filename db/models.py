from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    username: Mapped[str | None] = mapped_column(String(32), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    registrations: Mapped[list["Registration"]] = relationship(back_populates="user")

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(1024))
    date: Mapped[DateTime] = mapped_column(DateTime)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    adress: Mapped[str] = mapped_column(String(100), default="Nobe")

    registrations: Mapped[list["Registration"]] = relationship(back_populates="event")

class Registration(Base):
    __tablename__ = "registrations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    username: Mapped[str | None] = mapped_column(String(32), nullable=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    
    is_waitlist: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=None) 
    attended: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=None) 
    registered_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())


    user: Mapped["User"] = relationship(back_populates="registrations")
    event: Mapped["Event"] = relationship(back_populates="registrations")

class Moderator(Base):
    __tablename__ = "moderators"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    added_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship()

class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question: Mapped[str] = mapped_column(String(2048))
    answer: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    is_answered: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship()