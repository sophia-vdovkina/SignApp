from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from application.database import Base
import uuid


class Signature(Base):

    __tablename__ = "signature"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_path = Column(String(256), nullable=False)
    device_name = Column(String(128))
    capture_date_time = Column(DateTime())

    features = relationship("Feature", back_populates="signature")


class Feature(Base):

    __tablename__ = "feature"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    values = Column(ARRAY(Float), nullable=False)
    value_name = Column(String(32))
    index = Column(Integer())
    signature_id = Column(UUID, ForeignKey("signature.id"))
    
    signature = relationship("Signature", back_populates="features")