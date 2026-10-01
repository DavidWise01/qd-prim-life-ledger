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
      status.textContent = 'JS ONLINE';
      status.classList.add('online');
    }

    // Reveal is enhancement only; content stays visible if this file never loads.
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

    // Eight-layer navigator: links work natively; JS only marks current layer.
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

    // Emergence controller.
    const emergence = document.querySelector('[data-emergence]');
    let emergenceTimer = null;
    let emergenceStage = 0;

    const showEmergence = (index) => {
      if (!emergence) return;
      const nodes = [...emergence.querySelectorAll('.em-node')];
      const readout = emergence.querySelector('[data-readout]');
      const trace = [
        'root0 → {{2^3}} = 8 q.d states',
        '8 → serial gravity 10^3 = 1000:1',
        '1000:1 → 360 + 3L + 3R = 366 addresses',
        '366 → (360 - 10) / 17.5 = 20 rings',
        '20 rings → 4 phases × 90 = 360 per ring',
        '40 source lives × 2 incarnations × 90 = 7200',
        '60 ticks × 40 generations × 3 = 7200',
        '30 bubbles → 20 retained dots → 20^3 / 20 = 400'
      ];
      nodes.forEach((node, i) => node.classList.toggle('active', i < index));
      if (readout) readout.textContent = index === 0 ? 'root0 waiting' : trace[index - 1];
      emergence.classList.toggle('complete', index === nodes.length);
    };

    const startEmergence = () => {
      if (!emergence || emergenceTimer) return;
      const nodes = [...emergence.querySelectorAll('.em-node')];
      if (emergenceStage >= nodes.length) emergenceStage = 0;
      showEmergence(emergenceStage);
      const interval = reduced ? 40 : 360;
      const advance = () => {
        if (emergenceStage >= nodes.length) {
          clearInterval(emergenceTimer);
          emergenceTimer = null;
          return;
        }
        emergenceStage += 1;
        showEmergence(emergenceStage);
      };
      advance();
      emergenceTimer = setInterval(advance, interval);
    };

    const resetEmergence = () => {
      if (emergenceTimer) clearInterval(emergenceTimer);
      emergenceTimer = null;
      emergenceStage = 0;
      showEmergence(0);
    };

    // Memristic controller.
    const memory = document.querySelector('[data-memory]');
    const memoryRotations = ['−m', '+m', '−f', '+f'];
    const memoryContexts = ['advanced tech', 'dirt poor'];
    const memoryCharges = [-1, 0, -1, 0];
    let memoryIndex = 0;

    const renderMemory = () => {
      if (!memory) return;
      const phaseEl = memory.querySelector('[data-memory-phase]');
      const contextEl = memory.querySelector('[data-memory-context]');
      const yearEl = memory.querySelector('[data-memory-year]');
      const lifeEl = memory.querySelector('[data-memory-life]');
      const rotationIndex = memoryIndex % 4;
      const contextIndex = Math.floor(memoryIndex / 4) % 2;
      const years = memoryIndex * 3;
      if (phaseEl) phaseEl.textContent = memoryRotations[rotationIndex];
      if (contextEl) contextEl.textContent = memoryContexts[contextIndex];
      if (yearEl) yearEl.textContent = 'year +' + years + ' · memory ' + memoryCharges[rotationIndex];
      if (lifeEl) lifeEl.textContent = 'life ' + Math.min(9, Math.floor(years / 1000)) + ' / 9';
      memory.dataset.state = String(memoryIndex);
    };

    // Single delegated click handler: fewer fragile element-specific bindings.
    document.addEventListener('click', (event) => {
      const action = event.target.closest('[data-action]');
      if (!action) return;
      const name = action.dataset.action;

      if (name === 'grow-emergence') {
        event.preventDefault();
        startEmergence();
        return;
      }
      if (name === 'reset-emergence') {
        event.preventDefault();
        resetEmergence();
        return;
      }
      if (name === 'memory-next') {
        event.preventDefault();
        memoryIndex = (memoryIndex + 1) % 8;
        renderMemory();
        return;
      }
      if (name === 'memory-prev') {
        event.preventDefault();
        memoryIndex = (memoryIndex + 7) % 8;
        renderMemory();
        return;
      }
      if (name === 'memory-reset') {
        event.preventDefault();
        memoryIndex = 0;
        renderMemory();
      }
    });

    showEmergence(0);
    renderMemory();

    // Visible self-check so button wiring failures are obvious.
    const checks = {
      layers: layerLinks.length === 8,
      emergence: Boolean(emergence && emergence.querySelector('[data-action="grow-emergence"]')),
      memory: Boolean(memory && memory.querySelector('[data-action="memory-next"]'))
    };
    const selfCheck = document.querySelector('[data-self-check]');
    if (selfCheck) {
      const ok = Object.values(checks).every(Boolean);
      selfCheck.textContent = ok ? '8/8 UI TETHER PASS' : 'UI TETHER ERROR';
      selfCheck.classList.toggle('online', ok);
      selfCheck.dataset.checks = JSON.stringify(checks);
    }
  });
})();
