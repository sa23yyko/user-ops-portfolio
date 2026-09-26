// Navigation is native anchor scrolling; JavaScript only marks the visible chapter.
const chapterLinks = [...document.querySelectorAll('.directory-list a[href^="#"]')];
const chapters = chapterLinks.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);

function markCurrent(id) {
  chapterLinks.forEach(link => {
    if (link.getAttribute('href') === `#${id}`) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (visible) markCurrent(visible.target.id);
  }, { rootMargin: '-18% 0px -52% 0px', threshold: [0, .25, .5] });
  chapters.forEach(chapter => observer.observe(chapter));
}

chapterLinks.forEach(link => link.addEventListener('click', () => {
  markCurrent(link.hash.slice(1));
}));
