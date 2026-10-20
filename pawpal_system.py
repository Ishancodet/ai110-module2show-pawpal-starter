from dataclasses import dataclass, field
from datetime import date


def _to_minutes(time_str: str) -> int:
    """Convert an 'HH:MM' string into minutes since midnight."""
    hours, minutes = time_str.split(":")
    return int(hours) * 60 + int(minutes)


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
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's task list."""
        return self.tasks


class Owner:
    def __init__(self, name: str) -> None:
        """Create an owner with a name and no pets yet."""
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return the tasks of every pet combined into one list."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Create a scheduler that reads tasks from the given owner."""
        self.owner: Owner = owner

    def _tasks(self, tasks: list[Task] | None) -> list[Task]:
        """Return the given tasks, or every task from the owner if none given."""
        return tasks if tasks is not None else self.owner.get_all_tasks()

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Return the tasks sorted by their 'HH:MM' time."""
        return sorted(self._tasks(tasks), key=lambda t: _to_minutes(t.time))

    def filter_tasks(
        self,
        tasks: list[Task] | None = None,
        pet_name: str | None = None,
        priority: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Return tasks matching every filter that is not None."""
        result = []
        for task in self._tasks(tasks):
            if pet_name is not None and task.pet_name != pet_name:
                continue
            if priority is not None and task.priority != priority:
                continue
            if completed is not None and task.completed != completed:
                continue
            result.append(task)
        return result

    def detect_conflicts(self, tasks: list[Task] | None = None) -> list[tuple]:
        """Return (task_a, task_b) pairs for the same pet whose time slots overlap."""
        ordered = self.sort_by_time(tasks)
        conflicts = []
        for i, first in enumerate(ordered):
            first_end = _to_minutes(first.time) + first.duration_minutes
            for second in ordered[i + 1:]:
                if second.pet_name != first.pet_name:
                    continue
                if _to_minutes(second.time) < first_end:
                    conflicts.append((first, second))
        return conflicts

    def mark_task_complete(self, task: Task) -> None:
        """Mark the given task as completed."""
        task.mark_complete()
