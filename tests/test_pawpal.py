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


# ---------------------------------------------------------------------------
# Helpers for scheduler tests
# ---------------------------------------------------------------------------

from datetime import timedelta

from pawpal_system import Owner, Scheduler


def task_at(
    time: str,
    pet_name: str = "Biscuit",
    description: str | None = None,
    frequency: str = "once",
    due_date: date | None = None,
) -> Task:
    """Build a task at a given time with sensible defaults."""
    return Task(
        description or f"Task at {time}",
        pet_name,
        time,
        15,
        "medium",
        frequency,
        due_date or date(2026, 10, 20),
    )


def make_owner_with_pet(pet_name: str = "Biscuit") -> tuple[Owner, Pet, Scheduler]:
    """Build an owner with a single pet and a scheduler bound to that owner."""
    owner = Owner("Ishan")
    pet = Pet(pet_name, "dog")
    owner.add_pet(pet)
    return owner, pet, Scheduler(owner)


# ---------------------------------------------------------------------------
# sort_by_time
# ---------------------------------------------------------------------------

def test_sort_by_time_orders_tasks_added_out_of_order():
    owner, pet, scheduler = make_owner_with_pet()
    pet.add_task(task_at("18:30"))
    pet.add_task(task_at("07:15"))
    pet.add_task(task_at("12:00"))
    pet.add_task(task_at("09:45"))

    ordered = scheduler.sort_by_time()

    assert [t.time for t in ordered] == ["07:15", "09:45", "12:00", "18:30"]


def test_sort_by_time_compares_numerically_not_lexically():
    # "9:00" would sort after "10:00" as a plain string; numeric sort puts it first.
    owner, pet, scheduler = make_owner_with_pet()
    pet.add_task(task_at("10:00"))
    pet.add_task(task_at("9:00"))

    ordered = scheduler.sort_by_time()

    assert [t.time for t in ordered] == ["9:00", "10:00"]


def test_sort_by_time_does_not_mutate_original_list():
    owner, pet, scheduler = make_owner_with_pet()
    pet.add_task(task_at("18:30"))
    pet.add_task(task_at("07:15"))

    scheduler.sort_by_time()

    assert [t.time for t in pet.get_tasks()] == ["18:30", "07:15"]


# ---------------------------------------------------------------------------
# Recurring tasks
# ---------------------------------------------------------------------------

def test_completing_daily_task_creates_next_day_task():
    owner, pet, scheduler = make_owner_with_pet()
    today = date(2026, 10, 20)
    task = task_at("08:00", description="Morning walk", frequency="daily", due_date=today)
    pet.add_task(task)

    scheduler.mark_task_complete(task)

    assert task.completed is True
    assert len(pet.get_tasks()) == 2
    new_task = pet.get_tasks()[1]
    assert new_task is not task
    assert new_task.due_date == today + timedelta(days=1)
    assert new_task.completed is False
    assert (new_task.description, new_task.pet_name, new_task.time, new_task.frequency) == (
        "Morning walk", "Biscuit", "08:00", "daily"
    )


def test_completing_weekly_task_creates_task_seven_days_later():
    owner, pet, scheduler = make_owner_with_pet()
    today = date(2026, 10, 20)
    task = task_at("10:00", description="Flea treatment", frequency="weekly", due_date=today)
    pet.add_task(task)

    scheduler.mark_task_complete(task)

    assert task.completed is True
    assert len(pet.get_tasks()) == 2
    new_task = pet.get_tasks()[1]
    assert new_task.due_date == today + timedelta(days=7)
    assert new_task.completed is False
    assert new_task.frequency == "weekly"


def test_completing_one_time_task_does_not_create_new_task():
    owner, pet, scheduler = make_owner_with_pet()
    task = task_at("10:00", frequency="once")
    pet.add_task(task)

    scheduler.mark_task_complete(task)

    assert task.completed is True
    assert len(pet.get_tasks()) == 1


def test_recurring_task_is_added_to_the_correct_pet():
    owner = Owner("Ishan")
    biscuit = Pet("Biscuit", "dog")
    mochi = Pet("Mochi", "cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)
    scheduler = Scheduler(owner)
    task = task_at("08:00", pet_name="Mochi", frequency="daily")
    mochi.add_task(task)

    scheduler.mark_task_complete(task)

    assert len(biscuit.get_tasks()) == 0
    assert len(mochi.get_tasks()) == 2


# ---------------------------------------------------------------------------
# detect_conflicts
# ---------------------------------------------------------------------------

def test_detect_conflicts_flags_two_tasks_at_same_time_for_same_pet():
    owner, pet, scheduler = make_owner_with_pet()
    pet.add_task(task_at("08:00", description="Walk"))
    pet.add_task(task_at("08:00", description="Feed"))

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]
    assert "Walk" in conflicts[0]
    assert "Feed" in conflicts[0]


def test_detect_conflicts_flags_same_time_across_different_pets():
    owner = Owner("Ishan")
    biscuit = Pet("Biscuit", "dog")
    mochi = Pet("Mochi", "cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)
    scheduler = Scheduler(owner)
    biscuit.add_task(task_at("08:00", pet_name="Biscuit", description="Walk"))
    mochi.add_task(task_at("08:00", pet_name="Mochi", description="Feed"))

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Biscuit" in conflicts[0]
    assert "Mochi" in conflicts[0]


def test_detect_conflicts_returns_empty_when_times_differ():
    owner, pet, scheduler = make_owner_with_pet()
    pet.add_task(task_at("08:00"))
    pet.add_task(task_at("08:15"))
    pet.add_task(task_at("09:00"))

    assert scheduler.detect_conflicts() == []


def test_detect_conflicts_reports_one_warning_per_crowded_time_slot():
    owner, pet, scheduler = make_owner_with_pet()
    pet.add_task(task_at("08:00", description="A"))
    pet.add_task(task_at("08:00", description="B"))
    pet.add_task(task_at("08:00", description="C"))
    pet.add_task(task_at("17:00", description="D"))
    pet.add_task(task_at("17:00", description="E"))

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 2
    assert any("08:00" in c for c in conflicts)
    assert any("17:00" in c for c in conflicts)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_pet_with_no_tasks():
    owner, pet, scheduler = make_owner_with_pet()

    assert pet.get_tasks() == []
    assert owner.get_all_tasks() == []
    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []
    assert scheduler.filter_tasks(pet_name="Biscuit") == []


def test_owner_with_no_pets():
    owner = Owner("Ishan")
    scheduler = Scheduler(owner)

    assert owner.pets == []
    assert owner.get_all_tasks() == []
    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []
    assert scheduler.filter_tasks(completed=False) == []


def test_completing_recurring_task_for_unknown_pet_does_not_raise():
    owner = Owner("Ishan")
    scheduler = Scheduler(owner)
    orphan = task_at("08:00", pet_name="Ghost", frequency="daily")

    scheduler.mark_task_complete(orphan)

    assert orphan.completed is True
    assert owner.get_all_tasks() == []


def test_filter_tasks_with_no_matches():
    owner, pet, scheduler = make_owner_with_pet()
    pet.add_task(task_at("08:00"))
    pet.add_task(task_at("09:00"))

    assert scheduler.filter_tasks(pet_name="Nobody") == []
    assert scheduler.filter_tasks(completed=True) == []
    assert scheduler.filter_tasks(pet_name="Biscuit", completed=True) == []


def test_filter_tasks_with_no_filters_returns_everything():
    owner, pet, scheduler = make_owner_with_pet()
    pet.add_task(task_at("08:00"))
    pet.add_task(task_at("09:00"))

    assert len(scheduler.filter_tasks()) == 2


def test_filter_tasks_by_pet_and_completed_status():
    owner, pet, scheduler = make_owner_with_pet()
    done = task_at("08:00", description="Done")
    done.mark_complete()
    pet.add_task(done)
    pet.add_task(task_at("09:00", description="Pending"))

    completed = scheduler.filter_tasks(pet_name="Biscuit", completed=True)
    pending = scheduler.filter_tasks(pet_name="Biscuit", completed=False)

    assert [t.description for t in completed] == ["Done"]
    assert [t.description for t in pending] == ["Pending"]
