# Migrate Notion Content to GitHub Wiki

**Skill**: Migrate one or more Notion pages to a GitHub repository wiki, preserving formatting, structure, and converting Notion-specific elements to GitHub wiki markdown.

## Outcome

Transform Notion documentation into GitHub wiki pages while maintaining readability, structure, and navigation.

## Quick Start

**For a complete migration with script:**
```bash
# Use the migration script
./docs/skills/migrate-notion-to-wiki-script.sh
```

**For manual migration, follow the detailed instructions below.**

---

## Instructions

### 1. Gather Required Information

**Ask the user for:**
- Notion page URL(s) to migrate
- Target GitHub repository (format: `owner/repo`)
- Optional: custom wiki page names (default: use Notion page titles)

### 2. Fetch Notion Content

For each Notion page:
- Use `mcp__notion__notion-fetch` with the page URL
- Extract the page title and markdown content
- Note any child pages or databases that should also be migrated
- **If fetch times out:** Reconnect MCP with `/mcp connect notion` and retry
- If still timing out, try fetching in smaller sections

### 3. Convert Content

**Notion to GitHub Wiki markdown conversions:**

| Notion Element | GitHub Wiki Conversion |
|---|---|
| Callouts (`> [!note]` etc.) | GitHub blockquotes with emoji prefixes |
| Toggle blocks (`<details>` tags) | Keep as-is (supported in GitHub) |
| Databases/tables | Convert to markdown tables where possible, or link back to Notion |
| Page mentions | Convert to wiki links `[[Page-Name]]` if target is migrated, otherwise external links |
| File attachments | Download and commit to wiki, or use permanent URLs |
| Code blocks | Keep fenced code blocks (fully supported) |
| Math expressions | Keep LaTeX syntax (GitHub supports it) |

**CRITICAL: Filename and Wiki Link Matching**

When converting Notion page titles to filenames and wiki links:
- **Convert ALL special characters to dashes**: colons (`:`) → dashes (`-`)
- **Example**: "ADR-001: Use FastAPI" → filename: `ADR-001-Use-FastAPI.md`
- **Wiki links MUST match the filename exactly**: `[[ADR-001-Use-FastAPI]]` NOT `[[ADR-001: Use FastAPI]]`
- Spaces → dashes: "Project Overview" → `Project-Overview.md`
- Remove or convert quotes, slashes, and other special characters

### 4. Set Up Wiki Repository

**Important:** Create a temporary export directory first, then clone the wiki.

```bash
# 1. Create export directory in the project
mkdir -p wiki-export

# 2. Try to clone the wiki
gh repo clone owner/repo.wiki

# If clone fails with "Repository not found":
# - Wiki needs initialization via GitHub UI
# - Open https://github.com/owner/repo/wiki
# - Click "Create the first page"
# - Add any content and save
# - Then retry the clone

# 3. Once cloned, verify contents
cd repo.wiki
ls -la
```

### 5. Create Wiki Pages

**Workflow:**
1. Create all markdown files in `wiki-export/` directory first
2. Copy them to the cloned wiki repo
3. Commit and push all at once

```bash
# Step 1: Create pages in export directory (using Write tool)
# Step 2: Copy to wiki repo
cp wiki-export/*.md repo.wiki/

# Step 3: Verify and commit
cd repo.wiki
git status
git add .
git commit -m "docs: migrate documentation from Notion

- Add [list of pages]
- Convert Notion callouts and formatting
- Update wiki links to match filenames

Migrated from Notion using the Notion MCP server."

git push origin master
```

**Filename sanitization rules:**
- Spaces → dashes: "Project Overview" → `Project-Overview.md`
- Colons → dashes: "ADR-001: Title" → `ADR-001-Title.md`
- Remove quotes, slashes, and special characters
- Keep the `.md` extension

### 6. Handle Special Cases

**Images and attachments:**
- **Option A**: Keep Notion signed URLs (simple, but URLs expire)
- **Option B**: Download and commit to wiki (increases repo size)
- **Option C**: Upload to GitHub Issues and use permanent URLs (recommended)

**Notion databases:**
- **Small databases**: Convert to markdown tables
- **Large databases**: Create a summary table and link back to Notion
- **Views**: Note that only data, not view configurations, can be migrated

**Hierarchy:**
- Create or update `Home.md` as a table of contents
- Use wiki links `[[Page-Name]]` to connect related pages
- Replicate Notion's page structure in wiki navigation

### 7. Push and Verify

```bash
# Push all changes
git push origin master

# Verify in browser
open "https://github.com/owner/repo/wiki"
```

### 8. Quality Verification

Check each migrated page in the browser:
- [ ] Formatting is preserved (headings, lists, bold, italic)
- [ ] Code blocks render correctly with syntax highlighting
- [ ] **All internal wiki links work** (click each one to verify)
- [ ] External links work correctly
- [ ] Images/attachments are accessible
- [ ] Tables are properly formatted
- [ ] Special elements (callouts, toggles) display correctly
- [ ] Page navigation in sidebar is correct

---

## Technical Notes

- GitHub wikis use **GitHub-Flavored Markdown (GFM)**
- Wiki page URLs are **case-sensitive** and spaces become dashes
- **Wiki links must exactly match filenames** (including special character conversion)
- The wiki is a **separate Git repository** from the main repo
- No direct wiki API exists; use `git` commands for all operations
- Notion MCP's `fetch` returns enhanced markdown that may need conversion
- Wiki must be initialized via GitHub UI before cloning (create one dummy page)
- **Best practice**: Export all pages to `wiki-export/` first, then copy to cloned wiki repo

---

## Error Handling

**Notion MCP timeouts:**
- **First step:** Reconnect with `/mcp connect notion`
- Wait for "Authentication successful. Connected to notion." message
- Retry the fetch operation
- If still timing out, try fetching smaller sections
- Test connectivity with `mcp__notion__notion-list-recent-pages`

**Wiki push failures:**
- Ensure wiki has been initialized (create one page via GitHub UI)
- Check auth: `gh auth status`
- Verify repo write permissions
- Confirm you're on the `master` branch (wiki default)

**Missing images:**
- Download from Notion URLs before they expire
- Commit to wiki repo or upload to GitHub Issues
- Update image references in markdown

---

## Example Workflow

```bash
# 1. If Notion MCP times out, reconnect first
/mcp connect notion

# 2. Fetch Notion pages via MCP
# Use mcp__notion__notion-fetch tool with page URLs
# Extract titles and content

# 3. Create export directory
mkdir -p wiki-export

# 4. Create all wiki pages in export directory (using Write tool)
# Sanitize filenames: "ADR-001: Title" → "ADR-001-Title.md"
# Convert wiki links to match filenames: [[ADR-001-Title]]

# 5. Clone wiki
gh repo clone agile-orchestrator/tulip-churn.wiki
cd tulip-churn.wiki

# 6. Copy all pages
cp ../wiki-export/*.md .

# 7. Verify filenames and links
ls -la
cat Home.md  # Check that wiki links match filenames

# 8. Commit and push
git add .
git commit -m "docs: migrate Tulip Bank documentation from Notion

- Add Home page with project overview and links
- Add Project Overview, Data Dictionary, DoR, DoD
- Add ADR-001 and Model Card Template
- Convert all wiki links to match filenames

Migrated from Notion using the Notion MCP server."
git push origin master

# 9. Verify in browser
open "https://github.com/agile-orchestrator/tulip-churn/wiki"
# Click through all wiki links to ensure they work
```

---

## Common Conversion Patterns

### Notion Callouts → GitHub Blockquotes

```markdown
<!-- Notion callout -->
> 💡 This is important information

<!-- GitHub wiki equivalent -->
> **💡 Note**
> This is important information
```

### Notion Database → Markdown Table

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value A  | Value B  | Value C  |
| Value D  | Value E  | Value F  |
```

### Notion Page Links → Wiki Links

```markdown
<!-- CORRECT: Wiki link matches filename exactly -->
Filename: ADR-001-Use-FastAPI.md
Wiki link: [[ADR-001-Use-FastAPI]]

<!-- INCORRECT: Don't use page title with special chars -->
Wiki link: [[ADR-001: Use FastAPI]]  ❌ WRONG - won't work!

<!-- If target page is migrated -->
See [[Target-Page-Name]] for details.

<!-- If target stays in Notion -->
See [Target Page](https://notion.so/target-page-url) for details.
```

---

## Quality Checklist

Before completing the migration:

- [ ] All requested Notion pages fetched successfully
- [ ] Markdown conversion verified (headings, lists, formatting)
- [ ] Special Notion elements handled appropriately (callouts, toggles)
- [ ] **Filenames sanitized** (colons → dashes, spaces → dashes)
- [ ] **Wiki links match filenames exactly** (no special characters)
- [ ] Internal links converted to wiki links `[[Page-Name]]`
- [ ] External links preserved correctly
- [ ] Images and attachments accessible
- [ ] Code blocks have correct syntax highlighting
- [ ] Tables render properly
- [ ] Home.md updated with navigation links
- [ ] All changes committed and pushed
- [ ] **Verified in browser**: All wiki links work when clicked
- [ ] User confirmed migration looks correct
