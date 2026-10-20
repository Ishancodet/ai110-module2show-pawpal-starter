from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title: str, tasks: list[Task]) -> None:
    """Print a titled list of tasks, one per line."""
    print(f"\n{title}")
    print("-" * 60)
    for task in tasks:
        status = "[x]" if task.completed else "[ ]"
        print(
            f"{status} {task.time}  {task.description:<22} "
            f"{task.pet_name:<8} {task.duration_minutes:>3} min  "
            f"{task.frequency:<7} due {task.due_date}"
        )
    print(f"({len(tasks)} tasks)")


def main() -> None:
    """Build sample data and demo sorting, filtering, recurrence, and conflicts."""
    owner = Owner("Ishan")
    biscuit = Pet("Biscuit", "dog")
    mochi = Pet("Mochi", "cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    today = date.today()
    # Tasks are added out of time order on purpose.
    biscuit.add_task(Task("Grooming", "Biscuit", "17:30", 20, "low", "weekly", today))
    mochi.add_task(Task("Play with feather toy", "Mochi", "19:00", 15, "medium", "daily", today))
    walk = Task("Morning walk", "Biscuit", "08:00", 30, "high", "daily", today)
    biscuit.add_task(walk)
    mochi.add_task(Task("Feeding", "Mochi", "07:30", 10, "high", "daily", today))
    biscuit.add_task(Task("Feeding", "Biscuit", "09:00", 10, "high", "daily", today))

    scheduler = Scheduler(owner)

    print(f"PawPal schedule for {owner.name} ({today.strftime('%A, %B %d, %Y')})")
    print_tasks("Tasks in the order they were added:", owner.get_all_tasks())
    print_tasks("Sorted by time:", scheduler.sort_by_time())

    print_tasks("Filtered: Mochi only", scheduler.filter_tasks(pet_name="Mochi"))

    scheduler.mark_task_complete(walk)
    print_tasks("Filtered: completed tasks", scheduler.filter_tasks(completed=True))
    print_tasks("Filtered: incomplete tasks", scheduler.filter_tasks(completed=False))

    print("\nAfter completing the daily 'Morning walk', Biscuit's tasks now include:")
    for task in biscuit.get_tasks():
        if task.description == "Morning walk":
            status = "done" if task.completed else "pending"
            print(f"  Morning walk due {task.due_date} ({status})")

    # Three tasks at 19:00 across both pets should produce ONE grouped warning.
    biscuit.add_task(Task("Vet visit", "Biscuit", "19:00", 45, "high", "once", today))
    mochi.add_task(Task("Brush fur", "Mochi", "19:00", 5, "low", "weekly", today))
    print("\nConflict check (identical start times only):")
    for warning in scheduler.detect_conflicts(scheduler.filter_tasks(completed=False)):
        print(f"  WARNING: {warning}")


if __name__ == "__main__":
    main()
