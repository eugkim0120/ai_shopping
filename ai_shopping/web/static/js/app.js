/* AI Shopping — Frontend Logic */

const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultsGrid = document.getElementById('resultsGrid');
const loading = document.getElementById('loading');
const errorsDiv = document.getElementById('errors');
const searchMeta = document.getElementById('searchMeta');
const parsedIntent = document.getElementById('parsedIntent');
const resultCount = document.getElementById('resultCount');
const filtersPanel = document.getElementById('filtersPanel');
const dynamicFilters = document.getElementById('dynamicFilters');
const sortSelect = document.getElementById('sortSelect');
const demoBanner = document.getElementById('demoBanner');
const dataFreshness = document.getElementById('dataFreshness');

let allItems = [];
let totalFromServer = 0;
let currentSort = 'relevance';
let isDemo = false;

searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (!query) return;
    await performSearch(query);
});

if (sortSelect) {
    sortSelect.addEventListener('change', () => {
        currentSort = sortSelect.value;
        sortAndRender();
    });
}

async function performSearch(query) {
    showLoading();

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    try {
        const sort = currentSort || 'relevance';
        // Include selected marketplaces from chips
        const selectedMarketplaces = [];
        document.querySelectorAll('#marketplaceChips input[type="checkbox"]').forEach(cb => {
            if (!cb.checked) return; // only include checked ones
            selectedMarketplaces.push(cb.value);
        });
        const allChips = document.querySelectorAll('#marketplaceChips input[type="checkbox"]');
        // Only add marketplace param if not all are selected (i.e. user deselected some)
        let mpParam = '';
        if (selectedMarketplaces.length < allChips.length && selectedMarketplaces.length > 0) {
            mpParam = `&marketplaces=${selectedMarketplaces.join(',')}`;
        }
        const resp = await fetch(
            `/api/search?q=${encodeURIComponent(query)}&sort=${sort}${mpParam}`,
            { signal: controller.signal }
        );
        clearTimeout(timeoutId);
        const data = await resp.json();
        allItems = data.items || [];
        totalFromServer = data.total || 0;

        isDemo = (data.errors || []).some(e => e.includes('web-sourced') || e.includes('demo data'));
        if (demoBanner) {
            demoBanner.classList.toggle('hidden', !isDemo);
        }
        if (dataFreshness) {
            dataFreshness.classList.toggle('hidden', !isDemo || data.total === 0);
        }

        renderResults(data);
        renderFilters(data.filter_options || {});
        renderParsedIntent(data.parsed || {});
    } catch (err) {
        clearTimeout(timeoutId);
        if (err.name === 'AbortError') {
            showError('Search timed out after 30 seconds. Please try again.');
        } else {
            showError(`Search failed: ${err.message}`);
        }
    } finally {
        hideLoading();
    }
}

function sortAndRender() {
    if (allItems.length === 0) return;
    const sorted = [...allItems];
    if (currentSort === 'price_asc') {
        sorted.sort((a, b) => (parsePrice(a.price) || Infinity) - (parsePrice(b.price) || Infinity));
    } else if (currentSort === 'price_desc') {
        sorted.sort((a, b) => (parsePrice(b.price) || 0) - (parsePrice(a.price) || 0));
    } else if (currentSort === 'name_asc') {
        sorted.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
    }
    renderCards(sorted);
}

function parsePrice(priceStr) {
    if (!priceStr) return null;
    const cleaned = priceStr.replace(/[£$€,]/g, '').trim();
    const val = parseFloat(cleaned);
    return isNaN(val) ? null : val;
}

function renderResults(data) {
    resultsGrid.innerHTML = '';
    errorsDiv.classList.add('hidden');

    // Only show non-demo errors
    const realErrors = (data.errors || []).filter(e => !e.includes('demo data') && !e.includes('web-sourced'));
    if (realErrors.length > 0) {
        errorsDiv.innerHTML = realErrors.map(e =>
            `<div class="error-line">${escapeHtml(e)}</div>`
        ).join('');
        errorsDiv.classList.remove('hidden');
    }

    if (data.items.length === 0) {
        resultsGrid.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">&#x1F6D2;</div>
                <p>No results found. Try a different search term or broaden your filters.</p>
            </div>
        `;
        searchMeta.classList.add('hidden');
        filtersPanel.classList.add('hidden');
        return;
    }

    searchMeta.classList.remove('hidden');
    resultCount.textContent = `${data.total} result${data.total !== 1 ? 's' : ''}`;
    renderCards(data.items);
}

function renderCards(items) {
    resultsGrid.innerHTML = '';
    let visibleCount = 0;

    // Apply current sort
    let sorted = [...items];
    if (currentSort === 'price_asc') {
        sorted.sort((a, b) => (parsePrice(a.price) || Infinity) - (parsePrice(b.price) || Infinity));
    } else if (currentSort === 'price_desc') {
        sorted.sort((a, b) => (parsePrice(b.price) || 0) - (parsePrice(a.price) || 0));
    } else if (currentSort === 'name_asc') {
        sorted.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
    }

    sorted.forEach(item => {
        if (!passesFilters(item)) return;

        visibleCount++;
        const card = document.createElement('div');
        card.className = 'item-card';
        card.dataset.marketplace = item.marketplace || '';

        const attrs = Object.entries(item.raw_attributes || {})
            .filter(([k]) => !['brand', 'condition', 'colour', 'color'].includes(k.toLowerCase()))
            .slice(0, 4)
            .map(([k, v]) => `<span class="attr-tag">${escapeHtml(k)}: ${escapeHtml(v)}</span>`)
            .join('');

        const brand = item.raw_attributes?.brand;
        const condition = item.raw_attributes?.condition;
        const colour = item.raw_attributes?.colour || item.raw_attributes?.color;
        const isExternal = item.url && !item.url.includes('example.com');

        card.innerHTML = `
            <a href="${item.url}" target="_blank" rel="noopener">
                ${item.image_url
                    ? `<img class="item-image" src="${item.image_url}" alt="${escapeHtml(item.title)}" loading="lazy" onerror="this.outerHTML='<div class=\\'item-image-placeholder\\'>&#x1F4E6;</div>'">`
                    : `<div class="item-image-placeholder">&#x1F4E6;</div>`
                }
                <div class="item-body">
                    <div class="item-top-row">
                        <span class="item-marketplace item-marketplace--${(item.marketplace || '').replace('_', '-')}">${(item.marketplace || '').replace('_', ' ')}</span>
                        ${condition ? `<span class="item-condition item-condition--${condition.toLowerCase().replace(/\s+/g, '-')}">${escapeHtml(condition)}</span>` : ''}
                    </div>
                    ${brand ? `<div class="item-brand">${escapeHtml(brand)}</div>` : ''}
                    <h3 class="item-title">${escapeHtml(item.title)}</h3>
                    <div class="item-price-row">
                        ${item.price ? `<span class="item-price">${escapeHtml(item.price)}</span>` : ''}
                        ${colour ? `<span class="item-colour-dot" title="${escapeHtml(colour)}">${escapeHtml(colour)}</span>` : ''}
                    </div>
                    ${attrs ? `<div class="item-attrs">${attrs}</div>` : ''}
                </div>
            </a>
        `;
        resultsGrid.appendChild(card);
    });

    resultCount.textContent = `${visibleCount} of ${totalFromServer} result${totalFromServer !== 1 ? 's' : ''}`;
}

function passesFilters(item) {
    const checkboxes = dynamicFilters.querySelectorAll('input[type="checkbox"]');
    const filterState = {};
    checkboxes.forEach(cb => {
        const cat = cb.dataset.category;
        if (!filterState[cat]) filterState[cat] = { checked: [], unchecked: [] };
        if (cb.checked) {
            filterState[cat].checked.push(cb.dataset.value);
        } else {
            filterState[cat].unchecked.push(cb.dataset.value);
        }
    });

    for (const [category, state] of Object.entries(filterState)) {
        if (state.unchecked.length === 0) continue;

        const itemValues = getItemValuesForCategory(item, category);
        if (itemValues.length === 0) continue;

        const hasMatch = itemValues.some(v => state.checked.includes(v));
        if (!hasMatch) return false;
    }

    return true;
}

function getItemValuesForCategory(item, category) {
    const values = [];

    if (category === 'marketplace') {
        if (item.marketplace) {
            values.push(item.marketplace.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase()));
        }
        return values;
    }

    if (item.raw_attributes) {
        for (const [k, v] of Object.entries(item.raw_attributes)) {
            if (k.toLowerCase() === category.toLowerCase()) {
                values.push(v);
            }
        }
    }

    if (category === 'colour') {
        const colours = ['Black', 'White', 'Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple',
                         'Pink', 'Grey', 'Gray', 'Brown', 'Silver', 'Gold', 'Navy', 'Beige', 'Cream', 'Neon'];
        const titleWords = item.title.split(/\s+/);
        colours.forEach(c => {
            if (titleWords.some(w => w.toLowerCase() === c.toLowerCase())) {
                values.push(c);
            }
        });
    }

    return values;
}

function renderFilters(filterOptions) {
    dynamicFilters.innerHTML = '';
    const keys = Object.keys(filterOptions);

    if (keys.length === 0) {
        filtersPanel.classList.add('hidden');
        return;
    }

    filtersPanel.classList.remove('hidden');

    // Add clear filters button
    const clearBtn = document.createElement('button');
    clearBtn.className = 'clear-filters-btn';
    clearBtn.textContent = 'Clear All Filters';
    clearBtn.addEventListener('click', () => {
        dynamicFilters.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            cb.checked = true;
        });
        renderCards(allItems);
    });
    dynamicFilters.appendChild(clearBtn);

    keys.forEach(category => {
        const values = filterOptions[category];
        if (values.length === 0) return;

        const group = document.createElement('div');
        group.className = 'filter-group';
        group.innerHTML = `<h4>${category.replace(/_/g, ' ')}</h4>`;

        values.slice(0, 12).forEach(val => {
            const label = document.createElement('label');
            const cb = document.createElement('input');
            cb.type = 'checkbox';
            cb.checked = true;
            cb.dataset.category = category;
            cb.dataset.value = val;
            cb.addEventListener('change', () => renderCards(allItems));
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
    if (parsed.brand) badges.push(`<span class="intent-badge"><strong>Brand:</strong> ${parsed.brand}</span>`);
    if (parsed.min_price != null) badges.push(`<span class="intent-badge"><strong>Min:</strong> £${parsed.min_price}</span>`);
    if (parsed.max_price != null) badges.push(`<span class="intent-badge"><strong>Max:</strong> £${parsed.max_price}</span>`);
    if (parsed.colour) badges.push(`<span class="intent-badge"><strong>Colour:</strong> ${parsed.colour}</span>`);
    if (parsed.material) badges.push(`<span class="intent-badge"><strong>Material:</strong> ${parsed.material}</span>`);
    if (parsed.condition) badges.push(`<span class="intent-badge"><strong>Condition:</strong> ${parsed.condition}</span>`);
    if (parsed.size) badges.push(`<span class="intent-badge"><strong>Size:</strong> ${parsed.size}</span>`);
    if (parsed.marketplaces && parsed.marketplaces.length > 0) {
        badges.push(`<span class="intent-badge"><strong>From:</strong> ${parsed.marketplaces.join(', ')}</span>`);
    }

    parsedIntent.innerHTML = badges.join('');
}

function showLoading() {
    loading.classList.remove('hidden');
    resultsGrid.innerHTML = '';
    searchMeta.classList.add('hidden');
    filtersPanel.classList.add('hidden');
    errorsDiv.classList.add('hidden');
    if (demoBanner) demoBanner.classList.add('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}

function showError(msg) {
    errorsDiv.innerHTML = `<div class="error-line">${escapeHtml(msg)}</div>`;
    errorsDiv.classList.remove('hidden');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
