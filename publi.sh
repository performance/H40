#!/usr/bin/env bash
# publi.sh — Full build and deploy for Hanuman Chalisa Study Guide
# Run from the repo root. See CONTRIBUTING.md for step-by-step details.
set -e  # stop on first error

if [[ "$1" != "--local" && "$1" != "--github" ]]; then
    echo "Usage: ./publi.sh [--local | --github]"
    echo "  --local   : Build PDF, extract JSON data, and compile web app locally."
    echo "  --github  : Execute local build + commit to release-v1 and deploy to gh-pages."
    exit 1
fi

echo "📄 Step 1/5 — Compiling PDF (xelatex, 2 passes)..."
xelatex -interaction=nonstopmode main.tex > /dev/null || true
xelatex -interaction=nonstopmode main.tex > /dev/null || true
[ -f main.pdf ] || { echo "❌ xelatex failed — main.pdf not produced"; exit 1; }
cp main.pdf web/static/Hanuman_Chalisa_Study_Guide.pdf
echo "    ✓ main.pdf → web/static/"

echo "🐍 Step 2/5 — Extracting verse data from LaTeX..."
python3 build_web_data.py
python3 build_static_data.py
echo "    ✓ web_data/ generated"

echo "📦 Step 3/5 — Syncing data into SvelteKit app..."
cp -r web_data/verses web/src/lib/data/
cp web_data/index.json web/src/lib/data/index.json
echo "    ✓ web/src/lib/data/ updated"

echo "🏗️  Step 4/5 — Building web app..."
cd web && BASE_PATH=/H40 npm run build > /dev/null && cd ..
echo "    ✓ web/build/ ready (base path: /H40)"

if [[ "$1" == "--local" ]]; then
    echo ""
    echo "✅ Local build complete! Run 'cd web && npm run dev' to preview."
    exit 0
fi

echo "📝 Step 5/5 — Committing and pushing..."
git add -A
git commit -m "chore: publish — rebuild PDF, JSON data, and web app" || echo "    (nothing to commit)"

echo ""
echo "Pushing source branch (release-v1)..."
git push origin release-v1

echo "Pushing website (gh-pages)..."
REMOTE_URL=$(git remote get-url origin)
cd web/build
git init -b gh-pages-deploy > /dev/null 2>&1
git add -A > /dev/null
git commit -m "deploy: $(date '+%Y-%m-%d %H:%M')" > /dev/null
git push -f "$REMOTE_URL" HEAD:gh-pages
cd ../..
rm -rf web/build/.git

echo ""
echo "✅ Done! Source → release-v1 | Website → gh-pages"
