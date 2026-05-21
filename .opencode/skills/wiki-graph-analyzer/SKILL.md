# Wiki Graph Analyzer

## Description
Use this skill when the user asks to:
- Analyze the link structure of the wiki
- Find the most referenced pages (hubs)
- Identify isolated clusters of pages
- See which pages have the most outgoing links

## Workflow

1. **Collect data** using `fd` and `rg`:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   PAGES=$(fd -e md . | xargs -n1 basename | sed 's/\.md$//' | sort)
   ```

2. **Calculate inbound links** (pages linking TO this page):
   ```bash
   for page in $PAGES; do
     count=$(rg -c "\[\[${page}\]\]" *.md 2>/dev/null | awk -F: '{sum += $2} END {print sum+0}')
     echo "$count $page"
   done | sort -rn | head -10
   ```

3. **Calculate outbound links** (links FROM this page):
   ```bash
   for page in $PAGES; do
     count=$(rg -o "\[\[[a-zа-яё-]*\]\]" "$page.md" 2>/dev/null | wc -l)
     echo "$count $page"
   done | sort -rn | head -10
   ```

4. **Generate report**:
   - Top 10 pages by inbound links (Hubs)
   - Top 10 pages by outbound links (Connectors)
   - List pages with 0 inbound links (Orphans, excluding index/log)
   - Identify potential isolated clusters

## Notes
- Use `rg` for counting links
- Use `fd` for listing pages
