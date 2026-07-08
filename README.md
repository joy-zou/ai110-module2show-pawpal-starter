# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🧩 Features

- Sorting by time: tasks are ordered chronologically using the scheduler's time-based logic.
- Filtering by status and pet: pending tasks can be shown for a specific pet or across all pets.
- Conflict warnings: overlapping tasks at the same time trigger a warning instead of breaking the app.
- Daily recurrence: completing a daily recurring task creates a new task for the next day.
- Streamlit workflow: users can add pets, create tasks, mark tasks complete, and generate a schedule from the UI.

## 🧪 Testing PawPal+
The tests cover sorting correctness, recurrence logic, and conflict detection.

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
[100%]

================================ 7 passed in 0.06s =================================
```

Confidence Level: 5 stars

## 📐 Smarter Scheduling

The scheduler now supports several rule-based features to help generate a practical daily plan.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by their time value, using the time window as a fallback. |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks by completion status and optionally by pet name. |
| Conflict handling | `Scheduler.detect_conflicts()` | Detects overlapping tasks at the same time and returns a warning message. |
| Recurring tasks | `Task.mark_complete()` | Creates the next daily or weekly task when a recurring task is completed. |

## 📸 Demo Walkthrough
1. Open the Streamlit app and enter owner information. The app creates an owner profile and a scheduler instance for that owner.
2. Add one or more pets, then create tasks for them with a title, duration, priority, recurrence, and due date.
3. Use the task list to mark tasks complete. If a task is recurring, the scheduler creates the next occurrence automatically.
4. Click Generate schedule to view pending tasks in chronological order. If two tasks share the same time, a warning appears so the user can adjust the plan.
5. Review the task table and pending-task list to see how the scheduler sorts, filters, and warns about conflicts.

Example CLI output from running main.py:

```text
Warning: overlapping tasks at 08:00: Morning walk, Feed Luna (Bella, Luna)
Today's Schedule
--------------------
- Feed Luna | 08:00 | 10 min | Priority: high | Pet: Luna
- Evening grooming | 19:00 | 20 min | Priority: medium | Pet: Bella

Bella's pending tasks
--------------------
- Evening grooming | 19:00 | 20 min
```
