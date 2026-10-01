(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduced) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach((el) => observer.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('in'));
  }

  if (!reduced && window.matchMedia('(pointer:fine)').matches) {
    document.querySelectorAll('[data-tilt]').forEach((card) => {
      const maxX = 5;
      const maxY = 7;
      card.addEventListener('pointermove', (event) => {
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - 0.5;
        const y = (event.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = 'perspective(1100px) rotateX(' + (-y * maxX) + 'deg) rotateY(' + (x * maxY) + 'deg) translateY(-2px)';
      });
      card.addEventListener('pointerleave', () => {
        card.style.transform = '';
      });
    });
  }

  const navLinks = [...document.querySelectorAll('.nav-links a[href^="#"]')];
  const sections = navLinks
    .map((a) => document.querySelector(a.getAttribute('href')))
    .filter(Boolean);

  if ('IntersectionObserver' in window) {
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        navLinks.forEach((a) => a.removeAttribute('aria-current'));
        const active = navLinks.find((a) => a.getAttribute('href') === '#' + entry.target.id);
        if (active) active.setAttribute('aria-current', 'true');
      });
    }, { threshold: 0.45 });
    sections.forEach((section) => spy.observe(section));
  }
})();
