// Checks the admin login. The password is the edit key followed by "albin",
// i.e. MMyyHHmm + "albin" in EDIT_KEY_TZ.
import { timeKeys } from '../lib/time-key.mjs';

const USERNAME = 'admin';
const SUFFIX = 'albin';

const json = (statusCode, body) => ({
    statusCode,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
});

export const handler = async event => {
    if (event.httpMethod !== 'POST') return json(405, { error: 'Method not allowed' });

    let username;
    let password;
    try {
        ({ username, password } = JSON.parse(event.body || '{}'));
    } catch {
        return json(400, { error: 'Body is not valid JSON' });
    }

    const accepted = timeKeys().map(key => key + SUFFIX);
    const valid = String(username || '').trim() === USERNAME && accepted.includes(String(password || '').trim());
    return valid ? json(200, { ok: true }) : json(401, { error: 'Invalid credentials' });
};
