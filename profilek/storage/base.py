from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def save_profile_results(self) -> None:
        ...
