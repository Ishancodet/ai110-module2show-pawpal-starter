import streamlit as st
from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler

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

st.subheader("Owner & Pets")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
owner: Owner = st.session_state.owner
owner.name = owner_name

col_a, col_b = st.columns(2)
with col_a:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_b:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species))
    st.success(f"Added pet '{pet_name}' ({species}).")

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_time = st.text_input("Time (HH:MM)", value="08:00")
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

pet_names = [p.name for p in owner.pets]
task_pet = st.selectbox("Assign to pet", pet_names) if pet_names else None

if st.button("Add task", disabled=task_pet is None):
    pet = next(p for p in owner.pets if p.name == task_pet)
    pet.add_task(
        Task(
            description=task_title,
            pet_name=pet.name,
            time=task_time,
            duration_minutes=int(duration),
            priority=priority,
            frequency="daily",
            due_date=date.today(),
        )
    )
    st.success(f"Added task '{task_title}' for {pet.name} at {task_time}.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": t.pet_name,
                "task": t.description,
                "time": t.time,
                "duration_minutes": t.duration_minutes,
                "priority": t.priority,
            }
            for t in Scheduler(owner).sort_by_time(all_tasks)
        ]
    )
else:
    st.info("No tasks yet. Add a pet, then add a task.")

st.divider()

st.subheader("Build Schedule")
st.caption("Builds a time-ordered plan for today from all current tasks.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()
    if not all_tasks:
        st.info("No tasks to schedule. Add a pet and at least one task first.")
    else:
        schedule = scheduler.sort_by_time(all_tasks)
        st.table(
            [
                {
                    "time": t.time,
                    "pet": t.pet_name,
                    "task": t.description,
                    "duration_minutes": t.duration_minutes,
                    "priority": t.priority,
                    "status": "done" if t.completed else "pending",
                }
                for t in schedule
            ]
        )
        conflicts = scheduler.detect_conflicts(schedule)
        for message in conflicts:
            st.warning(message)
        if conflicts:
            st.info(f"Schedule built with {len(schedule)} task(s), but {len(conflicts)} time conflict(s) need attention.")
        else:
            st.success(f"Schedule built: {len(schedule)} task(s), no time conflicts.")
