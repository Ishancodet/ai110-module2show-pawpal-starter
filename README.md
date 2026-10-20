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

## 🖥️ Sample Output

Output from running `python main.py`:

```
Today's Schedule for Ishan (Tuesday, October 20, 2026)
============================================================
[ ] 07:30  Feeding                Mochi     10 min  priority: high
[ ] 08:00  Morning walk           Biscuit   30 min  priority: high
[ ] 09:00  Feeding                Biscuit   10 min  priority: high
[ ] 17:30  Grooming               Biscuit   20 min  priority: low
[ ] 19:00  Play with feather toy  Mochi     15 min  priority: medium
============================================================
5 tasks scheduled.
```

### Implementation Summary

`Task` is a dataclass holding one care activity: description, pet name, time, duration, priority, frequency, due date, and a completed flag it can set with `mark_complete()`. `Pet` stores a name, species, and its own list of tasks. `Owner` holds a name and a list of pets, and `get_all_tasks()` merges every pet's tasks into one list. `Scheduler` takes an owner and reads tasks through `get_all_tasks()`; it sorts them by time, filters by pet name, priority, or completion status, detects overlapping time slots for the same pet, and marks tasks complete. Together they form a simple chain: tasks belong to pets, pets belong to an owner, and the scheduler turns the owner's combined task list into a daily plan.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
