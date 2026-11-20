zola := env("ZOLA", "zola")

# List available recipes
default:
    @just --list

# Preview the site with drafts
serve host="127.0.0.1" port="1111":
    {{ quote(zola) }} serve --drafts --interface {{ quote(host) }} --port {{ quote(port) }} --output-dir public-dev

# Validate content and internal links
check:
    {{ quote(zola) }} check --skip-external-links

# Build the site and taxonomy RSS feeds into public/
build:
    {{ quote(zola) }} build
    uv run --locked scripts/taxonomy-feeds.py public

# Refresh GitHub project metadata
refresh-projects:
    uv run --locked scripts/update-projects.py data/projects.yml
