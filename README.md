# Albin Anthony — Portfolio

`profile.json` is the source of truth for every section of the site (basic info, contact, skills,
experience, projects, workshops, education, languages, references). `index.html` fetches it at load
time; the data inlined in `index.html` is only a fallback if the fetch fails.

## Editing content

Open `/update-profile.html` to add, edit, reorder and delete entries in any
section, or edit the raw JSON in the same page. Actions:

- **Preview** — opens `index.html?preview=1`, which renders your unsaved draft from localStorage.
- **Download JSON** — saves `profile.json`; commit it to the repo to publish.
- **Publish** — posts to the `save-profile` Netlify function, which commits `profile.json` to GitHub
  and triggers a Netlify deploy.

The edit key is derived from the current date and time in `EDIT_KEY_TZ`; see
`netlify/lib/time-key.mjs` for the exact form. The login (`login.html`, checked by
`netlify/functions/login.mjs`) uses username `admin` and the same key followed by `albin`.

Publishing needs these Netlify environment variables:

| Variable | Purpose |
| --- | --- |
| `GITHUB_TOKEN` | Fine-grained PAT for this repo with `contents: write` |
| `EDIT_KEY` | Optional static key accepted alongside the time-based one |
| `EDIT_KEY_TZ` | Optional, defaults to `Asia/Kolkata` |
| `GITHUB_REPO` | Optional, defaults to `IbhaX/albin-portfolio-latest` |
| `GITHUB_BRANCH` | Optional, defaults to `main` |
