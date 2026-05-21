# Orphan Page Checker

## Description
Use this skill when the user asks to:
- Find orphan pages (pages with no inbound wiki links)
- Check which wiki pages are not referenced by any other page
- Audit the wiki for isolated pages that need more cross-linking

## Workflow

When triggered, execute these steps:

1. **Get all wiki pages** using `fd`:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   fd -e md . | xargs -n1 basename | sed 's/\.md$//' | sort
   ```

2. **Check inbound links for each page** using `rg`:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   for page in $(fd -e md . | xargs -n1 basename | sed 's/\.md$//' | sort); do
     count=$(rg -c "\[\[${page}\]\]" *.md 2>/dev/null | awk -F: '{sum += $2} END {print sum+0}')
     if [ "$count" -eq 0 ]; then
       echo "ORPHAN: $page.md (0 inbound links)"
     fi
   done
   ```

3. **Generate report**:
   - List all orphan pages
   - Exclude `index.md` and `log.md` from the report (they are utility pages)
   - Suggest adding links to orphan pages from related content

## Example Usage

**User**: "Найди сиротские страницы в вики"
**Assistant**: *runs this skill, reports orphan pages*

**User**: "Какие страницы ни на что не ссылаются?"
**Assistant**: *uses this skill to check*

## Notes

- Orphan pages have 0 inbound links from other wiki pages
- Utility pages (`index.md`, `log.md`) are expected to be orphans — exclude them from reports
- Use `fd` for fast file discovery (replaces `find`)
- Use `rg` for fast content search (replaces `grep`)
- To fix orphan pages: add `[[page-name]]` links from related pages in `## Related pages` section
