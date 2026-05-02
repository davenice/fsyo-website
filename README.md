# FSYO Website — Hugo Guide

## How Hugo works

Hugo is a static site generator. It takes Markdown content files and HTML templates, combines them, and produces a folder of plain HTML, CSS and image files that can be hosted anywhere — no PHP, no database, no WordPress.

The key idea: **you never edit HTML directly**. You edit Markdown files for content, or TOML config for site-wide settings. Hugo does the rest.

### Project structure

```
fsyo-website/
├── content/          # Page content as Markdown files
│   ├── _index.md     # Home page
│   ├── about.md      # About Us page
│   ├── concerts.md   # Concerts & Events
│   ├── ensembles.md  # Ensembles & Orchestras
│   └── support-us.md # Support Us
├── themes/fsyo/
│   ├── layouts/      # HTML templates
│   └── static/css/   # Stylesheets
├── static/images/    # Images served at /images/
└── hugo.toml         # Site config: title, menu, social links
```

### Content files

Each page is a Markdown file with a small block of metadata at the top called **front matter**:

```markdown
---
title: "Concerts & Events"
---

Your content here, written in Markdown.
```

Hugo converts Markdown to HTML automatically. The basics:

```markdown
## A heading

Normal paragraph text.

**Bold text** and *italic text*.

[A link](https://example.com)

- Bullet point one
- Bullet point two
```

---

## Editing the site

### Prerequisites

Install Hugo (one-time):

```bash
brew install hugo   # macOS
```

### Making changes

1. **Clone the repository** (first time only):

   ```bash
   git clone https://github.com/YOUR-ORG/fsyo-website.git
   cd fsyo-website
   ```

2. **Start the local development server:**

   ```bash
   hugo server
   ```

   The site is now live at [http://localhost:1313](http://localhost:1313) and updates instantly as you save files.

3. **Edit content** — open any file in `content/` and save. Changes appear in the browser immediately.

4. **Stop the server** with `Ctrl+C` when done.

### Editing a page

Open the relevant file in `content/` and edit the Markdown. For example, to update the concerts page:

```
content/concerts.md
```

The page title comes from the front matter. The URL comes from the filename — `concerts.md` is served at `/concerts/`.

### Changing the navigation menu

The menu is defined in `hugo.toml`. Each entry has a name, URL, and weight (ordering):

```toml
[[menu.main]]
  name = "Concerts & Events"
  url = "/concerts/"
  weight = 5
```

To add a page to the menu, add a new `[[menu.main]]` block. To reorder, change the `weight` values.

### Adding a new page

1. Create a new Markdown file in `content/`:

   ```bash
   # e.g. content/news.md
   ```

2. Add front matter and content:

   ```markdown
   ---
   title: "News"
   ---

   Your content here.
   ```

3. Add it to the menu in `hugo.toml` if needed.

The page will be available at `/news/`.

### Changing site-wide settings

Edit `hugo.toml`:

- **Title** — shown in the browser tab and header
- **Social links** — `twitter` and `facebook` params update the footer icons
- **Menu** — see above

---

## Deployment

### Option A — GitHub Pages (current setup)

Deployment is fully automatic. Every time you push to the `main` branch, GitHub Actions builds the site and publishes it:

```bash
git add content/concerts.md
git commit -m "Update concert dates"
git push
```

GitHub builds and deploys within about a minute. No manual steps needed.

The workflow is defined in `.github/workflows/hugo.yml`.

### Option B — Manual deployment to a web server

If deploying to a traditional web server (Apache, Nginx, cPanel, etc.) instead:

1. **Build the site locally:**

   ```bash
   hugo --minify
   ```

   This produces a `public/` folder containing the complete website — plain HTML, CSS and images.

2. **Upload the contents of `public/` to your server**, replacing the previous files. You can use FTP, SFTP, rsync or a file manager. The contents of `public/` should go into your web root (often `public_html/` or `www/`):

   ```bash
   # Example using rsync over SSH
   rsync -avz --delete public/ user@yourserver.com:public_html/
   ```

   Or drag and drop the contents of `public/` via an FTP client such as FileZilla.

3. **The `public/` folder is not committed to Git** (it's in `.gitignore`) — it's always regenerated from the source files, so the source in `content/` and `themes/` is the single source of truth.

> **Important:** after running `hugo --minify`, always check `public/` was freshly generated before uploading. If in doubt, delete `public/` first and re-run the build.

---

## Quick reference

| Task | Command |
| --- | --- |
| Start dev server | `hugo server` |
| Build for deployment | `hugo --minify` |
| Build output folder | `public/` |
| Page content | `content/*.md` |
| Site config and menu | `hugo.toml` |
| Templates | `themes/fsyo/layouts/` |
| Stylesheets | `themes/fsyo/static/css/` |
| Images | `static/images/` |
