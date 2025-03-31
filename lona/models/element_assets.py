from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ElementAsset(Base):
    __tablename__ = "element_assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    html_element = Column(String(255), nullable=False, unique=True)
    css_block = Column(Text, nullable=True)
    js_snippets = Column(Text, nullable=True)
    template_file = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
