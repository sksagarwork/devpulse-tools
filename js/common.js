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

// URL State Sharing & Persistent Query Params
function shareCurrentCalculation() {
  const url = new URL(window.location.href);
  const inputs = document.querySelectorAll('.input-field, input[type="number"], select');
  inputs.forEach(input => {
    if (input.id && input.value !== '') {
      url.searchParams.set(input.id, input.value);
    }
  });
  navigator.clipboard.writeText(url.toString()).then(() => {
    showToast('🔗 Direct calculation link copied to clipboard!');
  }).catch(() => {
    prompt('Copy your calculation URL:', url.toString());
  });
}

function restoreUrlParams() {
  const params = new URLSearchParams(window.location.search);
  let hasRestored = false;
  params.forEach((val, key) => {
    const el = document.getElementById(key);
    if (el) {
      el.value = val;
      hasRestored = true;
    }
  });
  // Trigger calculation event if inputs were populated
  if (hasRestored) {
    const firstInput = document.querySelector('.input-field, input[type="number"]');
    if (firstInput) {
      firstInput.dispatchEvent(new Event('input', { bubbles: true }));
      firstInput.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }
}

// Embed Calculator Modal & Backlink Engine
function openEmbedModal(calcTitle, filename) {
  let modal = document.getElementById('embed-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'embed-modal';
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal-window">
        <div class="modal-header">
          <h3>Embed ${calcTitle}</h3>
          <button class="modal-close" onclick="closeEmbedModal()">&times;</button>
        </div>
        <p style="font-size:0.88rem; color:var(--text-secondary); margin-bottom:0.75rem;">
          Paste this responsive widget code into your blog, documentation, or website.
        </p>
        <textarea id="embed-code-text" class="embed-code-area" readonly></textarea>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:0.78rem; color:var(--text-muted);">Free &bull; Responsive &bull; Dark Mode Ready</span>
          <button class="btn-primary" onclick="copyEmbedCode()">Copy Embed Code</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeEmbedModal();
    });
  }
  const currentUrl = new URL(window.location.href);
  currentUrl.searchParams.set('embed', 'true');
  const embedCode = `<iframe src="${currentUrl.toString()}" width="100%" height="680" frameborder="0" style="border:1px solid #334155; border-radius:12px; max-width:820px; box-shadow:0 10px 25px rgba(0,0,0,0.2);" title="${calcTitle}"></iframe>\n<p style="font-size:12px; font-family:sans-serif; margin-top:6px; color:#64748b;">Powered by <a href="https://sksagarwork.github.io/devpulse-tools/" target="_blank" style="color:#3b82f6; text-decoration:none; font-weight:600;">CryptoCalc Pro</a></p>`;
  document.getElementById('embed-code-text').value = embedCode;
  modal.classList.add('active');
}

function closeEmbedModal() {
  const modal = document.getElementById('embed-modal');
  if (modal) modal.classList.remove('active');
}

function copyEmbedCode() {
  const text = document.getElementById('embed-code-text').value;
  navigator.clipboard.writeText(text).then(() => {
    showToast('✅ Embed code copied! Paste it into your site HTML.');
    closeEmbedModal();
  });
}

// Embed Mode Handler (?embed=true)
function checkEmbedMode() {
  const params = new URLSearchParams(window.location.search);
  if (params.get('embed') === 'true') {
    document.body.classList.add('is-embedded');
    const header = document.querySelector('header');
    if (header) header.style.display = 'none';
    const topAd = document.getElementById('top-banner-ad');
    if (topAd) topAd.style.display = 'none';
    const bottomAd = document.getElementById('content-banner-ad');
    if (bottomAd) bottomAd.style.display = 'none';
    const footer = document.querySelector('footer');
    if (footer) footer.style.display = 'none';
    const seoSection = document.querySelector('.seo-section');
    if (seoSection) seoSection.style.display = 'none';
    
    // Add small watermark attribution at the bottom
    let watermark = document.getElementById('embed-watermark');
    if (!watermark) {
      watermark = document.createElement('div');
      watermark.id = 'embed-watermark';
      watermark.style.cssText = 'text-align:center; padding:12px 0 6px; font-size:12px; color:var(--text-muted);';
      watermark.innerHTML = 'Powered by <a href="https://sksagarwork.github.io/devpulse-tools/" target="_blank" style="color:var(--accent); font-weight:600; text-decoration:none;">⚡ CryptoCalc Pro</a>';
      const main = document.querySelector('main');
      if (main) main.appendChild(watermark);
    }
  }
}

// Enhance initialization
window.addEventListener('DOMContentLoaded', () => {
  restoreUrlParams();
  checkEmbedMode();
});

// Crypto Tip Jar & Direct Community Support
function copyCryptoAddress(addr, chain) {
  navigator.clipboard.writeText(addr).then(() => {
    showToast(`✅ Copied ${chain} tip address to clipboard! Thank you for supporting free Web3 tools!`);
  }).catch(() => {
    prompt(`Copy ${chain} address:`, addr);
  });
}
