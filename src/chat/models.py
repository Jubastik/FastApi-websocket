from sqlalchemy import Column, Integer, String

from src.db_session import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    message = Column(String)

    def __repr__(self):
        return f"<Message(id={self.id}, message={self.message})>"
