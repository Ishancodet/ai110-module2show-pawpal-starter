from dataclasses import dataclass, field
from datetime import date, timedelta


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
        completed: bool | None = None,
    ) -> list[Task]:
        """Return tasks matching pet_name and/or completed status; both are optional."""
        result = []
        for task in self._tasks(tasks):
            if pet_name is not None and task.pet_name != pet_name:
                continue
            if completed is not None and task.completed != completed:
                continue
            result.append(task)
        return result

    def mark_task_complete(self, task: Task) -> None:
        """Mark the task complete and, if it repeats, add its next occurrence to the same pet."""
        task.mark_complete()
        days = {"daily": 1, "weekly": 7}.get(task.frequency)
        if days is None:
            return
        next_task = Task(
            task.description,
            task.pet_name,
            task.time,
            task.duration_minutes,
            task.priority,
            task.frequency,
            task.due_date + timedelta(days=days),
        )
        for pet in self.owner.pets:
            if pet.name == task.pet_name:
                pet.add_task(next_task)
                break

    def detect_conflicts(self, tasks: list[Task] | None = None) -> list[str]:
        """Return one warning per start time shared by 2+ tasks (identical 'HH:MM' only, not overlapping durations); never raises."""
        by_time: dict[str, list[Task]] = {}
        for task in self._tasks(tasks):
            by_time.setdefault(task.time, []).append(task)

        warnings: list[str] = []
        for time, group in by_time.items():
            if len(group) > 1:
                names = ", ".join(f"'{t.description}' ({t.pet_name})" for t in group)
                warnings.append(f"Conflict at {time}: {names}")
        return warnings
