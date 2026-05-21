# Wiki Source Validator

## Description
Use this skill when the user asks to:
- Validate that all source files listed in wiki pages exist in `raw/`
- Check for broken source references
- Find facts without source citations

## Workflow

1. **Scan wiki pages** for source references:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   rg "^\*\*Sources\*\*:" *.md | sed 's/.*:.*: //' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | sort -u > /tmp/sources.txt
   ```

2. **Check if sources exist** in `raw/`:
   ```bash
   while read source; do
     if [ ! -f "/home/whitepeach/Документы/Marsel/wiki_book/raw/$source" ]; then
       echo "MISSING SOURCE: $source (referenced in wiki)"
     fi
   done < /tmp/sources.txt
   ```

3. **Check for facts without citations**:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   for file in *.md; do
     # Count lines with (source: ...) vs total content lines
     total=$(rg -v "^\*\*|^---|^#|^$|^##" "$file" | wc -l)
     cited=$(rg "\(source:" "$file" | wc -l)
     if [ $total -gt 5 ] && [ $cited -eq 0 ]; then
       echo "NO CITATIONS: $file has $total content lines but 0 citations"
     fi
   done
   ```

4. **Generate report**:
   - List missing source files
   - List pages with no citations
   - Suggest adding missing sources to `raw/` or fixing references

## Notes
- Use `rg` for searching
- Source files should be relative to `raw/` directory
