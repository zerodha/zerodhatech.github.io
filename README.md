# zerodha.tech

Technology blog and open-source directory for Zerodha.

## Run locally

Install [Zola 0.23.6](https://github.com/getzola/zola/releases/tag/v0.23.6) and Python 3.9 or later, then run:

```sh
make serve         # preview the site, including drafts
make check         # validate content and internal Markdown links
make build         # build the complete site and RSS feeds into public/
```

Use the output of `make build` to preview the author and tag directory RSS feeds.
To add a post, create a Markdown file in `content/blog/`. Copy the front matter from a recent post for the date, authors, and tags. Author IDs map to files in `data/authors/`.

GitHub Actions builds pull requests and publishes builds from `main` to `gh-pages`. The same workflow refreshes `data/projects.yml` each Sunday. To refresh it on demand, run **Build site** on `main` with **Refresh GitHub project metadata before building** enabled.
