# Wiki Page Creator

## Description
Use this skill when the user asks to:
- Create a new wiki page with the correct format
- Add a new concept, character, or location to the wiki
- Quickly scaffold a page following the `AGENTS.md` standards

## Workflow

1. **Get details**: Ask for the page name (lowercase with hyphens) and a one-sentence summary.

2. **Create the file** using `write`:
   ```markdown
   # Page Title (from name)

   **Summary**: (provided summary)

   **Sources**: (list raw files or "TBD")

   **Last updated**: (current date, e.g., 29 апреля 2026)

   ---

   (Main content here)

   ## Related pages

   - (add links later)
   ```

3. **Update `wiki/index.md`**:
   - Read `wiki/index.md`
   - Find the correct category (e.g., "Персонажи", "Локации", "Концепции")
   - Add: `- [[page-name]] — (summary)`
   - Use `edit` to insert the line

4. **Update `wiki/log.md`**:
   - Read `wiki/log.md`
   - Append: `- (date): Created [[page-name]]`
   - Use `edit` to add the entry

5. **Confirm**: Report that the page was created and linked.
