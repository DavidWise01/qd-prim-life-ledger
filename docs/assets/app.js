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

  const emergence = document.querySelector('[data-emergence]');
  if (emergence) {
    const seed = emergence.querySelector('[data-seed]');
    const reset = emergence.querySelector('[data-reset]');
    const readout = emergence.querySelector('[data-readout]');
    const nodes = [...emergence.querySelectorAll('.em-node')];
    const trace = [
      'root0 → q.d volume 2³ = 8',
      '8 → serial gravity 10³ = 1000:1',
      '1000:1 → 360 + 3L + 3R = 366 addresses',
      '366 geometry → (360 − 10) / 17.5 = 20 rings',
      '20 rings → solid/liquid/gas/plasma × 90 = 360 per ring',
      '40 source lives × 2 incarnations × 90 = 7200',
      '60 ticks × 40 generations × 3 = 7200',
      '30 bubbles → 20 retained dots → 20³ / 20 = 400'
    ];
    let stage = 0;
    let timer = null;

    const showStage = (index) => {
      nodes.forEach((node, i) => node.classList.toggle('active', i < index));
      readout.textContent = index === 0 ? 'root0 waiting' : trace[index - 1];
      emergence.classList.toggle('complete', index === nodes.length);
    };

    const step = () => {
      if (stage >= nodes.length) {
        clearInterval(timer);
        timer = null;
        seed.classList.remove('growing');
        return;
      }
      stage += 1;
      showStage(stage);
      seed.classList.remove('growing');
      void seed.offsetWidth;
      seed.classList.add('growing');
    };

    seed.addEventListener('click', () => {
      if (timer) return;
      if (stage >= nodes.length) stage = 0;
      showStage(stage);
      step();
      timer = setInterval(step, reduced ? 70 : 430);
    });

    reset.addEventListener('click', () => {
      if (timer) clearInterval(timer);
      timer = null;
      stage = 0;
      seed.classList.remove('growing');
      showStage(0);
    });

    showStage(0);
  }


  const memory = document.querySelector('[data-memory]');
  if (memory) {
    const stepButton = memory.querySelector('[data-memory-step]');
    const phaseEl = memory.querySelector('[data-memory-phase]');
    const contextEl = memory.querySelector('[data-memory-context]');
    const yearEl = memory.querySelector('[data-memory-year]');
    const rotations = ['−m', '+m', '−f', '+f'];
    const deltas = [-1, 1, -1, 1];
    const contexts = ['advanced tech', 'dirt poor'];
    let index = 0;
    let charge = -1;

    const renderMemory = () => {
      const rotation = rotations[index % 4];
      const context = contexts[Math.floor(index / 4) % 2];
      if (index === 0) charge = -1;
      phaseEl.textContent = rotation;
      contextEl.textContent = context;
      yearEl.textContent = 'year +' + (index * 3) + ' · memory ' + (charge > 0 ? '+' : '') + charge;
    };

    stepButton.addEventListener('click', () => {
      index += 1;
      if (index % 8 === 0) {
        index = 0;
        charge = -1;
      } else {
        charge += deltas[index % 4];
      }
      renderMemory();
    });

    renderMemory();
  }

})();
