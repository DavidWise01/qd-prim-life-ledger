(() => {
  'use strict';

  const ready = (fn) => {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn, { once: true });
    } else {
      fn();
    }
  };

  ready(() => {
    const reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const finePointer = window.matchMedia && window.matchMedia('(pointer:fine)').matches;

    document.documentElement.classList.add('js-ready');

    const status = document.querySelector('[data-js-status]');
    if (status) {
      status.textContent = 'JS OPTIONAL / ONLINE';
      status.classList.add('online');
    }

    const reveals = [...document.querySelectorAll('.reveal')];
    reveals.forEach((el) => el.classList.add('js-reveal'));
    if ('IntersectionObserver' in window && !reduced) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('in');
          observer.unobserve(entry.target);
        });
      }, { threshold: 0.08, rootMargin: '0px 0px -5% 0px' });
      reveals.forEach((el) => observer.observe(el));
    } else {
      reveals.forEach((el) => el.classList.add('in'));
    }

    if (!reduced && finePointer) {
      document.querySelectorAll('[data-tilt]').forEach((card) => {
        card.addEventListener('pointermove', (event) => {
          const rect = card.getBoundingClientRect();
          const x = (event.clientX - rect.left) / rect.width - 0.5;
          const y = (event.clientY - rect.top) / rect.height - 0.5;
          card.style.transform =
            'perspective(1100px) rotateX(' + (-y * 5) + 'deg) rotateY(' + (x * 7) + 'deg) translateY(-2px)';
        });
        card.addEventListener('pointerleave', () => { card.style.transform = ''; });
      });
    }

    const layerLinks = [...document.querySelectorAll('[data-layer-link]')];
    const layerTargets = layerLinks
      .map((link) => document.querySelector(link.getAttribute('href')))
      .filter(Boolean);

    const markLayer = (id) => {
      layerLinks.forEach((link) => {
        const active = link.getAttribute('href') === '#' + id;
        link.classList.toggle('active', active);
        if (active) link.setAttribute('aria-current', 'step');
        else link.removeAttribute('aria-current');
      });
    };

    if ('IntersectionObserver' in window) {
      const layerObserver = new IntersectionObserver((entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible) markLayer(visible.target.id);
      }, { threshold: [0.15, 0.35, 0.6] });
      layerTargets.forEach((target) => layerObserver.observe(target));
    }

    const emergenceRadios = [...document.querySelectorAll('input[name="emergence-state"]')];
    const memoryRadios = [...document.querySelectorAll('input[name="memory-state"]')];
    const labels = [...document.querySelectorAll('label[for]')];
    const brokenLabels = labels.filter((label) => !document.getElementById(label.htmlFor));

    const checks = {
      layers: layerLinks.length === 8 && layerTargets.length === 8,
      emergence_states: emergenceRadios.length === 9,
      memory_states: memoryRadios.length === 8,
      label_targets: brokenLabels.length === 0
    };

    const selfCheck = document.querySelector('[data-self-check]');
    if (selfCheck) {
      const ok = Object.values(checks).every(Boolean);
      selfCheck.textContent = ok ? 'NATIVE 8/8 CONTROL PASS' : 'UI TETHER ERROR';
      selfCheck.classList.toggle('online', ok);
      selfCheck.dataset.checks = JSON.stringify(checks);
    }
  });
})();
