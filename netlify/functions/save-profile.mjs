// Commits profile.json back to GitHub so the editor can publish changes.
// Required Netlify env vars: GITHUB_TOKEN (repo contents: write).
// Optional: EDIT_KEY (static fallback key), EDIT_KEY_TZ, GITHUB_REPO (owner/name),
// GITHUB_BRANCH, PROFILE_PATH.

import { timeKeys } from '../lib/time-key.mjs';

const REQUIRED_KEYS = ['name', 'title', 'summary', 'contact', 'skills'];

const json = (statusCode, body) => ({
    statusCode,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
});

export const handler = async event => {
    if (event.httpMethod !== 'POST') return json(405, { error: 'Method not allowed' });

    const editKey = process.env.EDIT_KEY;
    const token = process.env.GITHUB_TOKEN;
    if (!token) {
        return json(500, { error: 'Publishing is not configured: set GITHUB_TOKEN in Netlify.' });
    }
    const provided = (event.headers['x-edit-key'] || '').trim();
    const accepted = timeKeys().concat(editKey ? [editKey] : []);
    if (!accepted.includes(provided)) return json(401, { error: 'Invalid edit key' });

    let profile;
    try {
        ({ profile } = JSON.parse(event.body || '{}'));
    } catch {
        return json(400, { error: 'Body is not valid JSON' });
    }
    if (!profile || typeof profile !== 'object' || Array.isArray(profile)) {
        return json(400, { error: 'Missing "profile" object' });
    }
    const missing = REQUIRED_KEYS.filter(key => !(key in profile));
    if (missing.length) return json(400, { error: `Profile is missing: ${missing.join(', ')}` });

    const repo = process.env.GITHUB_REPO || 'IbhaX/albin-portfolio-latest';
    const branch = process.env.GITHUB_BRANCH || 'main';
    const path = process.env.PROFILE_PATH || 'profile.json';
    const url = `https://api.github.com/repos/${repo}/contents/${path}`;
    const githubHeaders = {
        Authorization: `Bearer ${token}`,
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'albin-portfolio-editor'
    };

    try {
        const current = await fetch(`${url}?ref=${branch}`, { headers: githubHeaders });
        if (!current.ok) {
            return json(502, { error: `Could not read ${path} from GitHub (${current.status})` });
        }
        const sha = (await current.json()).sha;

        const content = Buffer.from(JSON.stringify(profile, null, 2) + '\n').toString('base64');
        const commit = await fetch(url, {
            method: 'PUT',
            headers: { ...githubHeaders, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: 'Update profile.json from the profile editor',
                content,
                sha,
                branch
            })
        });
        if (!commit.ok) {
            const detail = await commit.text();
            return json(502, { error: `GitHub rejected the commit (${commit.status}): ${detail.slice(0, 200)}` });
        }

        return json(200, { ok: true, commit: (await commit.json()).commit?.html_url });
    } catch (error) {
        return json(502, { error: `Publish failed: ${error.message}` });
    }
};
