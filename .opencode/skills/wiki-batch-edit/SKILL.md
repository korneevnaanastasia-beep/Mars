# Wiki Batch Edit

## Description
Use this skill when the user asks to:
- Rename a wiki page and update all links
- Replace text across multiple wiki pages
- Perform bulk operations on the wiki

## Workflow

### Rename Page
1. **Rename file**: `mv wiki/old-name.md wiki/new-name.md`
2. **Update all links**: 
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   rg -l "\[\[old-name\]\]" *.md | xargs sed -i "s/\[\[old-name\]\]/[[new-name]]/g"
   ```
3. **Update index.md**: Edit `wiki/index.md` to replace `[[old-name]]` with `[[new-name]]`
4. **Update log.md**: Add entry about rename

### Batch Text Replace
1. **Find and replace**:
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   rg -l "search-pattern" *.md | xargs sed -i "s/search-pattern/replace-pattern/g"
   ```
2. **Verify**: Check that changes were made correctly

### Add Category to Multiple Pages
1. **Add text to pages** (e.g., add a tag or category):
   ```bash
   cd /home/whitepeach/Документы/Marsel/wiki_book/wiki
   for file in *.md; do
     echo "" >> "$file"
     echo "**Category**: SomeCategory" >> "$file"
   done
   ```

## Notes
- Use `rg` to find files containing the pattern
- Use `sed -i` for in-place editing
- Always verify changes after batch operations
- Be careful with special characters in sed patterns
