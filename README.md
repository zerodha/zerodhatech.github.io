# zerodha.tech

Technology blog and open-source directory for Zerodha.

## Run locally

Install [Zola 0.23.6](https://github.com/getzola/zola/releases/tag/v0.23.6), [just](https://github.com/casey/just) and [uv](https://docs.astral.sh/uv/). uv installs the project's Python. Set `ZOLA` to use a Zola binary outside `PATH`. Then run:

```sh
just serve              # preview the site with drafts on 127.0.0.1:1111
just serve 127.0.0.1 8080 # preview on another interface and port
just check              # validate content and internal Markdown links
just build              # build the complete site and RSS feeds into public/
just refresh-projects   # refresh data/projects.yml with GITHUB_TOKEN
```

Use the output of `just build` to preview the author and tag directory RSS feeds.
To add a post, create a Markdown file in `content/blog/`. Copy the front matter from a recent post for the date, authors, and tags. Author IDs map to files in `data/authors/`.

GitHub Actions builds pull requests and publishes builds from `main` to `gh-pages`. The same workflow refreshes `data/projects.yml` each Sunday. To refresh it on demand, run **Build site** on `main` with **Refresh GitHub project metadata before building** enabled.
