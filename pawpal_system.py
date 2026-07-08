from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


@dataclass
class Task:
    title: str
    description: str = ""
    duration_minutes: int = 0
    priority: str = "medium"
    time_window: str = "anytime"
    is_recurring: bool = False
    recurrence: str | None = None
    due_date: date | None = None
    is_completed: bool = False
    pet_name: str | None = None

    def mark_complete(self) -> "Task | None":
        """Mark this task as completed and create the next occurrence for recurring tasks."""
        self.is_completed = True
        if not self.is_recurring or not self.recurrence:
            return None

        if self.recurrence.lower() == "daily":
            next_due_date = (self.due_date or date.today()) + timedelta(days=1)
        elif self.recurrence.lower() == "weekly":
            next_due_date = (self.due_date or date.today()) + timedelta(weeks=1)
        else:
            return None

        return Task(
            title=self.title,
            description=self.description,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            time_window=self.time_window,
            is_recurring=True,
            recurrence=self.recurrence,
            due_date=next_due_date,
            is_completed=False,
            pet_name=self.pet_name,
        )

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
        if not task.pet_name:
            task.pet_name = pet.name

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered by their time value, using the time window as a fallback."""
        return sorted(
            tasks,
            key=lambda task: (
                getattr(task, "time", None) is None,
                str(getattr(task, "time", getattr(task, "time_window", ""))).lower(),
            ),
        )

    def filter_tasks(
        self,
        tasks: List[Task],
        *,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> List[Task]:
        """Return tasks that match the requested completion state and optional pet name."""
        filtered_tasks: List[Task] = []
        for task in tasks:
            if completed is not None and task.is_completed != completed:
                continue
            if pet_name is not None:
                task_pet_name = getattr(task, "pet_name", None)
                if task_pet_name is None or task_pet_name.lower() != pet_name.lower():
                    continue
            filtered_tasks.append(task)
        return filtered_tasks

    def detect_conflicts(self, tasks: List[Task]) -> str | None:
        """Return a warning message when multiple tasks overlap at the same time window."""
        grouped: dict[str, List[Task]] = {}
        for task in tasks:
            time_value = str(getattr(task, "time", getattr(task, "time_window", ""))).strip().lower()
            grouped.setdefault(time_value, []).append(task)

        for time_value, time_tasks in grouped.items():
            if len(time_tasks) > 1:
                task_names = ", ".join(task.title for task in time_tasks)
                pet_names = ", ".join(task.pet_name or "unknown" for task in time_tasks)
                return f"Warning: overlapping tasks at {time_value}: {task_names} ({pet_names})"
        return None

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

    def mark_task_complete(self, task: Task) -> Task | None:
        """Mark a specific task as complete and return the next recurring task if created."""
        return task.mark_complete()

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
