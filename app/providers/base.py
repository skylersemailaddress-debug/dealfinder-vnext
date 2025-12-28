from abc import ABC, abstractmethod
from app.models import ProviderResult

class Provider(ABC):
    name: str

    @abstractmethod
    def fetch(self, query: str, *, limit: int = 40, **kwargs) -> ProviderResult:
        raise NotImplementedError
