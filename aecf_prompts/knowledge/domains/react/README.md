# React Domain

## What is this domain?

The **React** domain covers front-end development with React. It provides rules for treating React as a UI composition layer with clean separation of app shell, feature modules, reusable components, and data-access concerns — keeping state, routing, and side effects intentional.

## Capabilities

- **Architecture guidance** separating features, components, and data access with explicit state ownership.
- **Coding rules** for explicit props, predictable hooks, immutable state transitions, and loading/error/empty state handling.
- **Testing guidance** using React Testing Library for behavior-driven UI checks resilient to refactors.
- **Dependency management** reviewing client-side packages for bundle impact and security.
- **Common pitfall detection** for data fetching in leaf components, duplicated derived state, and mixed design-system/domain layers.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `react_component_app_architecture` | React app architecture — component design, hooks, state management, routing, testing. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=react
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor stack=react/react_component_app_architecture
```
