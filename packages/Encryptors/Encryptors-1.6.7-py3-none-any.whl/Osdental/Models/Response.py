from dataclasses import dataclass, field, asdict

@dataclass
class Response:
    status: str
    message: str
    data: str = field(default=None)

    def to_dict(self):
        return asdict(self)
