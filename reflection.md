# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I had the classes of owner, pet, tasks, and schedule. Owner and pet include information about each that the user can edit, tasks allow tasks to be created, and schedule uses the tasks to create a plan with constraints considered.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

No, my design did not really change during implementation.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers constraints such as priority and time as most important. I decided these mattered most, more than preferences, because time window determines when tasks can appear and priority ensures important tasks are handled first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff the scheduler makes is that it does not account for owner availability. This tradeoff is currently reasonable because in the app description, the owner does not ask for 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools as an assisistant in design brainstorming, drafting in Mermaid, and developing functions/improving algorithms. I found that the prompts that were most helpful included multiple files across my project, and explicitely mentioned functions in them, so that the tool had all the information necessary. I also found questions asking the tool to explain its suggestions before implementing them were helpful for both my own understanding and preventing mistakes.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I did not accept an AI suggestion is when I was using Copilot and it suggested changes to the UML draft and classes. Although Copilot thought the suggestions of added methods and fields would improve the app, it was not part of my original design, and I felt it would complicate the app beyond what was in the project description.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested behaviors such as adding tasks, marking them as complete, and scheduling the tasks. These tests are important because they make up the core functions of the app. If the tasks aren't created properly, they could influence the scheduling, and a well made schedule result is what the user is expecting.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am around 90% confident that my scheduler works correctly. I've implemented test cases and my scheduler passed all of them, and have tested the deployed app myself. However, I'm sure there are edge cases that I may have missed. If I had more time, I would test with multiple pets and boundaries of tasks (ex. more tasks than can be schduled in one day).

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I was most satisfied with designing the classes, as it was a good refersher on object-oriented programming and it felt very intuitive with this project scope.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would work on improving the scheduler to take into account more constraints and priorities. This way, the user will be more satisfied with the plan.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important thing I learned about working with AI is that I am able to collaborate with it to not only implement but design systems, and that when working across systems it is important to attach *all* relevant files when communicating with an AI tool.
