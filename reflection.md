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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
