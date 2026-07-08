import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Scheduler, Task


def test_mark_complete_updates_task_status():
    task = Task(title="Feed pet", duration_minutes=10, priority="high")

    assert task.is_completed is False

    task.mark_complete()

    assert task.is_completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    task = Task(title="Walk", duration_minutes=20, priority="medium")

    assert pet.get_task_count() == 0

    pet.add_task(task)

    assert pet.get_task_count() == 1


def test_sorting_correctness_returns_tasks_in_chronological_order():
    scheduler = Scheduler()
    late = Task(title="Late", duration_minutes=10, priority="high", time_window="19:00")
    early = Task(title="Early", duration_minutes=10, priority="high", time_window="09:00")
    middle = Task(title="Middle", duration_minutes=10, priority="high", time_window="12:00")

    ordered = scheduler.sort_by_time([late, early, middle])

    assert [task.title for task in ordered] == ["Early", "Middle", "Late"]


def test_recurrence_logic_creates_next_day_task_when_daily_task_completed():
    task = Task(
        title="Water plants",
        duration_minutes=5,
        priority="medium",
        is_recurring=True,
        recurrence="daily",
        due_date=date(2026, 7, 7),
    )

    next_task = task.mark_complete()

    assert task.is_completed is True
    assert next_task is not None
    assert next_task.is_completed is False
    assert next_task.due_date == date(2026, 7, 8)


def test_mark_complete_creates_next_weekly_task():
    task = Task(
        title="Groom pet",
        duration_minutes=15,
        priority="high",
        is_recurring=True,
        recurrence="weekly",
        due_date=date(2026, 7, 7),
    )

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 14)


def test_filter_tasks_by_completion_status_and_pet_name():
    scheduler = Scheduler()
    bella = Pet(name="Bella", species="dog")
    luna = Pet(name="Luna", species="cat")

    pending_bella = Task(title="Walk Bella", duration_minutes=20, priority="high")
    completed_luna = Task(title="Feed Luna", duration_minutes=10, priority="medium")
    completed_luna.mark_complete()

    scheduler.add_task(bella, pending_bella)
    scheduler.add_task(luna, completed_luna)

    filtered = scheduler.filter_tasks([pending_bella, completed_luna], completed=False, pet_name="Bella")

    assert filtered == [pending_bella]


def test_conflict_detection_flags_duplicate_times():
    scheduler = Scheduler()
    bella = Pet(name="Bella", species="dog")
    luna = Pet(name="Luna", species="cat")

    first = Task(title="Morning walk", duration_minutes=30, priority="high", time_window="08:00")
    second = Task(title="Feed Luna", duration_minutes=10, priority="high", time_window="08:00")

    scheduler.add_task(bella, first)
    scheduler.add_task(luna, second)

    warning = scheduler.detect_conflicts([first, second])

    assert warning is not None
    assert "08:00" in warning
