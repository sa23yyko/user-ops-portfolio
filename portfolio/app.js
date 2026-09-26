/* Progressive enhancement only; the entire case remains readable without JS. */
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const motionTargets = document.querySelectorAll('.doodle, .l-line, .chapter-number, .chapter-title, .overview-intro');
let motionObserver;
function configureMotion() {
  motionObserver?.disconnect();
  motionTargets.forEach(node => node.classList.remove('draw-now', 'number-now', 'reveal-now', 'float-now'));
  if (reducedMotion.matches || !('IntersectionObserver' in window)) return;
  motionObserver = new IntersectionObserver(entries => {
    entries.forEach(({target, isIntersecting}) => {
      if (!isIntersecting) return;
      target.classList.add(target.matches('svg') ? 'draw-now' : target.matches('.chapter-number') ? 'number-now' : 'reveal-now');
      if (target.matches('.hero-user .doodle')) target.classList.add('float-now');
      motionObserver.unobserve(target);
    });
  }, {threshold: .15});
  motionTargets.forEach(node => motionObserver.observe(node));
}
configureMotion();
reducedMotion.addEventListener('change', configureMotion);
const menu = document.querySelector('.menu');
menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => { menu.open = false; }));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu.open) { menu.open = false; menu.querySelector('summary').focus(); }
});

// 07 only: final values remain accessible; reduced motion cancels in-flight counts.
const cohortRows = document.querySelectorAll('#funnel .cohort-row');
const countFrames = new Map();
const counted = new WeakSet();
let cohortObserver;
function resetCohortMotion() {
  cohortObserver?.disconnect();
  countFrames.forEach(frame => cancelAnimationFrame(frame));
  countFrames.clear();
  cohortRows.forEach(row => {
    row.classList.remove('cohort-visible');
    const number = row.querySelector('[data-count]');
    number.textContent = number.dataset.count;
  });
  if (reducedMotion.matches || !('IntersectionObserver' in window)) return;
  cohortObserver = new IntersectionObserver(entries => {
    entries.forEach(({target: row, isIntersecting}) => {
      if (!isIntersecting || reducedMotion.matches) return;
      row.classList.add('cohort-visible');
      cohortObserver.unobserve(row);
      const number = row.querySelector('[data-count]');
      if (counted.has(number)) return;
      counted.add(number);
      const finalValue = Number(number.dataset.count);
      const start = performance.now();
      function tick(now) {
        if (reducedMotion.matches) { number.textContent = finalValue; countFrames.delete(number); return; }
        const progress = Math.min((now - start) / 850, 1);
        number.textContent = Math.round(finalValue * (1 - (1 - progress) ** 3));
        if (progress < 1) countFrames.set(number, requestAnimationFrame(tick));
        else { number.textContent = finalValue; countFrames.delete(number); }
      }
      countFrames.set(number, requestAnimationFrame(tick));
    });
  }, {threshold: .4});
  cohortRows.forEach(row => cohortObserver.observe(row));
}
resetCohortMotion();
reducedMotion.addEventListener('change', resetCohortMotion);
