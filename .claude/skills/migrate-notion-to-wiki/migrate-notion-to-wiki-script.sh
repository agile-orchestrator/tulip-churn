#!/bin/bash
# Migration script for Notion → GitHub Wiki
# Based on .claude/skills/migrate-notion-to-wiki/SKILL.md

set -e  # Exit on error

REPO_OWNER="agile-orchestrator"
REPO_NAME="tulip-churn"
WIKI_EXPORT_DIR="wiki-export"

echo "🌷 Tulip Bank - Notion to Wiki Migration Script"
echo "================================================"
echo ""

# Step 1: Check prerequisites
echo "📋 Step 1: Checking prerequisites..."
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found. Install: https://cli.github.com/"
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub. Run: gh auth login"
    exit 1
fi

echo "✅ Prerequisites OK"
echo ""

# Step 2: Create export directory
echo "📂 Step 2: Creating export directory..."
mkdir -p "$WIKI_EXPORT_DIR"
echo "✅ Created $WIKI_EXPORT_DIR/"
echo ""

# Step 3: Fetch Notion pages
echo "📥 Step 3: Fetching Notion pages..."
echo "⚠️  This requires the Notion MCP server to be connected."
echo "   If you see timeouts, run: /mcp connect notion"
echo ""
echo "🔄 Fetching pages via Notion MCP (manual step required)..."
echo "   Use mcp__notion__notion-fetch for each page URL:"
echo "   - <notion-main-page-url> (main page)"
echo "   - Child pages: Project Overview, Data Dictionary, DoR, DoD, ADR-001, Model Card, How We Work"
echo ""
echo "⏸️  Pausing for manual Notion fetch..."
read -p "Press Enter once you've fetched all Notion pages and created markdown files in $WIKI_EXPORT_DIR/"
echo ""

# Step 4: Validate export files
echo "🔍 Step 4: Validating export files..."
REQUIRED_FILES=(
    "Home.md"
    "Project-Overview.md"
    "Data-Dictionary.md"
    "Definition-of-Ready.md"
    "Definition-of-Done.md"
    "ADR-001-Use-FastAPI-for-the-scoring-service.md"
    "Model-Card-Template.md"
    "How-We-Work.md"
    "_Sidebar.md"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$WIKI_EXPORT_DIR/$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "❌ Missing required files:"
    for file in "${MISSING_FILES[@]}"; do
        echo "   - $file"
    done
    echo ""
    echo "Please create these files in $WIKI_EXPORT_DIR/ and run again."
    exit 1
fi

echo "✅ All required wiki pages present"
echo ""

# Step 5: Verify no confidential content
echo "🔒 Step 5: Confidential content check..."
echo "⚠️  Manual review required!"
echo "   Check each file for:"
echo "   - Customer data (names, IDs, account numbers)"
echo "   - Internal compliance details"
echo "   - Personal data from meeting notes"
echo ""
read -p "Have you reviewed all files for confidential content? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Please review files for confidential content first."
    exit 1
fi
echo "✅ Confidential content review complete"
echo ""

# Step 6: Clone wiki repository
echo "📦 Step 6: Cloning wiki repository..."
WIKI_DIR="${REPO_NAME}.wiki"
if [ -d "$WIKI_DIR" ]; then
    echo "⚠️  Wiki directory already exists. Removing..."
    rm -rf "$WIKI_DIR"
fi

gh repo clone "${REPO_OWNER}/${WIKI_DIR}" || {
    echo "❌ Failed to clone wiki. Has it been initialized?"
    echo "   Create the first page via GitHub UI:"
    echo "   https://github.com/${REPO_OWNER}/${REPO_NAME}/wiki"
    exit 1
}
echo "✅ Wiki repository cloned"
echo ""

# Step 7: Copy files to wiki
echo "📋 Step 7: Copying wiki pages..."
cp "$WIKI_EXPORT_DIR"/*.md "$WIKI_DIR/"
echo "✅ Files copied to wiki repo"
echo ""

# Step 8: Commit and push
echo "💾 Step 8: Committing changes..."
cd "$WIKI_DIR"
git add .
git commit -m "docs: migrate Tulip Bank documentation from Notion

- Add Home page with project overview and links
- Add Project Overview with business problem and objectives
- Add Data Dictionary with raw columns and engineered features
- Add Definition of Ready with PBI and bug criteria
- Add Definition of Done with code, model, and documentation requirements
- Add ADR-001: Use FastAPI for the scoring service
- Add Model Card Template for compliance review
- Add How We Work with team, sprint cadence, and tools
- Add _Sidebar.md for navigation

Migrated from Notion using the Notion MCP server.
Addresses #24"

echo "✅ Changes committed"
echo ""

echo "🚀 Step 9: Pushing to GitHub..."
git push origin master
cd ..
echo "✅ Wiki published!"
echo ""

# Step 10: Update repo files
echo "📝 Step 10: Updating repo file references..."
echo "⚠️  Manual step required:"
echo "   Update these files to reference wiki instead of Notion:"
echo "   - CLAUDE.md"
echo "   - AGENTS.md"
echo "   - README.md"
echo "   - .claude/commands/*.md (4 files)"
echo "   - .claude/skills/*/SKILL.md (2 files)"
echo "   - .github/ISSUE_TEMPLATE/epic.yml"
echo "   - .github/pull_request_template.md"
echo "   - Remove 'notion' from .mcp.json"
echo ""
echo "   Search for Notion references:"
echo "   git grep -il notion"
echo ""
read -p "Press Enter once you've updated all repo file references..."
echo ""

# Step 11: Final verification
echo "✅ Step 11: Final verification..."
echo ""
echo "🎉 Migration complete!"
echo ""
echo "📋 Next steps:"
echo "1. Verify wiki at: https://github.com/${REPO_OWNER}/${REPO_NAME}/wiki"
echo "2. Click through all links to ensure they work"
echo "3. Run: git grep -il notion (should only show archived references)"
echo "4. Commit repo file changes to your feature branch"
echo "5. Open PR with: gh pr create"
echo ""
echo "📌 Notion archival:"
echo "   Mark Notion space as read-only with link to wiki"
echo "   Do NOT delete Notion pages"
