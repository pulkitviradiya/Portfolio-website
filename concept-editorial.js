(() => {
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const motion = () => root.dataset.motion !== 'off' && !reduced.matches;
  const easing = 'cubic-bezier(.16, 1, .3, 1)';
  const liveAnimations = new Set();
  const play = (element, frames, options) => {
    if (!element || !motion()) return null;
    const animation = element.animate(frames, { fill: 'none', easing, ...options });
    liveAnimations.add(animation);
    animation.finished.catch(() => {}).finally(() => liveAnimations.delete(animation));
    return animation;
  };
  const wipe = document.querySelector('.page-wipe');
  let arrived = false;
  try { arrived = sessionStorage.getItem('pv-transition') === 'yes'; sessionStorage.removeItem('pv-transition'); } catch {}
  if (arrived && motion()) play(wipe, [{transform:'translateY(0)'},{transform:'translateY(-105%)'}], {duration:850});

  const intro = document.querySelector('.site-intro');
  let resolveIntro;
  const introDone = new Promise(resolve => { resolveIntro = resolve; });
  let introFinished = false;
  const finishIntro = () => {
    if (introFinished) return;
    introFinished = true;
    intro?.remove();
    resolveIntro();
  };
  if (arrived || !motion()) {
    finishIntro();
  } else {
    const started = performance.now();
    let advanced = false;
    const showSecond = () => {
      if (advanced) return;
      advanced = true;
      setTimeout(() => {
        if (introFinished) return;
        if (!motion()) return finishIntro();
        intro.dataset.step = 'second';
        intro.setAttribute('aria-label', 'सहज पके सो मीठा होय');
        intro.querySelector('.site-intro-first').setAttribute('aria-hidden', 'true');
        intro.querySelector('.site-intro-second').removeAttribute('aria-hidden');
        setTimeout(() => {
          if (!motion()) return finishIntro();
          intro.classList.add('is-leaving');
          setTimeout(finishIntro, 650);
        }, 1300);
      }, Math.max(0, 1000 - (performance.now() - started)));
    };
    if (document.readyState === 'complete') showSecond();
    else addEventListener('load', showSecond, {once:true});
    setTimeout(showSecond, 4500);
    reduced.addEventListener('change', () => { if (!motion()) finishIntro(); });
  }

  const entrance = () => {
    const delay = arrived ? 150 : 80;
    document.querySelectorAll('.hero-line>span').forEach((line, index) => {
      play(line, [{transform:'translateY(115%) rotate(4deg)',opacity:0},{transform:'translateY(0) rotate(0)',opacity:1}], {duration:1450,delay:delay+index*170,fill:'backwards'});
    });
    document.querySelectorAll('.hero-top,.hero-caption,.hero-bottom,.hero-rule').forEach((element, index) => {
      play(element, [{opacity:0,transform:'translateY(18px)'},{opacity:1,transform:'translateY(0)'}], {duration:950,delay:450+index*120,fill:'backwards'});
    });
    const heading = document.querySelector('.page-hero h1,.work-opening h1');
    play(heading, [{opacity:0,transform:'translateY(60px)',clipPath:'inset(100% 0 0 0)'},{opacity:1,transform:'translateY(0)',clipPath:'inset(0 0 0 0)'}], {duration:1300,delay,fill:'backwards'});
    document.querySelectorAll('.work-chapter').forEach((row, index) => {
      play(row, [{opacity:0,transform:'translateY(30px)'},{opacity:1,transform:'translateY(0)'}], {duration:900,delay:250+index*100,fill:'backwards'});
    });
  };
  Promise.all([introDone, Promise.race([document.fonts.ready, new Promise(resolve => setTimeout(resolve, 900))])]).then(entrance);

  const hero = document.querySelector('.hero');
  const portrait = document.querySelector('.hero-img');
  const coverImages = [...document.querySelectorAll('.case-cover img')];
  const inkHeadings = [...document.querySelectorAll('.intro h2,.dark-band .thesis')];
  inkHeadings.forEach(heading => {
    const walker = document.createTreeWalker(heading, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(node => {
      const fragment = document.createDocumentFragment();
      node.textContent.split(/(\s+)/).forEach(word => {
        if (/^\s*$/.test(word)) fragment.append(document.createTextNode(word));
        else { const span = document.createElement('span'); span.className = 'ink-word'; span.textContent = word; fragment.append(span); }
      });
      node.replaceWith(fragment);
    });
  });
  let pointerX = 0, pointerY = 0, currentX = 0, currentY = 0, frame = 0;
  const nav = document.querySelector('.nav');
  const update = () => {
    frame = 0;
    nav.classList.toggle('scrolled', scrollY > 35);
    if (!motion()) {
      if (portrait) portrait.style.transform = '';
      coverImages.forEach(image => image.style.transform = '');
      document.querySelectorAll('.ink-word').forEach(word => word.style.opacity = '');
      return;
    }
    currentX += (pointerX - currentX) * .08;
    currentY += (pointerY - currentY) * .08;
    if (portrait && hero.getBoundingClientRect().bottom > 0) {
      portrait.style.transform = `translate3d(${currentX}px,${currentY + Math.min(scrollY * .12, 95)}px,0) scale(1.045)`;
    }
    coverImages.forEach(image => {
      const box = image.parentElement.getBoundingClientRect();
      if (box.bottom > 0 && box.top < innerHeight) {
        const progress = Math.max(0, Math.min(1, (innerHeight - box.top) / (innerHeight + box.height)));
        image.style.transform = `translateY(${-progress * box.height * .14}px)`;
      }
    });
    inkHeadings.forEach(heading => {
      const box = heading.getBoundingClientRect();
      const amount = Math.max(0, Math.min(1, (innerHeight * .88 - box.top) / (innerHeight * .55)));
      const words = heading.querySelectorAll('.ink-word');
      words.forEach((word, index) => word.style.opacity = String(.65 + .35 * Math.max(0, Math.min(1, amount * (words.length + 5) - index))));
    });
    if (Math.abs(currentX - pointerX) + Math.abs(currentY - pointerY) > .03) frame = requestAnimationFrame(update);
  };
  const schedule = () => { if (!frame) frame = requestAnimationFrame(update); };
  addEventListener('scroll', schedule, {passive:true});
  addEventListener('resize', schedule, {passive:true});
  hero?.addEventListener('pointermove', event => {
    if (event.pointerType !== 'mouse') return;
    pointerX = (event.clientX / innerWidth - .5) * 16;
    pointerY = (event.clientY / innerHeight - .5) * 12;
    schedule();
  });
  hero?.addEventListener('pointerleave', () => { pointerX = pointerY = 0; schedule(); });
  new MutationObserver(() => {
    if (!motion()) liveAnimations.forEach(animation => animation.cancel());
    schedule();
  }).observe(root, {attributes:true,attributeFilter:['data-motion']});
  schedule();

  const backdrops = [...document.querySelectorAll('[data-backdrop]')];
  document.querySelectorAll('.work-chapter').forEach(row => {
    const activate = () => backdrops.forEach(backdrop => backdrop.classList.toggle('active', backdrop.dataset.backdrop === row.dataset.preview));
    row.addEventListener('pointerenter', activate);
    row.addEventListener('focus', activate);
  });
  const note = document.querySelector('.cursor-note');
  if (matchMedia('(hover:hover) and (pointer:fine)').matches) {
    document.querySelectorAll('.work-art').forEach(art => {
      art.addEventListener('pointerenter', () => { note.style.opacity = '1'; });
      art.addEventListener('pointermove', event => { note.style.transform = `translate(${event.clientX + 18}px,${event.clientY + 18}px)`; });
      art.addEventListener('pointerleave', () => { note.style.opacity = '0'; });
    });
  }
  document.querySelectorAll('.filter-bar').forEach(bar => bar.addEventListener('click', () => {
    requestAnimationFrame(() => {
      const target = document.getElementById(bar.dataset.filterGroup);
      target.querySelectorAll('[data-category]:not([hidden])').forEach((item,index) => play(item, [{opacity:0,transform:'translateY(24px)'},{opacity:1,transform:'translateY(0)'}], {duration:650,delay:Math.min(index*55,220),fill:'backwards'}));
    });
  }));
  let navigating = false;
  const sitePages = new Set(['index.html', 'work.html', 'journey.html', 'about.html', 'education.html', 'cairo.html', 'research.html', 'off-duty.html', 'candy-floss.html', 'pujan-energy.html', 'lenskart.html', 'ximivogue.html', 'ps-coffee.html']);
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href]');
    if (!anchor || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || anchor.target === '_blank' || anchor.hasAttribute('download') || !motion()) return;
    const destination = new URL(anchor.href, location.href);
    const pageName = destination.pathname.split('/').pop().replace(/^concept-/, '');
    if (!sitePages.has(pageName) || destination.origin !== location.origin || destination.pathname === location.pathname) return;
    event.preventDefault();
    if (navigating) return;
    navigating = true;
    try { sessionStorage.setItem('pv-transition','yes'); } catch {}
    wipe.style.transform = 'translateY(0)';
    play(wipe, [{transform:'translateY(105%)'},{transform:'translateY(0)'}], {duration:600});
    setTimeout(() => location.assign(destination.href), 610);
  });
  addEventListener('pageshow', event => {
    if (event.persisted) { navigating = false; wipe.style.transform = ''; schedule(); }
  });
  document.querySelectorAll('.flash-toggle').forEach(button => {
    button.addEventListener('click', () => {
      const card = button.closest('.venture-flash');
      const flipped = card.classList.toggle('is-flipped');
      button.setAttribute('aria-expanded', String(flipped));
      card.querySelector('.flash-front').inert = flipped;
      card.querySelector('.flash-front').setAttribute('aria-hidden', String(flipped));
      card.querySelector('.flash-back').inert = !flipped;
      card.querySelector('.flash-back').setAttribute('aria-hidden', String(!flipped));
    });
  });
})();
