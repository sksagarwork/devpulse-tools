// Common utilities for DevPulse Tools Suite

// Theme Toggle
function initTheme() {
  const saved = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeIcon(saved);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'dark';
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateThemeIcon(next);
}

function updateThemeIcon(theme) {
  const icon = document.getElementById('theme-icon');
  if (icon) {
    icon.textContent = theme === 'dark' ? '🌙' : '☀️';
  }
}

// Copy to Clipboard
function copyText(text, btnElement) {
  navigator.clipboard.writeText(text).then(() => {
    showToast('Copied to clipboard!');
    if (btnElement) {
      const orig = btnElement.textContent;
      btnElement.textContent = 'Copied!';
      setTimeout(() => { btnElement.textContent = orig; }, 1800);
    }
  }).catch(() => {
    showToast('Failed to copy');
  });
}

// Toast Notification
function showToast(msg) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 2200);
}

// FAQ Accordion
function initFAQ() {
  document.querySelectorAll('.faq-question').forEach(q => {
    q.addEventListener('click', () => {
      const answer = q.nextElementSibling;
      const isOpen = answer.style.display === 'block';
      answer.style.display = isOpen ? 'none' : 'block';
      const arrow = q.querySelector('.faq-arrow');
      if (arrow) arrow.textContent = isOpen ? '▼' : '▲';
    });
  });
}

// Tool Search Filter (Homepage)
function initSearch() {
  const input = document.getElementById('tool-search');
  if (!input) return;
  input.addEventListener('input', (e) => {
    const val = e.target.value.toLowerCase().trim();
    document.querySelectorAll('.tool-card').forEach(card => {
      const title = card.querySelector('.tool-title').textContent.toLowerCase();
      const desc = card.querySelector('.tool-desc').textContent.toLowerCase();
      const tag = card.querySelector('.tool-tag').textContent.toLowerCase();
      const match = title.includes(val) || desc.includes(val) || tag.includes(val);
      card.style.display = match ? 'flex' : 'none';
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initFAQ();
  initSearch();
});
