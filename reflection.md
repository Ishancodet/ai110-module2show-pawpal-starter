# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

**Three core actions a user should be able to perform:**

1. **Add a pet.** The owner enters their own name and then adds a pet by giving its name and species. This lets one owner manage more than one pet, each with its own care routine.

2. **Schedule a care task for a pet.** The owner picks a pet and adds a task such as a walk, feeding, medication, or vet appointment. Each task has a description, a time (HH:MM), a duration, a priority, and a frequency (once, daily, or weekly).

3. **View today's schedule.** The owner sees every task across all of their pets, sorted by time. Tasks that overlap at the same time are flagged with a warning, and completed tasks can be marked done so a new one is created for recurring tasks.

**Classes and responsibilities:**

- **Task** represents one care activity. It stores a description, time (HH:MM), duration, priority, frequency, due date, and completion status, and can mark itself complete.
- **Pet** stores a pet's name and species along with its list of tasks. It can add a task and return its tasks.
- **Owner** stores the owner's name and a list of pets. It can add a pet and return every pet's tasks together through `get_all_tasks()`.
- **Scheduler** is the brain. It holds a reference to the owner and reads all tasks through `Owner.get_all_tasks()`. It sorts tasks by time, filters by pet or completion status, detects conflicts, and marks tasks complete (creating the next occurrence for recurring tasks).

**b. Design changes**

Yes. I added a `pet_name` field to `Task` because `Owner.get_all_tasks()` merges the tasks from every pet into a single list, and once they are merged the `Scheduler` has no way to tell which pet a task belongs to. I also changed `Scheduler.filter_tasks()` to filter by pet name instead of species, since the assignment asks for filtering by pet or by completion status, and species was not specific enough to identify one pet.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

My scheduler only flags tasks that have an identical start time, not tasks whose durations overlap. That is simpler and more predictable, and it is enough for a daily pet routine where most tasks are short. The cost is that a 30-minute walk at 08:00 and a feeding at 08:15 are not flagged.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude Code as my main AI assistant across the project. In Phase 1 it generated the Mermaid class diagram from the attributes and methods I had brainstormed, then turned that diagram into a Python skeleton using dataclasses. In Phase 2 it implemented the core logic for Task, Pet, Owner, and Scheduler, wrote the main.py demo script, and drafted my first two pytest tests. The prompts that worked best were specific and narrow, for example "add a pet_name field to Task and change filter_tasks to filter by pet name, and change nothing else." Broad prompts produced more code than I wanted, so I kept each request small and checked the result before moving on. I also used a fresh chat session for each phase, which kept each conversation focused and made it easier to see what changed in each step.

The Claude Code features that helped most were editing several files at once (a change like adding pet_name touched pawpal_system.py, the UML diagram, and my reflection in one step) and running the code itself, so it could run main.py and the tests and show me the result. Starting a fresh /clear session for each phase (design, core logic, UI, algorithms, testing, polish) kept each conversation focused, so the context for one phase did not leak into the next and I could tell what changed in each step.

**b. Judgment and verification**

I did not accept the first skeleton as it was. After reviewing it, I noticed that Task had no way to record which pet it belonged to, so once Owner.get_all_tasks() merged every pet's tasks into one list, the Scheduler could not tell whose task was whose. I also saw that filter_tasks filtered by species, while the assignment asks for filtering by pet or completion status. I added a pet_name field to Task and changed the filter to use pet name, then updated the UML diagram and my design notes to match.

In Phase 2, Claude Code also left out recurring tasks to keep things simple, and it limited detect_conflicts to overlapping tasks for the same pet, which is narrower than my design (same time, same or different pets). I decided to leave both for Phase 4 instead of accepting them as final. To verify the AI's work, I did not rely on its summaries. I ran python main.py myself and compared the schedule to what I expected, and I ran python -m pytest to confirm the tests passed.

Claude Code also offered three ways to simplify detect_conflicts. I rejected the sort-and-compare version because it could raise an error on a bad time string, which breaks my requirement that conflict detection never crashes. I chose the dictionary grouping because it reads like the problem (bucket by time, report crowded buckets), even though it changes the output to one warning per time slot.

---

## 4. Testing and Verification

**a. What you tested**

I tested sorting (tasks added out of order come back in chronological order), recurrence (completing a daily task creates a new task for the next day, and a weekly one 7 days later), conflict detection (two tasks at the same time are flagged, including across different pets), and edge cases such as a pet with no tasks, an owner with no pets, and filters that match nothing. These matter because the app's value depends on the schedule being ordered correctly, recurring tasks not disappearing, and the owner being warned about clashes.

**b. Confidence**

I am about 4 out of 5 confident. All 19 tests pass, and they cover the main behaviors and several edge cases. I am not at 5 because conflict detection only compares identical start times, so overlapping durations are not caught, and I have not tested invalid time strings. If I had more time I would test overlapping durations (a 30-minute walk at 08:00 and a feeding at 08:15), malformed times like "8:00" or "25:99", and marking the same task complete twice.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the algorithmic layer. Sorting, filtering, daily and weekly recurrence, and conflict detection all work together through the Scheduler, and I verified them with 19 passing tests and a demo script that shows each behavior in the terminal.

**b. What you would improve**

I would add real overlap detection so a 30-minute walk at 08:00 and a feeding at 08:15 are flagged, since right now only identical start times are caught. I would also validate time strings so a value like '8:00' or '25:99' is rejected with a clear message instead of being silently treated as a different time.

**c. Key takeaway**

Working with AI made me the lead architect. Claude Code writes code quickly, but I had to decide the design, notice where its output did not match the spec (Task had no pet_name and filter_tasks used species), choose between its options, and verify everything by running main.py and pytest myself instead of trusting its summaries.
