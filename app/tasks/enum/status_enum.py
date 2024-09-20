from enum import Enum
from typing import List, Tuple


class StatusEnum(Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(key.value, key.name.replace("_", " ").title()) for key in cls]
