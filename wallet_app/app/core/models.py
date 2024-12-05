from dataclasses import dataclass
from enum import Enum
from typing import Optional

class OperationType(Enum):
    TRANSFER = "transfer"
    CREATE_ACCOUNT = "create_account"

@dataclass
class TransactionResult:
    success: bool
    message: str
    operation_type: Optional[OperationType] = None
    hash: Optional[str] = None

@dataclass
class TransactionData:
    source_secret: str
    destination_id: str
    amount: str
    operation_type: OperationType
    memo: Optional[str] = None
    asset_type: Optional[str] = None

class KeyType(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    INVALID = "invalid"

@dataclass
class KeyValidationResult:
    type: KeyType
    public_key: str = ""
    error_message: str = ""