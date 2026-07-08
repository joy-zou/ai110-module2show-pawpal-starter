from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Task:
    title: str
    description: str = ""
    duration_minutes: int = 0
    priority: str = "medium"
    time_window: str = "anytime"
    is_recurring: bool = False
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def update_details(
        self,
        title: str | None = None,
        duration: int | None = None,
        priority: str | None = None,
        description: str | None = None,
        time_window: str | None = None,
        is_recurring: bool | None = None,
    ) -> None:
        """Update the task's details with any provided values."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if duration is not None:
            self.duration_minutes = duration
        if priority is not None:
            self.priority = priority
        if time_window is not None:
            self.time_window = time_window
        if is_recurring is not None:
            self.is_recurring = is_recurring


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    energy_level: str = "medium"
    health_notes: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    owner: "Owner | None" = None

    def add_task(self, task: Task) -> None:
        """Add a task to this pet if it is not already present."""
        if task not in self.tasks:
            self.tasks.append(task)

    def get_task_count(self) -> int:
        """Return the number of tasks assigned to this pet."""
        return len(self.tasks)

    def get_pending_tasks(self) -> List[Task]:
        """Return the tasks that are still incomplete for this pet."""
        return [task for task in self.tasks if not task.is_completed]


class Owner:
    def __init__(self, name: str, availability_minutes: int = 0, preferences: List[str] | None = None):
        self.name = name
        self.availability_minutes = availability_minutes
        self.preferences = preferences or []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner if it is not already linked."""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def update_preferences(self, preferences: List[str]) -> None:
        """Replace the owner's preference list with a new one."""
        self.preferences = list(preferences)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets owned by this owner."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for this owner."""
        return [task for task in self.get_all_tasks() if not task.is_completed]


class Scheduler:
    def __init__(self, owners: List[Owner] | None = None):
        self.owners = owners or []

    def add_owner(self, owner: Owner) -> None:
        """Register an owner with the scheduler if needed."""
        if owner not in self.owners:
            self.owners.append(owner)

    def add_task(self, pet: Pet, task: Task) -> None:
        """Assign a task to a pet through the scheduler."""
        pet.add_task(task)

    def get_all_tasks(self, owner: Owner | None = None) -> List[Task]:
        """Return all known tasks for a specific owner or all registered owners."""
        if owner is not None:
            return owner.get_all_tasks()

        tasks: List[Task] = []
        for registered_owner in self.owners:
            tasks.extend(registered_owner.get_all_tasks())
        return tasks

    def get_pending_tasks(self, owner: Owner | None = None) -> List[Task]:
        """Return all incomplete tasks for the requested owner scope."""
        return [task for task in self.get_all_tasks(owner) if not task.is_completed]

    def organize_tasks(self, owner: Owner | None = None) -> List[Task]:
        """Sort pending tasks by priority, duration, and title."""
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        tasks = self.get_pending_tasks(owner)
        return sorted(
            tasks,
            key=lambda task: (
                priority_rank.get(task.priority.lower(), 99),
                task.duration_minutes,
                task.title.lower(),
            ),
        )

    def generate_daily_plan(self, owner: Owner | None = None) -> List[Task]:
        """Create a simple daily plan from the current pending tasks."""
        return self.organize_tasks(owner)

    def mark_task_complete(self, task: Task) -> None:
        """Mark a specific task as complete."""
        task.mark_complete()

    def explain_plan(self, owner: Owner | None = None) -> str:
        """Return a text summary of the current planned tasks."""
        tasks = self.generate_daily_plan(owner)
        if not tasks:
            return "No pending tasks to schedule."

        lines = [f"{task.title} ({task.priority}, {task.duration_minutes} min)" for task in tasks]
        return "\n".join(lines)

    def display_plan(self, owner: Owner | None = None) -> str:
        """Return the plan in a display-friendly string format."""
        return self.explain_plan(owner)


class Schedule(Scheduler):
    """Backward-compatible alias for the scheduler implementation."""

    pass
