from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="Jordan", availability_minutes=180, preferences=["morning walks", "gentle grooming"])

    bella = Pet(name="Bella", species="dog", age=4, energy_level="high")
    luna = Pet(name="Luna", species="cat", age=2, energy_level="low")

    owner.add_pet(bella)
    owner.add_pet(luna)

    tasks = [
        Task(title="Evening grooming", description="Brush Bella's coat", duration_minutes=20, priority="medium", time_window="19:00"),
        Task(title="Morning walk", description="Walk Bella before work", duration_minutes=30, priority="high", time_window="08:00"),
        Task(title="Feed Luna", description="Lunch and fresh water", duration_minutes=10, priority="high", time_window="08:00"),
    ]

    scheduler = Scheduler([owner])
    for pet, task in [(bella, tasks[0]), (bella, tasks[1]), (luna, tasks[2])]:
        scheduler.add_task(pet, task)

    tasks[1].mark_complete()

    conflict_warning = scheduler.detect_conflicts(scheduler.get_all_tasks(owner))
    if conflict_warning:
        print(conflict_warning)

    print("Today's Schedule")
    print("-" * 20)
    pending_tasks = scheduler.filter_tasks(scheduler.get_all_tasks(owner), completed=False)
    for task in scheduler.sort_by_time(pending_tasks):
        print(f"- {task.title} | {task.time_window} | {task.duration_minutes} min | Priority: {task.priority} | Pet: {task.pet_name}")

    print("\nBella's pending tasks")
    print("-" * 20)
    bella_pending = scheduler.filter_tasks(scheduler.get_all_tasks(owner), completed=False, pet_name="Bella")
    for task in scheduler.sort_by_time(bella_pending):
        print(f"- {task.title} | {task.time_window} | {task.duration_minutes} min")


if __name__ == "__main__":
    main()
