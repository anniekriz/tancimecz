// Handle loading more past events without replacing existing items
// This script intercepts clicks on the "Načíst další" button, fetches
// the next page of results and appends them to the current list.

document.addEventListener('DOMContentLoaded', () => {
    const loadMoreContainer = document.querySelector('.load-more');
    if (!loadMoreContainer) return;

    loadMoreContainer.addEventListener('click', async (event) => {
        const button = event.target.closest('.load-more-button');
        if (!button) return;
        event.preventDefault();

        try {
            const response = await fetch(button.href, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const text = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'text/html');

            const newGrid = doc.querySelector('.events-grid');
            const currentGrid = document.querySelector('.events-grid');
            if (newGrid && currentGrid) {
                Array.from(newGrid.children).forEach((child) => {
                    currentGrid.appendChild(child);
                });
            }

            const newLoadMore = doc.querySelector('.load-more');
            if (newLoadMore) {
                loadMoreContainer.innerHTML = newLoadMore.innerHTML;
            } else {
                loadMoreContainer.remove();
            }
        } catch (err) {
            console.error('Failed to load more events:', err);
        }
    });
});