// State Management
let currentStep = 1;
let generatedIdeas = [];
let selectedIdea = null;
let currentBlueprint = null;

// Initialize Mermaid.js
mermaid.initialize({
    startOnLoad: false,
    theme: 'dark',
    securityLevel: 'loose',
    fontFamily: 'Inter, sans-serif'
});

document.addEventListener('DOMContentLoaded', () => {
    initSkillsChips();
    initEventListeners();
    fetchSavedProjectsCount();
});

// SKILLS CHIPS SELECTION
function initSkillsChips() {
    const chips = document.querySelectorAll('#suggested-chips .chip-btn');
    const skillsInput = document.getElementById('skills-input');

    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            chip.classList.toggle('selected');
            const selectedSkills = Array.from(document.querySelectorAll('#suggested-chips .chip-btn.selected'))
                .map(c => c.dataset.skill);
            
            if (selectedSkills.length > 0) {
                skillsInput.value = selectedSkills.join(', ');
            }
        });
    });
}

// EVENT LISTENERS
function initEventListeners() {
    // Step 1 Form Submit
    document.getElementById('generator-form').addEventListener('submit', handleFormSubmit);

    // Back Buttons
    document.getElementById('btn-back-step1').addEventListener('click', () => switchStep(1));
    document.getElementById('btn-back-blueprint').addEventListener('click', () => switchStep(3));
    document.getElementById('btn-goto-mentor').addEventListener('click', () => switchStep(4));

    // Blueprint Tabs
    document.querySelectorAll('.bp-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            document.querySelectorAll('.bp-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            
            const target = e.currentTarget;
            target.classList.add('active');
            const panelId = target.dataset.tab;
            document.getElementById(panelId).classList.add('active');

            if (panelId === 'tab-architecture') {
                renderMermaidDiagram();
            }
        });
    });

    // Save Blueprint Button
    document.getElementById('btn-save-bp').addEventListener('click', saveCurrentProject);

    // Download Scaffold Zip Button
    const btnZip = document.getElementById('btn-download-scaffold');
    if (btnZip) btnZip.addEventListener('click', downloadScaffoldZip);

    // Export IEEE Paper Button
    const btnIeee = document.getElementById('btn-export-ieee');
    if (btnIeee) btnIeee.addEventListener('click', exportIeeePaper);
    const btnCloseIeee = document.getElementById('btn-close-ieee');
    if (btnCloseIeee) btnCloseIeee.addEventListener('click', () => {
        document.getElementById('ieee-modal').classList.add('hidden');
    });
    const btnPrintIeee = document.getElementById('btn-print-ieee');
    if (btnPrintIeee) btnPrintIeee.addEventListener('click', () => {
        const iframe = document.getElementById('ieee-frame');
        iframe.contentWindow.focus();
        iframe.contentWindow.print();
    });

    // Download Dataset CSV Button
    const btnDataset = document.getElementById('btn-download-dataset');
    if (btnDataset) btnDataset.addEventListener('click', downloadDatasetCsv);


    // Live Viva Simulator Submit
    const btnVivaSim = document.getElementById('btn-submit-viva-sim');
    if (btnVivaSim) btnVivaSim.addEventListener('click', submitVivaSimulator);

    // Saved Projects Modal
    document.getElementById('btn-saved-projects').addEventListener('click', openSavedProjectsModal);

    document.getElementById('btn-close-saved').addEventListener('click', () => {
        document.getElementById('saved-modal').classList.add('hidden');
    });

    // Mentor Prompt Chips
    document.querySelectorAll('.prompt-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.prompt-btn').forEach(b => b.classList.remove('active'));
            const target = e.currentTarget;
            target.classList.add('active');
            fetchMentorAdvice(target.dataset.prompt);
        });
    });

    // Custom Mentor Prompt
    document.getElementById('btn-ask-custom').addEventListener('click', () => {
        const text = document.getElementById('custom-mentor-input').value.trim();
        if (text) {
            fetchMentorAdvice('custom', text);
        }
    });

    // Export README Button Listeners
    const btnHeaderReadme = document.getElementById('btn-header-readme');
    if (btnHeaderReadme) btnHeaderReadme.addEventListener('click', exportReadme);

    const btnExportReadme = document.getElementById('btn-export-readme');
    if (btnExportReadme) btnExportReadme.addEventListener('click', exportReadme);

    const btnCloseReadme = document.getElementById('btn-close-readme');
    if (btnCloseReadme) btnCloseReadme.addEventListener('click', () => {
        document.getElementById('readme-modal').classList.add('hidden');
    });

    const btnCopyReadme = document.getElementById('btn-copy-readme');
    if (btnCopyReadme) btnCopyReadme.addEventListener('click', copyReadmeText);

    const btnDownloadReadmeFile = document.getElementById('btn-download-readme-file');
    if (btnDownloadReadmeFile) btnDownloadReadmeFile.addEventListener('click', downloadReadmeFile);
}

// STEP SWITCHER
function switchStep(stepNum) {
    currentStep = stepNum;
    
    // Update Wizard Tracker Header
    for (let i = 1; i <= 4; i++) {
        const wizardItem = document.getElementById(`wizard-step-${i}`);
        if (i <= stepNum) {
            wizardItem.classList.add('active');
        } else {
            wizardItem.classList.remove('active');
        }

        const section = document.getElementById(`section-step-${i}`);
        if (i === stepNum) {
            section.classList.remove('hidden');
        } else {
            section.classList.add('hidden');
        }
    }
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// STEP 1: FORM SUBMISSION -> GENERATE IDEAS
async function handleFormSubmit(e) {
    e.preventDefault();

    const domain = document.getElementById('domain-select').value;
    const category = document.getElementById('category-select').value;
    const skills = document.getElementById('skills-input').value;
    const difficulty = document.getElementById('difficulty-select').value;
    const goal = document.getElementById('goal-select').value;

    showLoading("Generating Custom Project Concepts...");

    try {
        const res = await fetch('/api/generate-ideas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ domain, category, skills, difficulty, goal })
        });
        const data = await res.json();
        hideLoading();

        if (data.success && data.ideas) {
            generatedIdeas = data.ideas;
            renderIdeaCards(generatedIdeas);
            switchStep(2);
        } else {
            alert('Error generating ideas: ' + (data.error || 'Unknown error'));
        }
    } catch (err) {
        hideLoading();
        alert('Network error generating ideas.');
    }
}

// RENDER STEP 2 IDEA CARDS
function renderIdeaCards(ideas) {
    const container = document.getElementById('ideas-container');
    container.innerHTML = '';

    ideas.forEach(idea => {
        const card = document.createElement('div');
        card.className = 'idea-card';
        card.innerHTML = `
            <div>
                <div class="idea-card-header">
                    <span class="tag-badge">${idea.domain}</span>
                    <h3>${idea.title}</h3>
                    <p class="idea-tagline">${idea.tagline}</p>
                </div>
                
                <div class="idea-body">
                    <div class="info-block">
                        <strong><i class="fa-solid fa-bullseye text-cyan"></i> Problem Statement</strong>
                        <p>${idea.problem}</p>
                    </div>
                    
                    <div class="info-block">
                        <strong><i class="fa-solid fa-wand-magic-sparkles text-violet"></i> Novelty Factor</strong>
                        <p>${idea.novelty}</p>
                    </div>

                    <div class="info-block">
                        <strong><i class="fa-solid fa-chart-line text-emerald"></i> Resume Impact</strong>
                        <p>${idea.resume_focus}</p>
                    </div>

                    <div class="tech-pills">
                        ${idea.tech_stack_preview.map(t => `<span class="pill-tech">${t}</span>`).join('')}
                    </div>
                </div>
            </div>

            <button class="btn-primary btn-sm btn-select-idea" style="margin-top: 1rem; width: 100%;">
                <i class="fa-solid fa-diagram-project"></i> Generate Full Blueprint
            </button>
        `;

        card.querySelector('.btn-select-idea').addEventListener('click', () => {
            selectedIdea = idea;
            fetchBlueprint(idea);
        });

        container.appendChild(card);
    });
}

// FETCH BLUEPRINT FOR SELECTED IDEA
async function fetchBlueprint(idea) {
    showLoading(`Generating Blueprint for ${idea.title}...`);

    try {
        const res = await fetch('/api/generate-blueprint', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ idea })
        });
        const data = await res.json();
        hideLoading();

        if (data.success && data.blueprint) {
            currentBlueprint = data.blueprint;
            populateBlueprintUI(currentBlueprint);
            switchStep(3);
            renderMermaidDiagram();
        } else {
            alert('Error generating blueprint.');
        }
    } catch (err) {
        hideLoading();
        alert('Network error fetching blueprint.');
    }
}

// POPULATE BLUEPRINT UI
function populateBlueprintUI(bp) {
    document.getElementById('bp-domain-tag').textContent = bp.domain;
    document.getElementById('bp-title').textContent = bp.title;
    document.getElementById('bp-tagline').textContent = bp.tagline;
    document.getElementById('bp-problem-statement').textContent = bp.problem_statement;

    // Tech Stack Tab
    const techContainer = document.getElementById('tech-stack-container');
    techContainer.innerHTML = '';
    for (const [key, val] of Object.entries(bp.tech_stack)) {
        const techCard = document.createElement('div');
        techCard.className = 'tech-card';
        techCard.innerHTML = `
            <h4>${key.replace('_', ' / ')}</h4>
            <p>${val}</p>
        `;
        techContainer.appendChild(techCard);
    }

    document.getElementById('req-hardware').textContent = bp.requirements.hardware;
    document.getElementById('req-software').textContent = bp.requirements.software;

    // Roadmap Tab
    const roadmapContainer = document.getElementById('roadmap-container');
    roadmapContainer.innerHTML = '';
    bp.roadmap_8_weeks.forEach(phase => {
        const card = document.createElement('div');
        card.className = 'phase-card';
        card.innerHTML = `
            <div class="phase-header">
                <span class="phase-week">${phase.week}</span>
                <h4>${phase.title}</h4>
            </div>
            <ul class="phase-tasks">
                ${phase.tasks.map(t => `
                    <li>
                        <input type="checkbox" onchange="this.parentElement.style.textDecoration = this.checked ? 'line-through' : 'none'">
                        <span>${t}</span>
                    </li>
                `).join('')}
            </ul>
        `;
        roadmapContainer.appendChild(card);
    });

    // Viva Prep Tab
    const vivaContainer = document.getElementById('viva-container');
    const vivaSelect = document.getElementById('viva-sim-q-select');
    vivaContainer.innerHTML = '';
    if (vivaSelect) vivaSelect.innerHTML = '';

    bp.viva_qa.forEach(item => {
        const card = document.createElement('div');
        card.className = 'viva-card';
        card.innerHTML = `
            <div class="viva-q"><i class="fa-solid fa-circle-question"></i> ${item.q}</div>
            <div class="viva-a"><i class="fa-solid fa-comment-dots text-emerald"></i> ${item.a}</div>
        `;
        vivaContainer.appendChild(card);

        if (vivaSelect) {
            const opt = document.createElement('option');
            opt.value = item.q;
            opt.textContent = item.q;
            vivaSelect.appendChild(opt);
        }
    });
}

// DOWNLOAD SCAFFOLD ZIP
async function downloadScaffoldZip() {
    if (!currentBlueprint) {
        alert('Please select or generate a blueprint first!');
        return;
    }

    showLoading("Packaging Project Starter Code (.zip)...");
    try {
        const res = await fetch('/api/download-scaffold', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentBlueprint)
        });
        const blob = await res.blob();
        hideLoading();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${currentBlueprint.title.replace(/[^a-zA-Z0-9_]/g, '_')}_scaffold.zip`;
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (e) {
        hideLoading();
        alert('Error downloading code scaffold zip.');
    }
}

// SUBMIT VIVA SIMULATOR
async function submitVivaSimulator() {
    if (!currentBlueprint) return;

    const q = document.getElementById('viva-sim-q-select').value;
    const ans = document.getElementById('viva-sim-answer').value.trim();

    if (!ans) {
        alert('Please type your answer to the examiner question first!');
        return;
    }

    showLoading("Evaluating Defense with AI Examiner...");

    try {
        const res = await fetch('/api/viva-grade', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question: q,
                user_answer: ans,
                project_title: currentBlueprint.title,
                skills: [currentBlueprint.tech_stack.Backend, currentBlueprint.tech_stack.Frontend]
            })
        });
        const data = await res.json();
        hideLoading();

        if (data.success && data.evaluation) {
            const ev = data.evaluation;
            const resDiv = document.getElementById('viva-sim-result');
            resDiv.classList.remove('hidden');
            resDiv.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.75rem;">
                    <span style="font-size: 1.2rem; font-weight: 700; color: var(--accent-rose);">
                        Score: ${ev.score} / ${ev.max_score} (${ev.feedback_tier})
                    </span>
                </div>
                <p style="color: #D1D5DB; margin-bottom: 0.75rem;">${ev.summary}</p>
                <div style="margin-bottom: 0.75rem;">
                    <strong style="color: var(--accent-emerald); font-size: 0.85rem;">Detected Keywords:</strong> 
                    ${ev.found_keywords.length > 0 ? ev.found_keywords.map(k => `<span class="pill-tech" style="background: rgba(16,185,129,0.2); color:#6EE7B7;">${k}</span>`).join(' ') : '<span style="color:var(--text-muted); font-size:0.85rem;">None detected</span>'}
                </div>
                <div style="margin-bottom: 0.75rem;">
                    <strong style="color: var(--accent-amber); font-size: 0.85rem;">Suggested Technical Keywords to Add:</strong> 
                    ${ev.missing_keywords.map(k => `<span class="pill-tech" style="background: rgba(245,158,11,0.2); color:#FCD34D;">${k}</span>`).join(' ')}
                </div>
                <div style="background: rgba(255,255,255,0.05); padding: 0.75rem; border-radius: var(--radius-sm); font-size: 0.88rem;">
                    <strong style="color: var(--accent-cyan);">Master Response Benchmark:</strong>
                    <p style="color: var(--text-muted); margin-top: 0.25rem;">${ev.model_answer}</p>
                </div>
            `;
        }
    } catch (e) {
        hideLoading();
        alert('Error evaluating answer.');
    }
}


// RENDER MERMAID DIAGRAM
function renderMermaidDiagram() {
    if (!currentBlueprint || !currentBlueprint.architecture_diagram) return;

    const target = document.getElementById('mermaid-target');
    target.removeAttribute('data-processed');
    target.innerHTML = currentBlueprint.architecture_diagram;

    try {
        mermaid.contentLoaded();
    } catch (e) {
        console.log('Mermaid render notice:', e);
    }
}

// SAVE CURRENT PROJECT
async function saveCurrentProject() {
    if (!currentBlueprint) return;

    try {
        const res = await fetch('/api/save-project', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentBlueprint)
        });
        const data = await res.json();
        if (data.success) {
            alert('Project Blueprint saved successfully to saved_projects.json!');
            fetchSavedProjectsCount();
        }
    } catch (e) {
        alert('Error saving project.');
    }
}

// EXPORT README
async function exportReadme() {
    if (!currentBlueprint) {
        try {
            const savedRes = await fetch('/api/saved-projects');
            const savedData = await savedRes.json();
            if (savedData.projects && savedData.projects.length > 0) {
                currentBlueprint = savedData.projects[0];
            }
        } catch (e) {}
    }

    if (!currentBlueprint) {
        alert('Please select or generate a project blueprint first!');
        return;
    }

    showLoading("Formatting GitHub README.md...");
    try {
        const res = await fetch('/api/export-readme', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentBlueprint)
        });
        const data = await res.json();
        hideLoading();

        if (data.success && data.readme) {
            document.getElementById('readme-text-area').value = data.readme;
            document.getElementById('readme-modal').classList.remove('hidden');
        } else {
            alert('Error formatting README: ' + (data.error || 'Unknown error'));
        }
    } catch (e) {
        hideLoading();
        alert('Error exporting README.');
    }
}

function copyReadmeText() {
    const area = document.getElementById('readme-text-area');
    area.select();
    navigator.clipboard.writeText(area.value);
    alert('README markdown copied to clipboard!');
}

function downloadReadmeFile() {
    const text = document.getElementById('readme-text-area').value;
    if (!text) return;
    const blob = new Blob([text], { type: 'text/markdown' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const cleanTitle = currentBlueprint ? currentBlueprint.title.replace(/[^a-zA-Z0-9_]/g, '_') : 'Project';
    a.download = `${cleanTitle}_README.md`;
    document.body.appendChild(a);
    a.click();
    a.remove();
}

// SAVED PROJECTS MODAL
async function openSavedProjectsModal() {
    try {
        const res = await fetch('/api/saved-projects');
        const data = await res.json();
        const body = document.getElementById('saved-modal-body');
        body.innerHTML = '';

        if (data.projects && data.projects.length > 0) {
            data.projects.forEach(p => {
                const safeTitle = (p.title || '').replace(/"/g, '&quot;');
                const div = document.createElement('div');
                div.className = 'viva-card';
                div.style.marginBottom = '1rem';
                div.innerHTML = `
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="tag-badge">${p.domain}</span>
                        <button class="btn-secondary btn-sm btn-delete-saved" data-title="${safeTitle}" style="cursor: pointer;"><i class="fa-solid fa-trash text-rose"></i> Delete</button>
                    </div>
                    <h3 style="margin: 0.5rem 0;">${p.title}</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">${p.tagline}</p>
                    <button class="btn-primary btn-sm btn-load-saved" style="margin-top: 0.75rem;"><i class="fa-solid fa-folder-open"></i> Open Blueprint</button>
                `;

                div.querySelector('.btn-load-saved').addEventListener('click', () => {
                    currentBlueprint = p;
                    populateBlueprintUI(currentBlueprint);
                    document.getElementById('saved-modal').classList.add('hidden');
                    switchStep(3);
                    renderMermaidDiagram();
                });

                div.querySelector('.btn-delete-saved').addEventListener('click', async (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    await deleteSavedProject(p.title);
                });

                body.appendChild(div);
            });
        } else {
            body.innerHTML = '<p style="text-align:center; color: var(--text-muted); padding: 2rem;">No saved projects yet. Click "Save Project" inside any blueprint!</p>';
        }

        document.getElementById('saved-modal').classList.remove('hidden');
    } catch (e) {
        alert('Error fetching saved projects.');
    }
}

async function deleteSavedProject(title) {
    try {
        showLoading("Deleting project...");
        const res = await fetch('/api/delete-project', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: title })
        });
        const data = await res.json();
        hideLoading();
        if (data.success) {
            await openSavedProjectsModal();
            await fetchSavedProjectsCount();
        } else {
            alert('Error deleting project: ' + (data.error || 'Failed'));
        }
    } catch (e) {
        hideLoading();
        alert('Error deleting saved project.');
    }
}

async function fetchSavedProjectsCount() {
    try {
        const res = await fetch('/api/saved-projects');
        const data = await res.json();
        if (data.projects) {
            document.getElementById('saved-count-badge').textContent = data.projects.length;
        }
    } catch (e) {}
}

// MENTOR ADVICE FETCH
async function fetchMentorAdvice(promptType, customQuestion = '') {
    if (!currentBlueprint) {
        alert('Please generate or select a project blueprint first!');
        return;
    }

    showLoading("Consulting AI Project Mentor...");

    try {
        const res = await fetch('/api/mentor-advise', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt_type: promptType,
                project_title: currentBlueprint.title,
                domain: currentBlueprint.domain,
                skills: [currentBlueprint.tech_stack.Backend, currentBlueprint.tech_stack.Frontend],
                custom_question: customQuestion
            })
        });
        const data = await res.json();
        hideLoading();

        if (data.success && data.advice) {
            renderMentorAdvice(data.advice);
        }
    } catch (e) {
        hideLoading();
        alert('Error consulting mentor.');
    }
}

function renderMentorAdvice(advice) {
    document.getElementById('mentor-welcome-state').classList.add('hidden');
    const contentArea = document.getElementById('mentor-content-area');
    contentArea.classList.remove('hidden');

    let html = `
        <h3 style="color: var(--accent-cyan); font-family: var(--font-heading); font-size: 1.3rem; margin-bottom: 0.5rem;">${advice.category}</h3>
        <p style="color: var(--text-muted); margin-bottom: 1.25rem;">${advice.headline}</p>
    `;

    advice.steps.forEach(step => {
        html += `
            <div class="mentor-step-card">
                <h4>${step.title}</h4>
                <p style="font-size: 0.9rem; color: #D1D5DB;">${step.detail}</p>
            </div>
        `;
    });

    if (advice.pro_tip) {
        html += `<div class="pro-tip-box">${advice.pro_tip}</div>`;
    }

    contentArea.innerHTML = html;
}

// LOADING SPINNER UTILS
function showLoading(msg = "Processing...") {
    document.getElementById('loading-text').textContent = msg;
    document.getElementById('loading-overlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}

// DOWNLOAD SYNTHETIC DATASET CSV
async function downloadDatasetCsv() {
    if (!currentBlueprint) {
        alert('Please select or generate a blueprint first!');
        return;
    }

    showLoading("Generating Domain Synthetic Dataset (.csv)...");
    try {
        const res = await fetch('/api/download-dataset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentBlueprint)
        });
        const blob = await res.blob();
        hideLoading();

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${currentBlueprint.title.replace(/[^a-zA-Z0-9_]/g, '_')}_dataset.csv`;
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (e) {
        hideLoading();
        alert('Error downloading dataset CSV.');
    }
}

// EXPORT IEEE PAPER MANUSCRIPT
async function exportIeeePaper() {
    if (!currentBlueprint) {
        alert('Please select or generate a blueprint first!');
        return;
    }

    showLoading("Formatting IEEE 2-Column Paper Draft...");
    try {
        const res = await fetch('/api/export-ieee-paper', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentBlueprint)
        });
        const data = await res.json();
        hideLoading();

        if (data.success && data.html) {
            const iframe = document.getElementById('ieee-frame');
            iframe.srcdoc = data.html;
            document.getElementById('ieee-modal').classList.remove('hidden');
        }
    } catch (e) {
        hideLoading();
        alert('Error exporting IEEE paper.');
    }
}

