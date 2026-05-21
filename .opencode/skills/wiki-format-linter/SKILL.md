# Wiki Format Linter

## Description
Use this skill when the user asks to:
- Check if all wiki pages follow the required format
- Audit pages for missing sections
- Validate the structure of the wiki

## Workflow

1. **Get list of pages** using `fd`:
   ```bash
   fd -e md . /home/whitepeach/Документы/Marsel/wiki_book/wiki/
   ```

2. **Check each page** using `rg` and `read`:
   For each file `$file`:
   - Check for `# Title`: `rg "^# " "$file"`
   - Check for `**Summary**:`: `rg "^\*\*Summary\*\*:" "$file"`
   - Check for `**Sources**:`: `rg "^\*\*Sources\*\*:" "$file"`
   - Check for `**Last updated**:`: `rg "^\*\*Last updated\*\*:" "$file"`
   - Check for `---`: `rg "^---$" "$file"`
   - Check for `## Related pages`: `rg "^## Related pages" "$file"`

3. **Generate report**:
   - List pages missing any required element
   - Group by missing element type
   - Suggest fixes

## Notes
- Use `rg` (ripgrep) for fast content search
- Use `fd` for fast file finding
- Exclude `index.md` and `log.md` from strict format checks if they don't follow the template
