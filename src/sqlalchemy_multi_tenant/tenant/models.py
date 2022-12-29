from dataclasses import dataclass
from typing import Optional


@dataclass
class Tenant:
    name: str
    schema: str
    id: Optional[int] = None  # pylint: disable=invalid-name
