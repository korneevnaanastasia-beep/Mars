# Wiki Stats

## Description
Use this skill when the user asks to:
- Get statistics about the wiki (page count, word count, etc.)
- See how the wiki has grown over time
- Generate a summary report of the wiki

## Workflow

1. **Basic counts** using `fd` and `rg`:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   echo "Total pages: $(fd -e md . | wc -l)"
   echo "Total lines: $(cat *.md | wc -l)"
   echo "Total words: $(cat *.md | wc -w)"
   ```

2. **Breakdown by category** (from `index.md`):
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   echo "--- Pages by category ---"
   rg "^### |^## " index.md
   ```

3. **Growth over time** (from `log.md`):
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   echo "--- Recent activity ---"
   rg "^- " log.md | tail -10
   ```

4. **Top pages by size**:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   ls -lS *.md | head -10
   ```

5. **Generate report**:
   - Summary of basic stats
   - Category breakdown
   - Recent activity
   - Largest pages

## Notes
- Use `fd` for counting files
- Use `rg` for searching within files
- Use `wc` for counting lines/words
