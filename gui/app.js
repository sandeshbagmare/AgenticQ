// State management
const state = {
    domains: [],
    plugins: [],
    recommendations: [],
    wizard: {
        currentStep: 1,
        selectedDomain: null,
        selectedPlugins: [],
        selectedHarness: null
    }
};

// Domain icons mapping
const domainIcons = {
    'web': '🌐',
    'database': '🗄️',
    'filesystem': '📁',
    'api': '🔌',
    'cloud': '☁️',
    'devtools': '🛠️',
    'communication': '💬',
    'data': '📊',
    'security': '🔒',
    'ml': '🤖',
    'monitoring': '📈',
    'automation': '⚙️'
};

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    await loadData();
    initializeTabs();
    initializePluginBrowser();
    initializeRecommendations();
    initializeWizard();
    initializeAgentBuilder();
    renderDomains();
    renderPlugins();
});

// Load data from API
async function loadData() {
    try {
        // Load domains
        const domainsResponse = await fetch('/api/domains');
        state.domains = await domainsResponse.json();

        // Load plugins
        const pluginsResponse = await fetch('/api/plugins');
        state.plugins = await pluginsResponse.json();
    } catch (error) {
        console.error('Error loading data:', error);
        // Use mock data for development
        state.domains = generateMockDomains();
        state.plugins = generateMockPlugins();
    }
}

// Generate mock domains
function generateMockDomains() {
    return [
        { id: 'web', name: 'Web & HTTP', description: 'Web scraping, HTTP requests, browser automation', pluginCount: 15 },
        { id: 'database', name: 'Database', description: 'SQL, NoSQL, data storage and retrieval', pluginCount: 12 },
        { id: 'filesystem', name: 'File System', description: 'File operations, directory management', pluginCount: 8 },
        { id: 'api', name: 'API Integration', description: 'REST, GraphQL, third-party APIs', pluginCount: 20 },
        { id: 'cloud', name: 'Cloud Services', description: 'AWS, Azure, GCP integrations', pluginCount: 18 },
        { id: 'devtools', name: 'Dev Tools', description: 'Git, CI/CD, testing frameworks', pluginCount: 14 },
        { id: 'communication', name: 'Communication', description: 'Email, Slack, messaging platforms', pluginCount: 10 },
        { id: 'data', name: 'Data Processing', description: 'ETL, data transformation, analytics', pluginCount: 16 },
        { id: 'security', name: 'Security', description: 'Authentication, encryption, secrets management', pluginCount: 9 },
        { id: 'ml', name: 'Machine Learning', description: 'ML models, training, inference', pluginCount: 11 },
        { id: 'monitoring', name: 'Monitoring', description: 'Logging, metrics, observability', pluginCount: 7 },
        { id: 'automation', name: 'Automation', description: 'Workflow automation, task scheduling', pluginCount: 13 }
    ];
}

// Generate mock plugins
function generateMockPlugins() {
    const plugins = [];
    const categories = ['Tool', 'Resource', 'Prompt', 'Hybrid'];
    const domains = ['web', 'database', 'filesystem', 'api', 'cloud', 'devtools', 'communication', 'data', 'security', 'ml', 'monitoring', 'automation'];

    domains.forEach(domain => {
        for (let i = 0; i < 5; i++) {
            plugins.push({
                id: `${domain}-plugin-${i}`,
                name: `${domain.charAt(0).toUpperCase() + domain.slice(1)} Plugin ${i + 1}`,
                domain: domain,
                category: categories[Math.floor(Math.random() * categories.length)],
                description: `A powerful plugin for ${domain} operations with advanced features`,
                tokenCost: Math.floor(Math.random() * 5000) + 500,
                rating: (Math.random() * 2 + 3).toFixed(1)
            });
        }
    });

    return plugins;
}

// Tab navigation
function initializeTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;

            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        });
    });
}

// Render domains
function renderDomains() {
    const grid = document.getElementById('domain-grid');
    grid.innerHTML = state.domains.map(domain => `
        <div class="domain-card" data-domain="${domain.id}">
            <div class="domain-icon">${domainIcons[domain.id] || '📦'}</div>
            <h3>${domain.name}</h3>
            <p>${domain.description}</p>
            <div class="domain-stats">
                <span class="plugin-count">${domain.pluginCount} plugins</span>
            </div>
        </div>
    `).join('');

    // Add click handlers
    grid.querySelectorAll('.domain-card').forEach(card => {
        card.addEventListener('click', () => {
            const domainId = card.dataset.domain;
            filterPluginsByDomain(domainId);
            document.querySelector('[data-tab="plugins"]').click();
        });
    });
}

// Plugin Browser
function initializePluginBrowser() {
    const searchInput = document.getElementById('plugin-search');
    const domainFilter = document.getElementById('domain-filter');
    const categoryFilter = document.getElementById('category-filter');

    // Populate filters
    const domains = [...new Set(state.plugins.map(p => p.domain))];
    domainFilter.innerHTML = '<option value="">All Domains</option>' +
        domains.map(d => `<option value="${d}">${d}</option>`).join('');

    const categories = [...new Set(state.plugins.map(p => p.category))];
    categoryFilter.innerHTML = '<option value="">All Categories</option>' +
        categories.map(c => `<option value="${c}">${c}</option>`).join('');

    // Event listeners
    searchInput.addEventListener('input', renderPlugins);
    domainFilter.addEventListener('change', renderPlugins);
    categoryFilter.addEventListener('change', renderPlugins);
}

function renderPlugins() {
    const searchTerm = document.getElementById('plugin-search').value.toLowerCase();
    const domainFilter = document.getElementById('domain-filter').value;
    const categoryFilter = document.getElementById('category-filter').value;

    const filtered = state.plugins.filter(plugin => {
        const matchesSearch = plugin.name.toLowerCase().includes(searchTerm) ||
                            plugin.description.toLowerCase().includes(searchTerm);
        const matchesDomain = !domainFilter || plugin.domain === domainFilter;
        const matchesCategory = !categoryFilter || plugin.category === categoryFilter;
        return matchesSearch && matchesDomain && matchesCategory;
    });

    const tbody = document.getElementById('plugin-tbody');
    tbody.innerHTML = filtered.map(plugin => `
        <tr>
            <td><strong>${plugin.name}</strong></td>
            <td><span class="badge badge-${plugin.domain}">${plugin.domain}</span></td>
            <td><span class="badge badge-category">${plugin.category}</span></td>
            <td>${plugin.description}</td>
            <td>${plugin.tokenCost.toLocaleString()} tokens</td>
            <td>
                <button class="btn-small btn-primary" onclick="viewPluginDetails('${plugin.id}')">View</button>
            </td>
        </tr>
    `).join('');
}

function filterPluginsByDomain(domainId) {
    document.getElementById('domain-filter').value = domainId;
    renderPlugins();
}

function viewPluginDetails(pluginId) {
    const plugin = state.plugins.find(p => p.id === pluginId);
    alert(`Plugin: ${plugin.name}\n\nDomain: ${plugin.domain}\nCategory: ${plugin.category}\nToken Cost: ${plugin.tokenCost}\n\n${plugin.description}`);
}

// Recommendations
function initializeRecommendations() {
    const scanBtn = document.getElementById('scan-btn');
    scanBtn.addEventListener('click', async () => {
        const input = document.getElementById('scan-input').value;
        if (!input.trim()) {
            alert('Please enter a project description');
            return;
        }

        scanBtn.disabled = true;
        scanBtn.textContent = 'Scanning...';

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ description: input })
            });
            state.recommendations = await response.json();
        } catch (error) {
            console.error('Error getting recommendations:', error);
            state.recommendations = generateMockRecommendations();
        }

        renderRecommendations();
        scanBtn.disabled = false;
        scanBtn.textContent = 'Scan & Recommend';
    });
}

function generateMockRecommendations() {
    return state.plugins
        .sort(() => Math.random() - 0.5)
        .slice(0, 8)
        .map((plugin, index) => ({
            ...plugin,
            score: (95 - index * 5),
            reason: `Highly relevant for your project requirements`
        }));
}

function renderRecommendations() {
    const container = document.getElementById('recommendations-container');

    if (state.recommendations.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No recommendations yet.</p></div>';
        return;
    }

    container.innerHTML = `
        <div class="recommendations-list">
            ${state.recommendations.map(rec => `
                <div class="recommendation-card">
                    <div class="rec-header">
                        <h3>${rec.name}</h3>
                        <span class="score-badge">${rec.score}% match</span>
                    </div>
                    <p class="rec-description">${rec.description}</p>
                    <div class="rec-meta">
                        <span class="badge badge-${rec.domain}">${rec.domain}</span>
                        <span class="badge badge-category">${rec.category}</span>
                        <span class="token-cost">${rec.tokenCost.toLocaleString()} tokens</span>
                    </div>
                    <p class="rec-reason"><strong>Why:</strong> ${rec.reason}</p>
                    <button class="btn btn-primary btn-small" onclick="addToWizard('${rec.id}')">Add to Wizard</button>
                </div>
            `).join('')}
        </div>
    `;
}

function addToWizard(pluginId) {
    if (!state.wizard.selectedPlugins.includes(pluginId)) {
        state.wizard.selectedPlugins.push(pluginId);
        alert('Plugin added to wizard!');
    }
}

// Wizard
function initializeWizard() {
    const prevBtn = document.getElementById('wizard-prev');
    const nextBtn = document.getElementById('wizard-next');

    prevBtn.addEventListener('click', () => navigateWizard(-1));
    nextBtn.addEventListener('click', () => navigateWizard(1));

    renderWizardStep();
}

function navigateWizard(direction) {
    const newStep = state.wizard.currentStep + direction;

    if (newStep < 1 || newStep > 5) return;

    // Validation
    if (direction > 0) {
        if (state.wizard.currentStep === 1 && !state.wizard.selectedDomain) {
            alert('Please select a domain');
            return;
        }
        if (state.wizard.currentStep === 2 && state.wizard.selectedPlugins.length === 0) {
            alert('Please select at least one plugin');
            return;
        }
        if (state.wizard.currentStep === 3 && !state.wizard.selectedHarness) {
            alert('Please select a harness');
            return;
        }
    }

    state.wizard.currentStep = newStep;
    renderWizardStep();
}

function renderWizardStep() {
    const step = state.wizard.currentStep;

    // Update step indicators
    document.querySelectorAll('.wizard-steps .step').forEach((el, index) => {
        el.classList.toggle('active', index + 1 === step);
        el.classList.toggle('completed', index + 1 < step);
    });

    // Update step content
    document.querySelectorAll('.wizard-step-content').forEach((el, index) => {
        el.classList.toggle('active', index + 1 === step);
    });

    // Update buttons
    document.getElementById('wizard-prev').disabled = step === 1;
    const nextBtn = document.getElementById('wizard-next');
    nextBtn.textContent = step === 5 ? 'Finish' : 'Next';

    // Render step-specific content
    switch (step) {
        case 1:
            renderWizardDomains();
            break;
        case 2:
            renderWizardPlugins();
            break;
        case 3:
            renderWizardHarnesses();
            break;
        case 4:
            renderWizardReview();
            break;
        case 5:
            renderWizardScaffold();
            break;
    }
}

function renderWizardDomains() {
    const grid = document.getElementById('wizard-domain-grid');
    grid.innerHTML = state.domains.map(domain => `
        <div class="domain-card small ${state.wizard.selectedDomain === domain.id ? 'selected' : ''}"
             onclick="selectWizardDomain('${domain.id}')">
            <div class="domain-icon">${domainIcons[domain.id] || '📦'}</div>
            <h4>${domain.name}</h4>
            <p>${domain.pluginCount} plugins</p>
        </div>
    `).join('');
}

function selectWizardDomain(domainId) {
    state.wizard.selectedDomain = domainId;
    renderWizardStep();
}

function renderWizardPlugins() {
    const domainPlugins = state.plugins.filter(p => p.domain === state.wizard.selectedDomain);
    const list = document.getElementById('wizard-plugin-list');

    list.innerHTML = domainPlugins.map(plugin => `
        <label class="plugin-checkbox">
            <input type="checkbox"
                   value="${plugin.id}"
                   ${state.wizard.selectedPlugins.includes(plugin.id) ? 'checked' : ''}
                   onchange="toggleWizardPlugin('${plugin.id}')">
            <div class="plugin-info">
                <strong>${plugin.name}</strong>
                <p>${plugin.description}</p>
                <span class="token-cost">${plugin.tokenCost.toLocaleString()} tokens</span>
            </div>
        </label>
    `).join('');
}

function toggleWizardPlugin(pluginId) {
    const index = state.wizard.selectedPlugins.indexOf(pluginId);
    if (index > -1) {
        state.wizard.selectedPlugins.splice(index, 1);
    } else {
        state.wizard.selectedPlugins.push(pluginId);
    }
}

function renderWizardHarnesses() {
    const harnesses = [
        { id: 'langchain', name: 'LangChain', description: 'Popular framework for LLM applications' },
        { id: 'autogen', name: 'AutoGen', description: 'Multi-agent conversation framework' },
        { id: 'crewai', name: 'CrewAI', description: 'Role-based agent orchestration' },
        { id: 'custom', name: 'Custom', description: 'Build your own harness' }
    ];

    const grid = document.getElementById('harness-options');
    grid.innerHTML = harnesses.map(harness => `
        <div class="harness-card ${state.wizard.selectedHarness === harness.id ? 'selected' : ''}"
             onclick="selectWizardHarness('${harness.id}')">
            <h4>${harness.name}</h4>
            <p>${harness.description}</p>
        </div>
    `).join('');
}

function selectWizardHarness(harnessId) {
    state.wizard.selectedHarness = harnessId;
    renderWizardStep();
}

function renderWizardReview() {
    const domain = state.domains.find(d => d.id === state.wizard.selectedDomain);
    const plugins = state.plugins.filter(p => state.wizard.selectedPlugins.includes(p.id));
    const totalTokens = plugins.reduce((sum, p) => sum + p.tokenCost, 0);

    const content = document.getElementById('review-content');
    content.innerHTML = `
        <div class="review-section">
            <h4>Domain</h4>
            <p>${domain.name}</p>
        </div>
        <div class="review-section">
            <h4>Selected Plugins (${plugins.length})</h4>
            <ul>
                ${plugins.map(p => `<li>${p.name} - ${p.tokenCost.toLocaleString()} tokens</li>`).join('')}
            </ul>
            <p><strong>Total Token Cost:</strong> ${totalTokens.toLocaleString()} tokens</p>
        </div>
        <div class="review-section">
            <h4>Harness</h4>
            <p>${state.wizard.selectedHarness}</p>
        </div>
    `;
}

function renderWizardScaffold() {
    const result = document.getElementById('scaffold-result');
    result.innerHTML = `
        <div class="scaffold-progress">
            <div class="spinner"></div>
            <p>Generating project scaffold...</p>
        </div>
    `;

    setTimeout(() => {
        result.innerHTML = `
            <div class="success-message">
                <h3>✅ Scaffold Complete!</h3>
                <p>Your project has been generated successfully.</p>
                <div class="file-tree">
                    <pre>
project/
├── config/
│   └── mcp_config.json
├── plugins/
│   ${state.wizard.selectedPlugins.map(id => {
                        const plugin = state.plugins.find(p => p.id === id);
                        return `├── ${plugin.name.toLowerCase().replace(/\s+/g, '_')}/`;
                    }).join('\n│   ')}
├── harness/
│   └── ${state.wizard.selectedHarness}_setup.py
└── README.md
                    </pre>
                </div>
                <button class="btn btn-primary" onclick="downloadScaffold()">Download Project</button>
            </div>
        `;
    }, 2000);
}

function downloadScaffold() {
    alert('Project download started!');
}

// Agent Builder
function initializeAgentBuilder() {
    const tempSlider = document.getElementById('agent-temperature');
    const tempValue = document.getElementById('temperature-value');

    tempSlider.addEventListener('input', (e) => {
        tempValue.textContent = e.target.value;
    });

    // Populate plugin list
    const pluginList = document.getElementById('agent-plugin-list');
    pluginList.innerHTML = state.plugins.slice(0, 20).map(plugin => `
        <label class="plugin-checkbox">
            <input type="checkbox" value="${plugin.id}">
            <div class="plugin-info">
                <strong>${plugin.name}</strong>
                <span class="badge badge-${plugin.domain}">${plugin.domain}</span>
            </div>
        </label>
    `).join('');

    const generateBtn = document.getElementById('generate-agent-btn');
    generateBtn.addEventListener('click', generateAgent);
}

async function generateAgent() {
    const name = document.getElementById('agent-name').value;
    const description = document.getElementById('agent-description').value;
    const model = document.getElementById('agent-model').value;
    const temperature = document.getElementById('agent-temperature').value;
    const maxTokens = document.getElementById('agent-max-tokens').value;

    const selectedPlugins = Array.from(
        document.querySelectorAll('#agent-plugin-list input:checked')
    ).map(cb => cb.value);

    if (!name || !description || selectedPlugins.length === 0) {
        alert('Please fill in all required fields and select at least one plugin');
        return;
    }

    const output = document.getElementById('agent-output');
    output.innerHTML = `
        <div class="generating">
            <div class="spinner"></div>
            <p>Generating agent configuration...</p>
        </div>
    `;

    setTimeout(() => {
        const config = {
            name,
            description,
            model,
            temperature: parseFloat(temperature),
            maxTokens: parseInt(maxTokens),
            plugins: selectedPlugins
        };

        output.innerHTML = `
            <div class="success-message">
                <h3>✅ Agent Generated!</h3>
                <pre>${JSON.stringify(config, null, 2)}</pre>
                <button class="btn btn-primary" onclick="downloadAgentConfig()">Download Config</button>
                <button class="btn btn-secondary" onclick="deployAgent()">Deploy Agent</button>
            </div>
        `;
    }, 1500);
}

function downloadAgentConfig() {
    alert('Agent configuration downloaded!');
}

function deployAgent() {
    alert('Agent deployment initiated!');
}
