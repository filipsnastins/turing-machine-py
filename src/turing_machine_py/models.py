from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class State:
    name: str
    instructions: Optional[List[Instruction]] = None


@dataclass
class Instruction:
    meet: List[str]
    write: str
    move: Optional[str] = None
    set: Optional[str] = None
