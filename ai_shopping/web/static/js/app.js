/* AI Shopping — Frontend Logic */

const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultsGrid = document.getElementById('resultsGrid');
const emptyState = document.getElementById('emptyState');
const loading = document.getElementById('loading');
const errorsDiv = document.getElementById('errors');
const searchMeta = document.getElementById('searchMeta');
const parsedIntent = document.getElementById('parsedIntent');
const resultCount = document.getElementById('resultCount');
const filtersPanel = document.getElementById('filtersPanel');
const dynamicFilters = document.getElementById('dynamicFilters');

let allItems = [];

searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (!query) return;
    await performSearch(query);
});

async function performSearch(query) {
    showLoading();

    try {
        const resp = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await resp.json();
        allItems = data.items || [];
        renderResults(data);
        renderFilters(data.filter_options || {});
        renderParsedIntent(data.parsed || {});
    } catch (err) {
        showError(`Search failed: ${err.message}`);
    } finally {
        hideLoading();
    }
}

function renderResults(data) {
    resultsGrid.innerHTML = '';
    errorsDiv.classList.add('hidden');

    if (data.errors && data.errors.length > 0) {
        errorsDiv.textContent = `Warnings: ${data.errors.join(', ')}`;
        errorsDiv.classList.remove('hidden');
    }

    if (data.items.length === 0) {
        resultsGrid.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">&#x1F6D2;</div>
                <p>No results found. Try a different search.</p>
            </div>
        `;
        searchMeta.classList.add('hidden');
        filtersPanel.classList.add('hidden');
        return;
    }

    searchMeta.classList.remove('hidden');
    resultCount.textContent = `${data.total} result${data.total !== 1 ? 's' : ''}`;

    data.items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'item-card';
        card.dataset.marketplace = item.marketplace;

        const attrs = Object.entries(item.raw_attributes || {})
            .slice(0, 3)
            .map(([k, v]) => `<span class="attr-tag">${k}: ${v}</span>`)
            .join('');

        card.innerHTML = `
            <a href="${item.url}" target="_blank" rel="noopener">
                ${item.image_url
                    ? `<img class="item-image" src="${item.image_url}" alt="${escapeHtml(item.title)}" loading="lazy">`
                    : `<div class="item-image-placeholder">&#x1F4E6;</div>`
                }
                <div class="item-body">
                    <span class="item-marketplace">${item.marketplace.replace('_', ' ')}</span>
                    <h3 class="item-title">${escapeHtml(item.title)}</h3>
                    ${item.price ? `<div class="item-price">${escapeHtml(item.price)}</div>` : ''}
                    ${attrs ? `<div class="item-attrs">${attrs}</div>` : ''}
                </div>
            </a>
        `;
        resultsGrid.appendChild(card);
    });
}

function renderFilters(filterOptions) {
    dynamicFilters.innerHTML = '';
    const keys = Object.keys(filterOptions);

    if (keys.length === 0) {
        filtersPanel.classList.add('hidden');
        return;
    }

    filtersPanel.classList.remove('hidden');

    keys.forEach(category => {
        const values = filterOptions[category];
        if (values.length === 0) return;

        const group = document.createElement('div');
        group.className = 'filter-group';
        group.innerHTML = `<h4>${category.replace(/_/g, ' ')}</h4>`;

        values.slice(0, 10).forEach(val => {
            const label = document.createElement('label');
            const cb = document.createElement('input');
            cb.type = 'checkbox';
            cb.checked = true;
            cb.dataset.category = category;
            cb.dataset.value = val;
            cb.addEventListener('change', applyFilters);
            label.appendChild(cb);
            label.appendChild(document.createTextNode(` ${val}`));
            group.appendChild(label);
        });

        dynamicFilters.appendChild(group);
    });
}

function renderParsedIntent(parsed) {
    parsedIntent.innerHTML = '';
    if (!parsed) return;

    const badges = [];
    if (parsed.min_price != null) badges.push(`<span class="intent-badge"><strong>Min:</strong> £${parsed.min_price}</span>`);
    if (parsed.max_price != null) badges.push(`<span class="intent-badge"><strong>Max:</strong> £${parsed.max_price}</span>`);
    if (parsed.colour) badges.push(`<span class="intent-badge"><strong>Colour:</strong> ${parsed.colour}</span>`);
    if (parsed.condition) badges.push(`<span class="intent-badge"><strong>Condition:</strong> ${parsed.condition}</span>`);
    if (parsed.marketplaces && parsed.marketplaces.length > 0) {
        badges.push(`<span class="intent-badge"><strong>From:</strong> ${parsed.marketplaces.join(', ')}</span>`);
    }

    parsedIntent.innerHTML = badges.join('');
}

function applyFilters() {
    const cards = document.querySelectorAll('.item-card');
    cards.forEach(card => {
        card.style.display = '';
    });
}

function showLoading() {
    loading.classList.remove('hidden');
    resultsGrid.innerHTML = '';
    searchMeta.classList.add('hidden');
    filtersPanel.classList.add('hidden');
    errorsDiv.classList.add('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}

function showError(msg) {
    errorsDiv.textContent = msg;
    errorsDiv.classList.remove('hidden');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
