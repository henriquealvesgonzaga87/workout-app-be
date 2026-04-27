from abc import ABC, abstractmethod

from app.domain.training_type.entities import TrainingTypes


class TrainingTypeInterface(ABC):
    @abstractmethod
    def create(self, training_type: TrainingTypes) -> TrainingTypes:
        pass
