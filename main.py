from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="Jordan", availability_minutes=180, preferences=["morning walks", "gentle grooming"])

    bella = Pet(name="Bella", species="dog", age=4, energy_level="high")
    luna = Pet(name="Luna", species="cat", age=2, energy_level="low")

    owner.add_pet(bella)
    owner.add_pet(luna)

    tasks = [
        Task(title="Morning walk", description="Walk Bella before work", duration_minutes=30, priority="high", time_window="08:00"),
        Task(title="Feed Luna", description="Lunch and fresh water", duration_minutes=10, priority="high", time_window="12:00"),
        Task(title="Evening grooming", description="Brush Bella's coat", duration_minutes=20, priority="medium", time_window="19:00"),
    ]

    scheduler = Scheduler([owner])
    for pet, task in [(bella, tasks[0]), (luna, tasks[1]), (bella, tasks[2])]:
        scheduler.add_task(pet, task)

    print("Today's Schedule")
    print("-" * 20)
    for task in scheduler.generate_daily_plan(owner):
        print(f"- {task.title} | {task.time_window} | {task.duration_minutes} min | Priority: {task.priority}")


if __name__ == "__main__":
    main()
