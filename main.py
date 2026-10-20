from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Build sample data and print today's schedule."""
    owner = Owner("Ishan")
    biscuit = Pet("Biscuit", "dog")
    mochi = Pet("Mochi", "cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    today = date.today()
    biscuit.add_task(Task("Morning walk", "Biscuit", "08:00", 30, "high", "daily", today))
    biscuit.add_task(Task("Feeding", "Biscuit", "09:00", 10, "high", "daily", today))
    biscuit.add_task(Task("Grooming", "Biscuit", "17:30", 20, "low", "weekly", today))
    mochi.add_task(Task("Feeding", "Mochi", "07:30", 10, "high", "daily", today))
    mochi.add_task(Task("Play with feather toy", "Mochi", "19:00", 15, "medium", "daily", today))

    scheduler = Scheduler(owner)
    schedule = scheduler.sort_by_time()

    print(f"Today's Schedule for {owner.name} ({today.strftime('%A, %B %d, %Y')})")
    print("=" * 60)
    for task in schedule:
        status = "[x]" if task.completed else "[ ]"
        print(
            f"{status} {task.time}  {task.description:<22} "
            f"{task.pet_name:<8} {task.duration_minutes:>3} min  "
            f"priority: {task.priority}"
        )
    print("=" * 60)
    print(f"{len(schedule)} tasks scheduled.")


if __name__ == "__main__":
    main()
