from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from ..config.database import metadata, base, engine

class TodoTable(base):
    __tablename__ = 'todo'
    metadata
    todoId = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)
    userId = mapped_column(Integer, ForeignKey('user.userId'))

    def __init__(self, task, description, status, priority):
        self.task = task
        self.description = description
        self.status = status
        self.priority = priority

    def __repr__(self):
        return f"<TodoTable(task={self.task}, \r\n description={self.description}, \r\n status={self.status}, \r\n priority={self.priority})>"