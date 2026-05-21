# Wiki Auto Linker

## Description
Use this skill when the user asks to:
- Find mentions of existing pages that are not wikilinked
- Suggest adding `[[page-name]]` links to relevant pages
- Discover missing backlinks

## Workflow

1. **Get list of existing pages** using `fd`:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   fd -e md . | xargs -n1 basename | sed 's/\.md$//' | sort > /tmp/pages.txt
   ```

2. **For each page**, search for mentions of other page names:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   for target in $(cat /tmp/pages.txt); do
     # Search for the target name in all files except the target file itself
     rg -l "$target" *.md | while read file; do
       # Skip if file is the target page itself
       if [ "$(basename $file .md)" != "$target" ]; then
         # Check if it's NOT already a wikilink [[target]]
         if ! rg -q "\[\[${target}\]\]" "$file"; then
           echo "SUGGEST: In $file, mention of '$target' is not linked. Add [[$target]]"
         fi
       fi
     done
   done
   ```

3. **Generate report**:
   - List all suggestions grouped by source file
   - Prioritize suggestions where the mention is a full word match

## Notes
- Use `rg` for fast searching
- Use `fd` for listing pages
- Be careful with partial matches (e.g., "cat" matching "category")
