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

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude Code as my main AI assistant across the project. In Phase 1 it generated the Mermaid class diagram from the attributes and methods I had brainstormed, then turned that diagram into a Python skeleton using dataclasses. In Phase 2 it implemented the core logic for Task, Pet, Owner, and Scheduler, wrote the main.py demo script, and drafted my first two pytest tests. The prompts that worked best were specific and narrow, for example "add a pet_name field to Task and change filter_tasks to filter by pet name, and change nothing else." Broad prompts produced more code than I wanted, so I kept each request small and checked the result before moving on. I also used a fresh chat session for each phase, which kept each conversation focused and made it easier to see what changed in each step.

**b. Judgment and verification**

I did not accept the first skeleton as it was. After reviewing it, I noticed that Task had no way to record which pet it belonged to, so once Owner.get_all_tasks() merged every pet's tasks into one list, the Scheduler could not tell whose task was whose. I also saw that filter_tasks filtered by species, while the assignment asks for filtering by pet or completion status. I added a pet_name field to Task and changed the filter to use pet name, then updated the UML diagram and my design notes to match.

In Phase 2, Claude Code also left out recurring tasks to keep things simple, and it limited detect_conflicts to overlapping tasks for the same pet, which is narrower than my design (same time, same or different pets). I decided to leave both for Phase 4 instead of accepting them as final. To verify the AI's work, I did not rely on its summaries. I ran python main.py myself and compared the schedule to what I expected, and I ran python -m pytest to confirm the tests passed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
