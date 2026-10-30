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

// PWA Service Worker Registration & Install Prompt
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').then((reg) => {
      console.log('CryptoCalc Pro ServiceWorker active:', reg.scope);
    }).catch((err) => {
      console.warn('ServiceWorker registration notice:', err);
    });
  });
}

let deferredInstallPrompt = null;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredInstallPrompt = e;
  const installBtn = document.getElementById('pwa-install-btn');
  if (installBtn) {
    installBtn.style.display = 'inline-flex';
  }
});

function triggerPwaInstall() {
  if (deferredInstallPrompt) {
    deferredInstallPrompt.prompt();
    deferredInstallPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        showToast('🎉 CryptoCalc Pro installed to your device!');
      }
      deferredInstallPrompt = null;
      const installBtn = document.getElementById('pwa-install-btn');
      if (installBtn) installBtn.style.display = 'none';
    });
  } else {
    showToast('To install: click your browser menu & select "Install App" or "Add to Home Screen"');
  }
}

// Global Command Palette (Cmd+K / Ctrl+K)
const SEARCH_INDEX = [
  { title: "Ethereum Gas Fee Calculator", desc: "Live Gwei to USD, Uniswap swaps & L2 fees", url: "eth-gas-calculator.html", icon: "⛽" },
  { title: "Crypto SIP & Compounding", desc: "Monthly Bitcoin DCA returns over 1-10 years", url: "crypto-sip-calculator.html", icon: "📈" },
  { title: "Uniswap Impermanent Loss", desc: "LP pool fee APR vs simple HODLing", url: "impermanent-loss-calculator.html", icon: "⚖️" },
  { title: "Crypto Capital Gains Tax", desc: "IRS, HMRC & ATO short/long-term tax estimator", url: "crypto-tax-calculator.html", icon: "📊" },
  { title: "Staking APY & Yield Calculator", desc: "Daily/weekly compound validator staking returns", url: "staking-yield-calculator.html", icon: "💎" },
  { title: "DCA Bitcoin Calculator", desc: "Dollar cost averaging backtest & average cost", url: "dca-crypto-calculator.html", icon: "🔄" },
  { title: "Futures Liquidation Price", desc: "Long and Short liquidation prices 2x-100x", url: "liquidation-price-calculator.html", icon: "⚡" },
  { title: "Crypto Trading Profit & ROI", desc: "Maker/taker exchange fees and break-even price", url: "crypto-profit-calculator.html", icon: "💰" },
  { title: "Best Crypto Tax Software Review", desc: "Koinly vs CoinLedger vs CoinTracker 2024", url: "content/best-crypto-tax-software-koinly-review.html", icon: "📑" },
  { title: "Best Hardware Wallets Review", desc: "Ledger Nano X vs Trezor vs Tangem cold storage", url: "content/best-crypto-hardware-wallets-ledger-vs-trezor.html", icon: "🔒" },
  { title: "Layer 2 Gas Fees Breakdown", desc: "Arbitrum vs Base vs Optimism fee savings", url: "content/layer-2-gas-fees-arbitrum-optimism-base.html", icon: "🚀" },
  { title: "Free Embed Widget Builder", desc: "Embed responsive calculators on your website", url: "embed-builder.html", icon: "🧩" }
];

function initCommandPalette() {
  let palette = document.getElementById('command-palette');
  if (!palette) {
    palette = document.createElement('div');
    palette.id = 'command-palette';
    palette.className = 'modal-overlay';
    palette.innerHTML = `
      <div class="modal-window" style="max-width:540px; padding:1.25rem;">
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
          <span style="font-size:1.2rem;">🔍</span>
          <input type="text" id="palette-search-input" placeholder="Search calculators, guides, tools... (Esc to close)" style="width:100%; background:none; border:none; color:var(--text-primary); font-size:1.05rem; outline:none;" />
          <span style="font-size:0.75rem; color:var(--text-muted); background:var(--bg-tertiary); padding:0.2rem 0.5rem; border-radius:4px;">ESC</span>
        </div>
        <div id="palette-results" style="max-height:360px; overflow-y:auto; display:flex; flex-direction:column; gap:0.4rem;">
        </div>
      </div>
    `;
    document.body.appendChild(palette);
    palette.addEventListener('click', (e) => {
      if (e.target === palette) closeCommandPalette();
    });

    const input = document.getElementById('palette-search-input');
    input.addEventListener('input', renderPaletteResults);
  }

  // Keyboard Shortcuts: Ctrl+K / Cmd+K / Esc
  window.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      toggleCommandPalette();
    } else if (e.key === 'Escape') {
      closeCommandPalette();
    }
  });
}

function toggleCommandPalette() {
  const palette = document.getElementById('command-palette');
  if (palette && palette.classList.contains('active')) {
    closeCommandPalette();
  } else {
    openCommandPalette();
  }
}

function openCommandPalette() {
  initCommandPalette();
  const palette = document.getElementById('command-palette');
  palette.classList.add('active');
  const input = document.getElementById('palette-search-input');
  input.value = '';
  input.focus();
  renderPaletteResults();
}

function closeCommandPalette() {
  const palette = document.getElementById('command-palette');
  if (palette) palette.classList.remove('active');
}

function renderPaletteResults() {
  const query = (document.getElementById('palette-search-input').value || '').toLowerCase().trim();
  const resultsEl = document.getElementById('palette-results');
  resultsEl.innerHTML = '';

  const filtered = SEARCH_INDEX.filter(item => {
    return item.title.toLowerCase().includes(query) || item.desc.toLowerCase().includes(query);
  });

  if (filtered.length === 0) {
    resultsEl.innerHTML = '<div style="padding:1.5rem; text-align:center; color:var(--text-muted);">No matching tools found.</div>';
    return;
  }

  filtered.forEach(item => {
    const a = document.createElement('a');
    // Normalize relative path if we are inside /content/
    const isSubdir = window.location.pathname.includes('/content/');
    const targetUrl = isSubdir ? (item.url.startsWith('content/') ? item.url.replace('content/', '') : '../' + item.url) : item.url;
    
    a.href = targetUrl;
    a.style.cssText = 'display:flex; align-items:center; gap:0.75rem; padding:0.65rem 0.85rem; border-radius:8px; text-decoration:none; color:var(--text-primary); transition:background 0.15s;';
    a.addEventListener('mouseenter', () => a.style.background = 'var(--bg-tertiary)');
    a.addEventListener('mouseleave', () => a.style.background = 'none)');
    a.innerHTML = `
      <span style="font-size:1.4rem;">${item.icon}</span>
      <div style="flex:1;">
        <strong style="display:block; font-size:0.95rem;">${item.title}</strong>
        <span style="font-size:0.8rem; color:var(--text-muted);">${item.desc}</span>
      </div>
      <span style="color:var(--text-muted); font-size:0.85rem;">&rarr;</span>
    `;
    resultsEl.appendChild(a);
  });
}

// Auto init on page load
window.addEventListener('DOMContentLoaded', () => {
  initCommandPalette();
});
