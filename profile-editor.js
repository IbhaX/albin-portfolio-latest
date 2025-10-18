// Global variables
let profileData = {
    name: "",
    title: "",
    summary: "",
    contact: {
        email: "",
        phone: "",
        location: "",
        linkedin: "",
        github: ""
    },
    skills: {
        categories: {}
    },
    experience: []
};

// DOM Elements
const profileForm = document.getElementById('profileForm');
const skillsContainer = document.getElementById('skillsContainer');
const experienceContainer = document.getElementById('experienceContainer');

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadProfile();
    setupEventListeners();
});

// Set up event listeners
function setupEventListeners() {
    profileForm.addEventListener('submit', handleFormSubmit);
}

// Load profile data from localStorage or default
async function loadProfile() {
    try {
        const savedData = localStorage.getItem('profile_data');
        if (savedData) {
            profileData = JSON.parse(savedData);
        } else {
            // Try to load from profile.json if no saved data
            try {
                const response = await fetch('profile.json');
                if (response.ok) {
                    profileData = await response.json();
                    // Save to localStorage for future use
                    localStorage.setItem('profile_data', JSON.stringify(profileData));
                }
            } catch (error) {
                console.log('Using default profile data');
            }
        }
        populateForm();
    } catch (error) {
        console.error('Error loading profile:', error);
        alert('Failed to load profile data. Using default values.');
    }
}

// Populate form with profile data
function populateForm() {
    // Basic Information
    document.getElementById('name').value = profileData.name || '';
    document.getElementById('title').value = profileData.title || '';
    document.getElementById('summary').value = profileData.summary || '';
    
    // Contact Information
    if (profileData.contact) {
        document.getElementById('email').value = profileData.contact.email || '';
        document.getElementById('phone').value = profileData.contact.phone || '';
        document.getElementById('location').value = profileData.contact.location || '';
        document.getElementById('linkedin').value = profileData.contact.linkedin ? 
            profileData.contact.linkedin.replace('linkedin.com/in/', '') : '';
        document.getElementById('github').value = profileData.contact.github ? 
            profileData.contact.github.replace('github.com/', '') : '';
    }
    
    // Skills
    renderSkills();
    
    // Experience
    renderExperience();
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;
    
    try {
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i data-lucide="loader" class="w-4 h-4 mr-2 animate-spin"></i> Saving...';
        
        // Update profile data from form
        updateProfileFromForm();
        
        // Save to localStorage
        localStorage.setItem('profile_data', JSON.stringify(profileData));
        
        // Show success message
        submitBtn.innerHTML = '<i data-lucide="check" class="w-4 h-4 mr-2"></i> Saved!';
        setTimeout(() => {
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
        }, 2000);
        
    } catch (error) {
        console.error('Error saving profile:', error);
        alert('Failed to save profile. Please try again.');
        submitBtn.innerHTML = originalBtnText;
        submitBtn.disabled = false;
    }
}

// Update profile data from form inputs
function updateProfileFromForm() {
    // Basic Information
    profileData.name = document.getElementById('name').value.trim();
    profileData.title = document.getElementById('title').value.trim();
    profileData.summary = document.getElementById('summary').value.trim();
    
    // Contact Information
    profileData.contact = profileData.contact || {};
    profileData.contact.email = document.getElementById('email').value.trim();
    profileData.contact.phone = document.getElementById('phone').value.trim();
    profileData.contact.location = document.getElementById('location').value.trim();
    
    const linkedin = document.getElementById('linkedin').value.trim();
    profileData.contact.linkedin = linkedin ? 
        (linkedin.startsWith('http') ? linkedin : `https://linkedin.com/in/${linkedin}`) : '';
        
    const github = document.getElementById('github').value.trim();
    profileData.contact.github = github ? 
        (github.startsWith('http') ? github : `https://github.com/${github}`) : '';
    
    // Note: Skills and Experience are updated in their respective render functions
}

// Skills Management
function renderSkills() {
    skillsContainer.innerHTML = '';
    
    if (!profileData.skills || !profileData.skills.categories) {
        profileData.skills = { categories: {} };
        return;
    }
    
    Object.entries(profileData.skills.categories).forEach(([category, skills], index) => {
        const skillElement = document.createElement('div');
        skillElement.className = 'mb-6 p-4 border rounded-lg';
        skillElement.innerHTML = `
            <div class="flex justify-between items-center mb-2">
                <h3 class="font-medium text-gray-700">${category.replace(/_/g, ' ').toUpperCase()}</h3>
                <button type="button" onclick="removeSkillCategory(${index})" class="text-red-500 hover:text-red-700">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div>
                <input type="text" id="skill-category-${index}" 
                       value="${category}" 
                       onchange="updateSkillCategory(${index}, this.value)"
                       class="w-full p-2 border rounded mb-2">
                <textarea id="skills-${index}" 
                          class="w-full p-2 border rounded" 
                          rows="3" 
                          onchange="updateSkills(${index}, this.value)">${Array.isArray(skills) ? skills.join(', ') : skills}</textarea>
            </div>
        `;
        skillsContainer.appendChild(skillElement);
    });
}

function addSkillCategory() {
    if (!profileData.skills.categories) {
        profileData.skills.categories = {};
    }
    
    const newCategory = `new_category_${Object.keys(profileData.skills.categories).length + 1}`;
    profileData.skills.categories[newCategory] = [];
    renderSkills();
}

function updateSkillCategory(index, newName) {
    const categories = Object.entries(profileData.skills.categories);
    if (index >= 0 && index < categories.length) {
        const [oldName, skills] = categories[index];
        if (newName && newName !== oldName) {
            delete profileData.skills.categories[oldName];
            profileData.skills.categories[newName] = skills;
            renderSkills();
        }
    }
}

function updateSkills(index, skillsText) {
    const categories = Object.entries(profileData.skills.categories);
    if (index >= 0 && index < categories.length) {
        const [category] = categories[index];
        profileData.skills.categories[category] = skillsText
            .split(',')
            .map(skill => skill.trim())
            .filter(skill => skill.length > 0);
    }
}

function removeSkillCategory(index) {
    const categories = Object.keys(profileData.skills.categories);
    if (index >= 0 && index < categories.length) {
        const categoryToRemove = categories[index];
        delete profileData.skills.categories[categoryToRemove];
        renderSkills();
    }
}

// Experience Management
function renderExperience() {
    experienceContainer.innerHTML = '';
    
    if (!Array.isArray(profileData.experience)) {
        profileData.experience = [];
    }
    
    profileData.experience.forEach((exp, index) => {
        const expElement = document.createElement('div');
        expElement.className = 'mb-6 p-4 border rounded-lg';
        expElement.innerHTML = `
            <div class="flex justify-between items-center mb-2">
                <h3 class="font-medium text-gray-700">Experience #${index + 1}</h3>
                <button type="button" onclick="removeExperience(${index})" class="text-red-500 hover:text-red-700">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="grid md:grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
                    <input type="text" value="${exp.title || ''}" 
                           onchange="updateExperienceField(${index}, 'title', this.value)"
                           class="w-full p-2 border rounded">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Company</label>
                    <input type="text" value="${exp.company || ''}" 
                           onchange="updateExperienceField(${index}, 'company', this.value)"
                           class="w-full p-2 border rounded">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Duration</label>
                    <input type="text" value="${exp.duration || ''}" 
                           onchange="updateExperienceField(${index}, 'duration', this.value)"
                           class="w-full p-2 border rounded"
                           placeholder="e.g. 01/2020 - Present">
                </div>
                <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Description (one point per line)</label>
                    <textarea onchange="updateExperienceDescription(${index}, this.value)" 
                              class="w-full p-2 border rounded" 
                              rows="4">${Array.isArray(exp.description) ? exp.description.join('\n') : ''}</textarea>
                </div>
                <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Technologies (comma separated)</label>
                    <input type="text" value="${Array.isArray(exp.tech) ? exp.tech.join(', ') : ''}" 
                           onchange="updateExperienceTech(${index}, this.value)"
                           class="w-full p-2 border rounded"
                           placeholder="e.g. Python, JavaScript, React">
                </div>
            </div>
        `;
        experienceContainer.appendChild(expElement);
    });
}

function addExperience() {
    if (!Array.isArray(profileData.experience)) {
        profileData.experience = [];
    }
    
    profileData.experience.push({
        title: '',
        company: '',
        duration: '',
        description: [],
        tech: []
    });
    
    renderExperience();
}

function updateExperienceField(index, field, value) {
    if (profileData.experience[index]) {
        profileData.experience[index][field] = value.trim();
    }
}

function updateExperienceDescription(index, description) {
    if (profileData.experience[index]) {
        profileData.experience[index].description = description
            .split('\n')
            .filter(point => point.trim().length > 0);
    }
}

function updateExperienceTech(index, techText) {
    if (profileData.experience[index]) {
        profileData.experience[index].tech = techText
            .split(',')
            .map(tech => tech.trim())
            .filter(tech => tech.length > 0);
    }
}

function removeExperience(index) {
    if (confirm('Are you sure you want to remove this experience?')) {
        profileData.experience.splice(index, 1);
        renderExperience();
    }
}

// Make functions available globally
window.addSkillCategory = addSkillCategory;
window.updateSkillCategory = updateSkillCategory;
window.updateSkills = updateSkills;
window.removeSkillCategory = removeSkillCategory;
window.addExperience = addExperience;
window.updateExperienceField = updateExperienceField;
window.updateExperienceDescription = updateExperienceDescription;
window.updateExperienceTech = updateExperienceTech;
window.removeExperience = removeExperience;

// Helper functions for form data extraction
window.getSkillsData = function() {
    return profileData.skills.categories || [];
};

window.getExperienceData = function() {
    return profileData.experience || [];
};
window.loadProfile = loadProfile;
