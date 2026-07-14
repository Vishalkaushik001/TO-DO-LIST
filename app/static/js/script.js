document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  const toggle = document.querySelector('.theme-toggle');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const savedTheme = localStorage.getItem('todo-theme');

  if (savedTheme) {
    body.setAttribute('data-theme', savedTheme);
  } else if (prefersDark) {
    body.setAttribute('data-theme', 'dark');
  }

  if (toggle) {
    const updateToggleLabel = () => {
      const isDark = body.getAttribute('data-theme') === 'dark';
      toggle.setAttribute('aria-pressed', isDark ? 'true' : 'false');
      toggle.textContent = isDark ? '☀️ Light' : '🌙 Dark';
    };

    updateToggleLabel();

    toggle.addEventListener('click', () => {
      const nextTheme = body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      body.setAttribute('data-theme', nextTheme);
      localStorage.setItem('todo-theme', nextTheme);
      updateToggleLabel();
    });
  }

  document.querySelectorAll('form').forEach((form) => {
    form.addEventListener('submit', () => {
      const submitButton = form.querySelector('button[type="submit"]');
      if (submitButton) {
        submitButton.textContent = 'Working...';
        submitButton.disabled = true;
      }
    });
  });
});
