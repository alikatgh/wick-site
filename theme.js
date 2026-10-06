/* One appearance preference for the homepage, reference, blog, and book. */
(() => {
  const key = 'wick-theme';
  const valid = value => ['light', 'dark', 'system'].includes(value) ? value : 'system';
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = 'system';
  try { preference = valid(localStorage.getItem(key)); } catch (_) { /* Storage is optional. */ }
  function apply() {
    const theme = preference === 'system' ? (media.matches ? 'dark' : 'light') : preference;
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
    if (document.body) document.body.dataset.mdColorScheme = theme === 'dark' ? 'slate' : 'default';
    document.querySelectorAll('[data-wick-theme]').forEach(control => { control.value = preference; });
  }
  apply();
  document.addEventListener('DOMContentLoaded', apply, { once: true });
  document.addEventListener('change', event => {
    if (!event.target.matches('[data-wick-theme]')) return;
    preference = valid(event.target.value);
    try { localStorage.setItem(key, preference); } catch (_) { /* Keep the choice for this page. */ }
    apply();
  });
  media.addEventListener('change', () => { if (preference === 'system') apply(); });
  window.addEventListener('storage', event => {
    if (event.key === key || event.key === null) { preference = valid(event.newValue); apply(); }
  });
})();
