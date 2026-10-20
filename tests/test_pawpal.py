from datetime import date

from pawpal_system import Pet, Task


def make_task() -> Task:
    """Build a sample task for tests."""
    return Task("Morning walk", "Biscuit", "08:00", 30, "high", "daily", date.today())


def test_mark_complete_sets_completed_true():
    task = make_task()
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_task_count_by_one():
    pet = Pet("Biscuit", "dog")
    before = len(pet.get_tasks())

    pet.add_task(make_task())

    assert len(pet.get_tasks()) == before + 1
