const coverImage = document.querySelector('.cover-original');
const titleMasks = [...document.querySelectorAll('.title-wipe')];
const mobileLayout = window.matchMedia('(max-width: 700px)');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

function updateHotspots() {
  document.querySelector('.cover-hotspots').inert = mobileLayout.matches;
  document.querySelector('.mobile-zoom').inert = !mobileLayout.matches;
}
updateHotspots();
mobileLayout.addEventListener('change', updateHotspots);

function startCover() {
  if (reducedMotion.matches) {
    titleMasks.forEach(mask => mask.remove());
    return;
  }
  document.documentElement.classList.add('cover-ready');
  titleMasks.forEach(mask => mask.addEventListener('animationend', () => mask.remove(), {once:true}));
}
if (coverImage.complete && coverImage.naturalWidth) startCover();
else coverImage.addEventListener('load', startCover, {once:true});

// PRD V1.0 rule preview. This demonstrates proposed logic; no production events are sent.
const ruleExamples = {
  R01: ['目标驱动型', '注册后未首学 · start_learning = 0', '展示 10 分钟首学任务', '距离目标还有一段路，今天先完成第一步。', '开始今天的第一步', '激活率 / 首日任务完成率'],
  R02: ['碎片学习型', '注册后未首学 · 每天可用时间 ≤ 10 分钟', '展示 10 分钟微任务', '今天只有10分钟？够了。完成这一组，今天就算学过了。', '开始10分钟', '首日任务完成率'],
  R03: ['兴趣成长型', '低频但仍有内容兴趣', '展示兴趣内容入口', '今天不背词表。用一段影视对白学3个真实表达。', '看看今天学什么', '内容点击 / 再次学习'],
  R04: ['习惯激励型', '刚刚断签 · streak_broken = 1', '展示断签恢复', '昨天没学，也不用重新开始。今天完成一个小任务，可以恢复连续记录。', '继续我的记录', '3日回访 / 恢复率'],
  R05: ['目标驱动型', 'D1 未学习', '展示目标进度提醒', '今天先完成最小任务，别让计划从第一天就变重。', '完成今日最小任务', 'D1 学习率'],
  R06: ['碎片学习型', '沉默 2 天及以上', '展示低成本召回', '现在有10分钟，也可以完成一组。', '回来学10分钟', '再次学习率'],
  R07: ['兴趣成长型', '沉默 2 天及以上', '展示新主题召回', '今天换个方式：不做题，学3个你会真的用到的表达。', '看看新主题', '召回点击 / 再次学习'],
  R08: ['习惯激励型', '完成连续学习任务', '展示连续反馈', '今天完成啦。连续记录 +1，明天继续一点就好。', '明天提醒我', '次日回访']
};
const ruleButtons = [...document.querySelectorAll('[data-rule]')];
function showRule(id) {
  const data = ruleExamples[id];
  if (!data) return;
  const fields = ['rule-id', 'rule-when', 'rule-action', 'rule-copy', 'rule-cta', 'rule-metric'];
  const values = [`${id} / ${data[0]}`, data[1], data[2], data[3], `${data[4]} ↗`, data[5]];
  fields.forEach((field, index) => { document.getElementById(field).textContent = values[index]; });
  ruleButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.rule === id)));
}
ruleButtons.forEach(button => button.addEventListener('click', () => showRule(button.dataset.rule)));
showRule('R02');

const readingLinks = [...document.querySelectorAll('.reading-links a')];
const chapters = [...document.querySelectorAll('.chapter')];
if ('IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, {rootMargin: '0px 0px -45px 0px', threshold: 0.05});
  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
  const navObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      readingLinks.forEach(link => {
        if (link.getAttribute('href') === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    });
  }, {rootMargin: '-25% 0px -60% 0px'});
  chapters.forEach(chapter => navObserver.observe(chapter));
} else {
  document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
}
document.documentElement.classList.add('can-reveal');
