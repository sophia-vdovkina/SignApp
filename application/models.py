from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql.elements import ColumnElement
from application.database import Base
from dataclasses import dataclass
from typing import List
import uuid

class ReferenceParams(Base):

    __tablename__ = "reference_parameters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id"))
    min_value = Column(Float(), nullable=True)
    max_value = Column(Float(), nullable=True)
    mean_value = Column(Float(), nullable=True)

    person = relationship("Person", back_populates="params")

class SecuritySettings(Base):

    __tablename__ = "security_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id"))
    threshold = Column(Float(), default=0.75)
    attempts_num = Column(Integer(), default=3)

    person = relationship("Person", back_populates="security")

class Info(Base):

    __tablename__ = "info"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id"))
    organization = Column(String(255), nullable=True) 
    registration_date = Column(DateTime, default=func.now())
    comment = Column(String(255), nullable=True) 

    person = relationship("Person", back_populates="info")

class SignatureSet(Base):

    __tablename__ = "signature_set"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id"))
    isActive = Column(Boolean, nullable=False)

    signature = relationship("Signature", back_populates="signature_set")
    person = relationship("Person", back_populates="signature_sets")


class Signature(Base):

    __tablename__ = "signature"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    set_id = Column(UUID(as_uuid=True), ForeignKey("signature_set.id"), nullable=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("device.id"))
    file_path = Column(String(255), nullable=True)
    num_in_file = Column(Integer, nullable=True)
    capture_date_time = Column(DateTime(), default=func.now())

    features = relationship("Feature", back_populates="signature")
    signature_set = relationship("SignatureSet", back_populates="signature")
    device = relationship("Device", back_populates="signature")
    login_attempts = relationship("LoginAttempts", back_populates="signature")
    identification_attempts = relationship("IdentificationAttempts", back_populates="signature")

class Device(Base):

    __tablename__ = "device"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    has_pressure = Column(Boolean, nullable=False)

    signature = relationship("Signature", back_populates="device")


@dataclass
class Feature(Base):
    id: int
    values: List[int]

    __tablename__ = "feature"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signature_id = Column(UUID(as_uuid=True), ForeignKey("signature.id"))
    values = Column(ARRAY(Float), nullable=False)
    name = Column(String(32))
    index = Column(Integer())
    
    signature = relationship("Signature", back_populates="features")
    
    
class Person(Base):

    __tablename__ = "person"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    second_name = Column(String(64), nullable=True)
    passport = Column(String(10), unique=True, nullable=False)

    signature_sets = relationship("SignatureSet", back_populates="person")
    params = relationship("ReferenceParams", back_populates="person")
    security = relationship("SecuritySettings", back_populates="person")
    info = relationship("Info", back_populates="person")
    login_attempts = relationship("LoginAttempts", back_populates="person")
    identification_attempts = relationship("IdentificationAttempts", back_populates="person")


class LoginAttempts(Base):

    __tablename__ = "login_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id"))
    signature_id = Column(UUID(as_uuid=True), ForeignKey("signature.id"))
    date_time = Column(DateTime(), default=func.now())

    person = relationship("Person", back_populates="login_attempts")
    signature = relationship("Signature", back_populates="login_attempts")

class IdentificationAttempts(Base):

    __tablename__ = "identification_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id"))
    signature_id = Column(UUID(as_uuid=True), ForeignKey("signature.id"))
    date_time = Column(DateTime(), default=func.now())
    confidence_value = Column(Float, nullable=True)

    person = relationship("Person", back_populates="identification_attempts")
    signature = relationship("Signature", back_populates="identification_attempts")


