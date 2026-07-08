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
        pass

    def update_details(self, title: str, duration: int, priority: str) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    energy_level: str = "medium"
    health_notes: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_task_count(self) -> int:
        return 0


class Owner:
    def __init__(self, name: str, availability_minutes: int = 0, preferences: List[str] | None = None):
        self.name = name
        self.availability_minutes = availability_minutes
        self.preferences = preferences or []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def update_preferences(self, preferences: List[str]) -> None:
        pass


class Schedule:
    def __init__(self, date_value: date, owner: Owner, pet: Pet, planned_tasks: List[Task] | None = None):
        self.date = date_value
        self.owner = owner
        self.pet = pet
        self.planned_tasks = planned_tasks or []
        self.total_duration_minutes = 0

    def generate_plan(self, tasks: List[Task], owner: Owner, pet: Pet) -> None:
        pass

    def explain_plan(self) -> str:
        return ""

    def display_plan(self) -> str:
        return ""
