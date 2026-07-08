import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Task


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
