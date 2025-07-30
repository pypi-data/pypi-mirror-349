from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict
from Osdental.Models.Legacy import Legacy
from Osdental.Shared.Utils.CaseConverter import CaseConverter
from Osdental.Exception.ControlledException import MissingFieldException

@dataclass
class AuthToken:
    token_id: str
    user_id: str
    external_enterprise_id: str
    profile_id: str
    legacy_id: str
    item_report_id: str
    enterprise_id: str
    authorization_id: str
    user_full_name: str
    abbreviation: str
    aes_key_auth: str
    jwt_user_key: Optional[str] = None
    legacy: Optional[Legacy] = None

    def __post_init__(self):
        required_fields = [
            'token_id', 'user_id', 'external_enterprise_id', 'profile_id',
            'legacy_id', 'item_report_id', 'enterprise_id', 'authorization_id',
            'user_full_name', 'abbreviation', 'aes_key_auth'
        ]

        missing = [f for f in required_fields if not getattr(self, f)]
        if missing:
            raise MissingFieldException(error=f'Missing required fields: {', '.join(missing)}')
        

    @classmethod
    def from_jwt(cls, payload: Dict[str,str], legacy: Legacy, jwt_user_key: str) -> AuthToken:
        mapped = {CaseConverter.case_to_snake(key): value for key, value in payload.items()}
        mapped['legacy'] = legacy
        mapped['jwt_user_key'] = jwt_user_key
        return cls(**mapped)