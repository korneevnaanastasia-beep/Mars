# Wiki Link Checker

## Description
Use this skill when the user asks to:
- Check for broken wiki links (links to non-existent pages)
- Validate that all `[[page-name]]` links in `wiki/` point to existing `.md` files
- Audit the wiki for orphaned concepts or missing pages

## Workflow

When triggered, execute these steps:

1. **List all existing pages**:
   ```bash
   fd -e md . /home/whitepeach/Документы/Marsel/wiki_book/wiki/
   ```

2. **Extract all wiki links** from every `.md` file in `wiki/`:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   rg -o "\[\[[a-zа-яё-]*\]\]" *.md | sed 's/.*:\[\[\(.*\)\]\]/\1/' | sort -u
   ```

3. **Check if each linked page exists**:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   for link in $(rg -o "\[\[[a-zа-яё-]*\]\]" *.md | sed 's/.*:\[\[\(.*\)\]\]/\1/' | sort -u); do
     if [ ! -f "${link}.md" ]; then
       echo "BROKEN LINK: [[$link]] -> ${link}.md not found"
     fi
   done
   ```

4. **Generate report**:
   - List all broken links found
   - Group by source file
   - Suggest creating missing pages or fixing links

## Example Usage

**User**: "Проверь битые ссылки в вики"
**Assistant**: *runs this skill, reports broken links*

**User**: "Есть ли страница для концепции X?"
**Assistant**: *uses this skill to check*

## Notes

- Page names use lowercase with hyphens (e.g., `machine-learning.md`)
- Wiki links use double brackets: `[[page-name]]`
- All pages should have a corresponding `.md` file in `wiki/`
- Use `rg` (ripgrep) for fast content search
- Use `fd` for fast file finding
