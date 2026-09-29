// Profile editor: full add / update / delete over profile.json.
// profile.json is the source of truth; the editor loads it, edits an in-memory
// copy, and writes it back (download or publish through the Netlify function).

const EMPTY_PROFILE = {
    name: '',
    title: '',
    summary: '',
    contact: { email: '', phone: '', location: '', linkedin: '', github: '' },
    skills: { categories: {} },
    experience: [],
    projects: [],
    workshops: [],
    education: [],
    languages: [],
    references: []
};

const SECTIONS = {
    experience: {
        singular: 'Experience',
        title: item => item.title || 'New role',
        blank: { icon: 'briefcase', title: '', company: '', duration: '', description: [], tech: [] },
        fields: [
            { key: 'title', label: 'Title' },
            { key: 'company', label: 'Company' },
            { key: 'duration', label: 'Duration', placeholder: 'e.g. 01/2020 - Present' },
            { key: 'icon', label: 'Lucide icon name', placeholder: 'e.g. shield' },
            { key: 'description', label: 'Description (one bullet per line)', type: 'lines', rows: 5, full: true },
            { key: 'tech', label: 'Technologies (comma separated)', type: 'csv', full: true }
        ]
    },
    projects: {
        singular: 'Project',
        title: item => item.name || 'New project',
        blank: { name: '', description: '', tech: '', link: '' },
        fields: [
            { key: 'name', label: 'Name', full: true },
            { key: 'description', label: 'Description', type: 'textarea', rows: 5, full: true },
            { key: 'tech', label: 'Tech (comma separated text)', full: true },
            { key: 'link', label: 'Link', placeholder: 'https://…', full: true }
        ]
    },
    workshops: {
        singular: 'Workshop / Talk',
        itemType: 'string',
        title: item => item || 'New entry',
        blank: '',
        fields: [{ key: '', label: 'Description', type: 'textarea', rows: 2, full: true }]
    },
    education: {
        singular: 'Education',
        title: item => item.name || 'New qualification',
        blank: { name: '', institution: '', year: '' },
        fields: [
            { key: 'name', label: 'Qualification' },
            { key: 'institution', label: 'Institution' },
            { key: 'year', label: 'Year' }
        ]
    },
    languages: {
        singular: 'Language',
        title: item => item.name || 'New language',
        blank: { name: '', proficiency: '' },
        fields: [
            { key: 'name', label: 'Language' },
            { key: 'proficiency', label: 'Proficiency' }
        ]
    },
    references: {
        singular: 'Reference',
        title: item => item.name || 'New reference',
        blank: { quote: '', name: '', role: '', company: '', link: '' },
        fields: [
            { key: 'quote', label: 'What they said about you', type: 'textarea', rows: 4, full: true },
            { key: 'name', label: 'Reviewer name' },
            { key: 'role', label: 'Reviewer title' },
            { key: 'company', label: 'Company (optional)' },
            { key: 'link', label: 'Profile link (optional)', placeholder: 'https://linkedin.com/in/…' }
        ]
    }
};

const BASIC_FIELDS = ['name', 'title', 'summary'];
const CONTACT_FIELDS = ['email', 'phone', 'location', 'linkedin', 'github'];
const DRAFT_KEY = 'profile_draft';

let profileData = structuredClone(EMPTY_PROFILE);
let publishedData = structuredClone(EMPTY_PROFILE);

// --- data helpers ---

const isDirty = () => JSON.stringify(profileData) !== JSON.stringify(publishedData);

function normalize(data) {
    const merged = { ...structuredClone(EMPTY_PROFILE), ...data };
    merged.contact = { ...EMPTY_PROFILE.contact, ...(data.contact || {}) };
    merged.skills = { categories: { ...((data.skills || {}).categories || {}) } };
    Object.keys(SECTIONS).forEach(key => {
        if (!Array.isArray(merged[key])) merged[key] = [];
    });
    return merged;
}

async function loadProfile({ keepDraft = true } = {}) {
    const response = await fetch(`profile.json?t=${Date.now()}`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`profile.json returned ${response.status}`);
    publishedData = normalize(await response.json());
    profileData = structuredClone(publishedData);

    const draft = keepDraft && localStorage.getItem(DRAFT_KEY);
    if (draft) {
        try {
            const parsed = normalize(JSON.parse(draft));
            if (JSON.stringify(parsed) !== JSON.stringify(publishedData) &&
                confirm('You have unsaved changes from a previous session. Restore them?')) {
                profileData = parsed;
            } else {
                localStorage.removeItem(DRAFT_KEY);
            }
        } catch (error) {
            localStorage.removeItem(DRAFT_KEY);
        }
    }
    renderAll();
}

function touch() {
    localStorage.setItem(DRAFT_KEY, JSON.stringify(profileData));
    const jsonView = document.getElementById('jsonView');
    if (jsonView && document.activeElement !== jsonView) {
        jsonView.value = JSON.stringify(profileData, null, 2);
    }
    const indicator = document.getElementById('dirtyIndicator');
    if (indicator) indicator.classList.toggle('hidden', !isDirty());
}

// --- generic field builders ---

function labelled(labelText, control, full) {
    const wrapper = document.createElement('div');
    if (full) wrapper.className = 'md:col-span-2';
    const label = document.createElement('label');
    label.className = 'block text-sm font-medium text-gray-300 mb-1';
    label.textContent = labelText;
    wrapper.append(label, control);
    return wrapper;
}

function makeControl(field, value, onChange) {
    const control = document.createElement(field.type === 'textarea' || field.type === 'lines' ? 'textarea' : 'input');
    control.className = 'w-full px-3 py-2 border border-gray-600 rounded-md';
    if (control.tagName === 'TEXTAREA') control.rows = field.rows || 3;
    if (field.placeholder) control.placeholder = field.placeholder;

    if (field.type === 'lines') control.value = (value || []).join('\n');
    else if (field.type === 'csv') control.value = (value || []).join(', ');
    else control.value = value || '';

    control.addEventListener('input', () => {
        if (field.type === 'lines') {
            onChange(control.value.split('\n').filter(line => line.trim().length));
        } else if (field.type === 'csv') {
            onChange(control.value.split(',').map(part => part.trim()).filter(Boolean));
        } else {
            onChange(control.value);
        }
    });
    return control;
}

function itemCard(sectionKey, index, headingText) {
    const card = document.createElement('div');
    card.className = 'mb-5 p-3 sm:p-4 rounded-lg border border-gray-700 bg-gray-900/40';

    const header = document.createElement('div');
    header.className = 'flex justify-between items-center mb-3 gap-2';

    const heading = document.createElement('h3');
    heading.className = 'font-medium text-gray-200 truncate';
    heading.textContent = `${index + 1}. ${headingText}`;

    const controls = document.createElement('div');
    controls.className = 'flex items-center gap-2 shrink-0';
    controls.append(
        iconButton('↑', 'Move up', () => moveItem(sectionKey, index, -1), 'text-gray-400 hover:text-cyan-300'),
        iconButton('↓', 'Move down', () => moveItem(sectionKey, index, 1), 'text-gray-400 hover:text-cyan-300'),
        iconButton('Delete', 'Delete', () => deleteItem(sectionKey, index), 'text-red-400 hover:text-red-300 text-sm')
    );

    header.append(heading, controls);
    card.append(header);
    return card;
}

function iconButton(text, title, onClick, className) {
    const button = document.createElement('button');
    button.type = 'button';
    button.title = title;
    button.textContent = text;
    button.className = `px-2 py-1 rounded ${className}`;
    button.addEventListener('click', onClick);
    return button;
}

// --- section rendering ---

function renderAll() {
    BASIC_FIELDS.forEach(key => {
        const input = document.getElementById(key);
        if (input) input.value = profileData[key] || '';
    });
    CONTACT_FIELDS.forEach(key => {
        const input = document.getElementById(key);
        if (input) input.value = profileData.contact[key] || '';
    });
    renderSkills();
    Object.keys(SECTIONS).forEach(renderSection);
    touch();
    if (window.lucide) lucide.createIcons();
}

function renderSection(sectionKey) {
    const container = document.getElementById(`${sectionKey}Container`);
    if (!container) return;
    const config = SECTIONS[sectionKey];
    container.innerHTML = '';

    if (!profileData[sectionKey].length) {
        const empty = document.createElement('p');
        empty.className = 'text-gray-500 text-sm';
        empty.textContent = 'Nothing here yet.';
        container.append(empty);
    }

    profileData[sectionKey].forEach((item, index) => {
        const card = itemCard(sectionKey, index, config.title(item));
        const grid = document.createElement('div');
        grid.className = 'grid md:grid-cols-2 gap-4';

        config.fields.forEach(field => {
            const value = config.itemType === 'string' ? item : item[field.key];
            const control = makeControl(field, value, newValue => {
                if (config.itemType === 'string') profileData[sectionKey][index] = newValue;
                else profileData[sectionKey][index][field.key] = newValue;
                touch();
            });
            grid.append(labelled(field.label, control, field.full));
        });

        card.append(grid);
        container.append(card);
    });
}

function addItem(sectionKey) {
    const config = SECTIONS[sectionKey];
    profileData[sectionKey].push(structuredClone(config.blank));
    renderSection(sectionKey);
    touch();
}

function deleteItem(sectionKey, index) {
    if (!confirm(`Delete this ${SECTIONS[sectionKey].singular.toLowerCase()}?`)) return;
    profileData[sectionKey].splice(index, 1);
    renderSection(sectionKey);
    touch();
}

function moveItem(sectionKey, index, offset) {
    const target = index + offset;
    const list = profileData[sectionKey];
    if (target < 0 || target >= list.length) return;
    [list[index], list[target]] = [list[target], list[index]];
    renderSection(sectionKey);
    touch();
}

// --- skills (object of category -> string[]) ---

function renderSkills() {
    const container = document.getElementById('skillsContainer');
    if (!container) return;
    container.innerHTML = '';

    const categories = Object.entries(profileData.skills.categories);
    if (!categories.length) {
        const empty = document.createElement('p');
        empty.className = 'text-gray-500 text-sm';
        empty.textContent = 'No skill categories yet.';
        container.append(empty);
    }

    categories.forEach(([category, skills], index) => {
        const card = document.createElement('div');
        card.className = 'mb-5 p-3 sm:p-4 rounded-lg border border-gray-700 bg-gray-900/40';

        const header = document.createElement('div');
        header.className = 'flex justify-between items-center mb-3';
        const heading = document.createElement('h3');
        heading.className = 'font-medium text-gray-200';
        heading.textContent = category.replace(/_/g, ' ').toUpperCase();
        header.append(heading, iconButton('Delete', 'Delete category', () => {
            if (!confirm(`Delete the "${category}" category?`)) return;
            delete profileData.skills.categories[category];
            renderSkills();
            touch();
        }, 'text-red-400 hover:text-red-300 text-sm'));
        card.append(header);

        const nameInput = document.createElement('input');
        nameInput.className = 'w-full px-3 py-2 border border-gray-600 rounded-md mb-2';
        nameInput.value = category;
        nameInput.addEventListener('change', () => {
            const newName = nameInput.value.trim();
            if (!newName || newName === category) return;
            const entries = Object.entries(profileData.skills.categories);
            entries[index] = [newName, profileData.skills.categories[category]];
            profileData.skills.categories = Object.fromEntries(entries);
            renderSkills();
            touch();
        });

        const skillsInput = document.createElement('textarea');
        skillsInput.className = 'w-full px-3 py-2 border border-gray-600 rounded-md';
        skillsInput.rows = 3;
        skillsInput.value = (Array.isArray(skills) ? skills : [skills]).join(', ');
        skillsInput.addEventListener('input', () => {
            profileData.skills.categories[category] = skillsInput.value
                .split(',').map(skill => skill.trim()).filter(Boolean);
            touch();
        });

        card.append(labelled('Category key', nameInput), labelled('Skills (comma separated)', skillsInput));
        container.append(card);
    });
}

function addSkillCategory() {
    const name = (prompt('Category key (e.g. cloud_devops):') || '').trim();
    if (!name) return;
    if (profileData.skills.categories[name]) {
        alert('That category already exists.');
        return;
    }
    profileData.skills.categories[name] = [];
    renderSkills();
    touch();
}

// --- basic / contact binding ---

function bindSimpleFields() {
    BASIC_FIELDS.forEach(key => {
        const input = document.getElementById(key);
        input?.addEventListener('input', () => {
            profileData[key] = input.value;
            touch();
        });
    });
    CONTACT_FIELDS.forEach(key => {
        const input = document.getElementById(key);
        input?.addEventListener('input', () => {
            profileData.contact[key] = input.value;
            touch();
        });
    });
}

// --- output: raw JSON, preview, download, publish ---

function applyJsonView() {
    const jsonView = document.getElementById('jsonView');
    try {
        profileData = normalize(JSON.parse(jsonView.value));
        renderAll();
        setStatus('JSON applied to the form.', 'ok');
    } catch (error) {
        setStatus(`Invalid JSON: ${error.message}`, 'error');
    }
}

function downloadJson() {
    const blob = new Blob([JSON.stringify(profileData, null, 2) + '\n'], { type: 'application/json' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'profile.json';
    link.click();
    URL.revokeObjectURL(link.href);
    setStatus('profile.json downloaded — commit it to the repo to publish.', 'ok');
}

function previewSite() {
    localStorage.setItem(DRAFT_KEY, JSON.stringify(profileData));
    window.open('index.html?preview=1', '_blank');
}

async function publishChanges() {
    const editKey = document.getElementById('editKey').value.trim();
    if (!editKey) {
        setStatus('Enter your edit key to publish.', 'error');
        return;
    }
    const button = document.getElementById('publishBtn');
    button.disabled = true;
    setStatus('Publishing to GitHub…', 'info');

    try {
        const response = await fetch('/.netlify/functions/save-profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'x-edit-key': editKey },
            body: JSON.stringify({ profile: profileData })
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(result.error || `Request failed (${response.status})`);

        publishedData = structuredClone(profileData);
        localStorage.removeItem(DRAFT_KEY);
        touch();
        setStatus('Published. Netlify is redeploying — the site updates in about a minute.', 'ok');
    } catch (error) {
        setStatus(`Publish failed: ${error.message}. You can still download profile.json and commit it manually.`, 'error');
    } finally {
        button.disabled = false;
    }
}

function setStatus(message, kind) {
    const status = document.getElementById('statusMessage');
    if (!status) return;
    const colors = { ok: 'text-green-400', error: 'text-red-400', info: 'text-cyan-400' };
    status.className = `text-sm ${colors[kind] || 'text-gray-300'}`;
    status.textContent = message;
}

// --- init ---

function setupEditor() {
    bindSimpleFields();

    Object.keys(SECTIONS).forEach(sectionKey => {
        document.getElementById(`add-${sectionKey}`)?.addEventListener('click', () => addItem(sectionKey));
    });
    document.getElementById('add-skills')?.addEventListener('click', addSkillCategory);
    document.getElementById('applyJsonBtn')?.addEventListener('click', applyJsonView);
    document.getElementById('downloadBtn')?.addEventListener('click', downloadJson);
    document.getElementById('previewBtn')?.addEventListener('click', previewSite);
    document.getElementById('publishBtn')?.addEventListener('click', publishChanges);
    document.getElementById('reloadBtn')?.addEventListener('click', () => {
        if (isDirty() && !confirm('Discard your unsaved changes and reload profile.json?')) return;
        localStorage.removeItem(DRAFT_KEY);
        loadProfile({ keepDraft: false }).catch(error => setStatus(error.message, 'error'));
    });

    window.addEventListener('beforeunload', event => {
        if (isDirty()) event.preventDefault();
    });

    loadProfile().catch(error => setStatus(`Could not load profile.json: ${error.message}`, 'error'));
}

window.loadProfile = loadProfile;
window.setupEditor = setupEditor;
