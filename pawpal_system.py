from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    description: str
    pet_name: str
    time: str
    duration_minutes: int
    priority: str
    frequency: str
    due_date: date
    completed: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Owner:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner: Owner = owner

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        pass

    def filter_tasks(
        self,
        tasks: list[Task],
        pet_name: str | None = None,
        priority: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        pass

    def detect_conflicts(self, tasks: list[Task]) -> list[tuple]:
        pass

    def mark_task_complete(self, task: Task) -> None:
        pass
