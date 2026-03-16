document.addEventListener('DOMContentLoaded', () => {
    const root = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('theme');

    if (savedTheme) {
        root.setAttribute('data-theme', savedTheme);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = root.getAttribute('data-theme') || 'light';
            const nextTheme = currentTheme === 'light' ? 'dark' : 'light';
            root.setAttribute('data-theme', nextTheme);
            localStorage.setItem('theme', nextTheme);
        });
    }

    const questionCards = document.querySelectorAll('.js-question-card');

    questionCards.forEach((card) => {
        card.addEventListener('click', () => {
            const inputId = card.dataset.inputId;
            const input = document.getElementById(inputId);
            if (!input) return;

            const currentValue = input.value === '1' ? '1' : '0';
            const nextValue = currentValue === '1' ? '0' : '1';
            input.value = nextValue;

            const statusEl = card.querySelector('.question-card__status');
            if (nextValue === '1') {
                card.classList.add('question-card--correct');
                if (statusEl) statusEl.textContent = '✓ Acertou';
            } else {
                card.classList.remove('question-card--correct');
                if (statusEl) statusEl.textContent = '✗ Errou';
            }
        });
    });
});