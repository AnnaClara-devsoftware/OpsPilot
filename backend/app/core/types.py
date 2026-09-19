"""Cross-dialect column types.

Production runs on PostgreSQL (Neon), but the test suite runs against
in-memory SQLite for speed and zero external dependencies. These
TypeDecorators pick the native, efficient type on PostgreSQL (UUID, JSONB)
and fall back to a compatible representation (CHAR(36), TEXT-as-JSON) on
SQLite and other dialects, so the same models work unmodified in both.
"""
import json
import uuid

from sqlalchemy import CHAR, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.types import JSON as SA_JSON


class GUID(TypeDecorator):
    """Platform-independent UUID type."""

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "postgresql":
            return str(value)
        if not isinstance(value, uuid.UUID):
            return str(uuid.UUID(value))
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)


class JSONEncoded(TypeDecorator):
    """Platform-independent JSON/JSONB type."""

    impl = SA_JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        return dialect.type_descriptor(SA_JSON())

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "postgresql":
            return value
        return json.loads(json.dumps(value, default=str))

    def process_result_value(self, value, dialect):
        return value
