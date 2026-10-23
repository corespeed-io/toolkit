---
name: principle-experience-first
description: "Use for product, UX, or feature-scope tradeoffs. Choose user delight over implementation convenience. Ship fewer polished features, not more rough ones."
disable-model-invocation: true
---

# Experience First

When implementation convenience conflicts with user delight, choose delight.

- Each feature, control, and option must have a reason.
- Ship less, and ship better. A polished experience with three features is better than a rough experience with ten.
- Make a prototype before you commit. Design decisions cost less in throwaway HTML than in production code.
- Get the details correct: transitions, alignment, spacing, feedback, and error states.
- Make the core loop tight. Each feature must serve the central workflow or stay out of its way.

The user is the person who uses the work. For a UI, this is the end user. For a library or an internal API, this is the colleague who imports it. The engineer who maintains the code next is also a user. Give their experience the same weight. Explain the impact from their point of view.

Foundations must serve the experience. Foundational thinking controls the *sequence* of the work. This principle controls the *target*.
