# Commit Message Guidelines

Effective commit messages are essential for maintaining a clear and organized version history of our project. We follow the "Conventional Commits" format to structure our commit messages consistently. This format helps convey information about each commit's purpose and context.

## Commit Message Structure

A commit message consists of several parts:

1. **Type:** Start the commit message with a type that describes the purpose of the commit. Common types include:

   - `feat`: A new feature or enhancement.
   - `fix`: A bug fix.
   - `chore`: Routine tasks, maintenance, or tooling changes.
   - `docs`: Documentation changes.
   - `style`: Code style/formatting changes (no code logic changes).
   - `refactor`: Code refactoring (neither a new feature nor a bug fix).
   - `test`: Adding or modifying tests.
   - `perf`: Performance improvements.

2. **Scope (optional):** Specify the scope of the commit, indicating which part of the project it affects. Enclose it in parentheses, e.g., `(core)` or `(docs)`.

3. **Description:** Write a concise and clear description of the changes made in this commit. Use the imperative mood (e.g., "Add feature" instead of "Added feature"). Keep it under 72 characters if possible.

4. **Body (optional):** For more complex changes, provide additional details in the commit message body. Use a blank line between the description and the body, and use paragraphs as needed for clarity.

5. **Breaking Changes (optional):** If the commit introduces breaking changes (e.g., API changes), include this section with a description of the breaking changes and instructions for users on how to update.

## Example Commit Message

```markdown
feat(core): Add new function for dictionary manipulation

This commit adds a new function, `nestdict.merge()`, which allows
users to merge two dictionaries with conflict resolution.

BREAKING CHANGE: The function signature of `nestdict.merge()` has
changed to support additional options. Users should update
their code accordingly.
