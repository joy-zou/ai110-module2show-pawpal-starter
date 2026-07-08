import streamlit as st
from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def sync_task_state(owner: Owner) -> None:
    st.session_state.tasks = [
        {
            "pet_name": pet.name,
            "title": task.title,
            "duration_minutes": task.duration_minutes,
            "priority": task.priority,
            "recurrence": task.recurrence or "none",
            "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else "No date",
            "completed": task.is_completed,
        }
        for pet in owner.pets
        for task in pet.tasks
    ]


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", availability_minutes=180, preferences=["morning walks", "gentle grooming"])

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler([st.session_state.owner])

owner = st.session_state.owner
scheduler = st.session_state.scheduler

owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name

st.markdown("### Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if any(existing_pet.name.lower() == pet_name.lower() for existing_pet in owner.pets):
        st.warning("That pet already exists for this owner.")
    else:
        new_pet = Pet(name=pet_name or "Pet", species=species)
        owner.add_pet(new_pet)
        sync_task_state(owner)
        st.success(f"Added {new_pet.name} to {owner.name}'s pets.")

st.markdown("### Add a Task")
st.caption("Create a task and attach it to one of your pets.")

pet_options = [pet.name for pet in owner.pets] if owner.pets else ["No pets yet"]
selected_pet_name = st.selectbox("Assign task to", pet_options)

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"], index=0)

due_date = st.date_input("Due date", value=date.today())

if st.button("Add task"):
    if not owner.pets:
        st.warning("Please add a pet before creating a task.")
    else:
        selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            is_recurring=recurrence != "none",
            recurrence=recurrence if recurrence != "none" else None,
            due_date=due_date,
        )
        scheduler.add_owner(owner)
        scheduler.add_task(selected_pet, task)
        task.pet_name = selected_pet.name
        sync_task_state(owner)
        st.success(f"Added {task.title} for {selected_pet.name}.")

if st.session_state.get("tasks"):
    st.subheader("Current tasks")
    task_rows = [
        {
            "Pet": pet.name,
            "Task": task.title,
            "Priority": task.priority,
            "Duration (min)": task.duration_minutes,
            "Recurrence": task.recurrence or "once",
            "Due": task.due_date.strftime("%Y-%m-%d") if task.due_date else "n/a",
            "Status": "Completed" if task.is_completed else "Pending",
        }
        for pet in owner.pets
        for task in pet.tasks
    ]
    st.table(task_rows)

    pending_tasks = scheduler.filter_tasks(scheduler.get_all_tasks(owner), completed=False)
    if pending_tasks:
        st.subheader("Pending tasks")
        sorted_pending = scheduler.sort_by_time(pending_tasks)
        for task in sorted_pending:
            st.write(
                f"- {task.title} ({task.pet_name}) | {task.priority} | {task.duration_minutes} min | {task.time_window} | due {task.due_date or 'n/a'}"
            )
            if st.button("Mark complete", key=f"complete_{id(task)}"):
                next_task = task.mark_complete()
                if next_task is not None:
                    owner.pets[0].add_task(next_task) if owner.pets else None
                sync_task_state(owner)
                st.rerun()
    else:
        st.info("No pending tasks.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Use the schedule button to preview the sorted pending tasks.")

if st.button("Generate schedule"):
    scheduler.add_owner(owner)
    for pet in owner.pets:
        for task in pet.tasks:
            if task not in scheduler.get_all_tasks(owner):
                scheduler.add_task(pet, task)

    pending_tasks = scheduler.filter_tasks(scheduler.get_all_tasks(owner), completed=False)
    conflict_warning = scheduler.detect_conflicts(pending_tasks)
    plan = scheduler.sort_by_time(pending_tasks)

    if conflict_warning:
        st.warning(conflict_warning)

    st.success("Schedule generated")
    if plan:
        plan_rows = [
            {
                "Task": task.title,
                "Pet": task.pet_name or "unknown",
                "Priority": task.priority,
                "Time": task.time_window,
                "Duration (min)": task.duration_minutes,
                "Due": task.due_date.strftime("%Y-%m-%d") if task.due_date else "n/a",
            }
            for task in plan
        ]
        st.table(plan_rows)
    else:
        st.info("No tasks available yet.")
