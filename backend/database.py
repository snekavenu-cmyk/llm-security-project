import os
import hashlib
import secrets

from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean
)
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

load_dotenv()


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "llm_security.db"
)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


# ============================================================
# API KEY TABLE
# ============================================================

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    key_hash = Column(
        String(64),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(100),
        nullable=False,
        default="Default API Key"
    )

    active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# ATTACK LOG TABLE
# ============================================================

class AttackLog(Base):
    __tablename__ = "attack_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    attack_type = Column(
        String(100),
        nullable=False
    )

    payload = Column(
        Text,
        nullable=False
    )

    defense_logs = Column(
        Text,
        nullable=True
    )

    detection_score = Column(
        Integer,
        default=0
    )

    defense_triggered = Column(
        Boolean,
        default=False
    )

    latency = Column(
        String(50),
        nullable=True
    )

    username = Column(
        String(100),
        default="Admin"
    )

    role = Column(
        String(100),
        default="Tester"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# API KEY HELPER FUNCTIONS
# ============================================================

def hash_api_key(api_key: str) -> str:
    """
    Convert an API key into a SHA-256 hash.
    """

    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()


def generate_api_key() -> str:
    """
    Generate a secure random API key.
    """

    return secrets.token_urlsafe(32)


def create_api_key(
    name: str = "Default API Key"
) -> tuple[str, APIKey]:
    """
    Create a new API key.

    Returns:
        raw_api_key
        database_record
    """

    raw_api_key = generate_api_key()

    key_hash = hash_api_key(
        raw_api_key
    )

    db = SessionLocal()

    try:

        existing = db.query(APIKey).filter(
            APIKey.key_hash == key_hash
        ).first()

        if existing:
            return raw_api_key, existing

        new_key = APIKey(
            key_hash=key_hash,
            name=name,
            active=True
        )

        db.add(new_key)
        db.commit()
        db.refresh(new_key)

        return raw_api_key, new_key

    finally:

        db.close()


def verify_api_key(
    api_key: str
) -> bool:
    """
    Verify whether an API key exists
    and is active.
    """

    key_hash = hash_api_key(
        api_key
    )

    db = SessionLocal()

    try:

        record = db.query(APIKey).filter(
            APIKey.key_hash == key_hash,
            APIKey.active == True
        ).first()

        return record is not None

    finally:

        db.close()


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================
#
# The previous version of the project used:
#
#     from database import API_KEYS
#
# We keep API_KEYS here so older modules do not immediately
# break while we rebuild the project.
#
# ============================================================

API_KEYS = set()


def load_api_keys():
    """
    Load active API-key hashes from the database.
    """

    global API_KEYS

    db = SessionLocal()

    try:

        records = db.query(APIKey).filter(
            APIKey.active == True
        ).all()

        API_KEYS = {
            record.key_hash
            for record in records
        }

    finally:

        db.close()


# Load existing API keys when this module starts.
load_api_keys()


# ============================================================
# DATABASE SESSION HELPER
# ============================================================

def get_db():
    """
    Provide a database session.
    """

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()