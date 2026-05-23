from datetime import datetime
import uuid
from sqlalchemy import Column, String, JSON, Float, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship
import enum

class Base(DeclarativeBase):
    pass

class AssessmentStatus(str, enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNCERTAIN = "UNCERTAIN"

class Trace(Base):
    __tablename__ = "traces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)

    input_payload = Column(JSON, nullable=False)
    output_payload = Column(JSON, nullable=True)

    metadata_info = Column(JSON, default={})
    latency_ms = Column(Float, nullable=True)

    critiques = relationship("Critique", back_populates="trace")
    guardrail_results = relationship("GuardrailResult", back_populates="trace")

class Critique(Base):
    __tablename__ = "critiques"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trace_id = Column(UUID(as_uuid=True), ForeignKey("traces.id"), nullable=False)
    expert_uid = Column(String, nullable=False)

    assessment = Column(Enum(AssessmentStatus), nullable=False)
    critique_text = Column(Text, nullable=False)

    metadata_info = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    trace = relationship("Trace", back_populates="critiques")

class Guardrail(Base):
    __tablename__ = "guardrails"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    type = Column(String, nullable=False) # e.g., 'regex', 'semantic', 'custom'
    config = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)

    results = relationship("GuardrailResult", back_populates="guardrail")

class GuardrailResult(Base):
    __tablename__ = "guardrail_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trace_id = Column(UUID(as_uuid=True), ForeignKey("traces.id"), nullable=False)
    guardrail_id = Column(UUID(as_uuid=True), ForeignKey("guardrails.id"), nullable=False)

    passed = Column(Boolean, nullable=False)
    score = Column(Float, nullable=True)
    details = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    trace = relationship("Trace", back_populates="guardrail_results")
    guardrail = relationship("Guardrail", back_populates="results")
