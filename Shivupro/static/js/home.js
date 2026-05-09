// Basic smooth UI for landing page
(function () {
  const onReady = (fn) => {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  };

  onReady(() => {
    // Smooth scroll for in-page anchors (if any)
    document.querySelectorAll('a[href^="#"]').forEach((a) => {
      a.addEventListener('click', (e) => {
        const id = a.getAttribute('href');
        const el = id && id.length > 1 ? document.querySelector(id) : null;
        if (!el) return;
        e.preventDefault();
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });

    // Simple hero entrance animation
    const hero = document.querySelector('.tit');
    if (hero) {
      hero.style.opacity = '0';
      hero.style.transform = 'translateY(10px)';
      hero.style.transition = 'opacity 600ms ease, transform 600ms ease';
      requestAnimationFrame(() => {
        hero.style.opacity = '1';
        hero.style.transform = 'translateY(0)';
      });
    }

    // Navigation active highlight
    const current = window.location.pathname;
    document.querySelectorAll('ul li a').forEach((a) => {
      const href = a.getAttribute('href') || '';
      if (href === current || (current === '/' && href === '/')) {
        a.classList.add('active');
      }
      a.addEventListener('mouseenter', () => a.classList.add('hovered'));
      a.addEventListener('mouseleave', () => a.classList.remove('hovered'));
    });
  });
})();

