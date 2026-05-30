/* ====================================================================
   Portfolio interactions & rendering
   ==================================================================== */
(function () {
  "use strict";

  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  /* ---------- Render: Experience timeline ---------- */
  function renderExperience() {
    const root = $("#timeline");
    if (!root) return;
    root.innerHTML = PORTFOLIO_DATA.experience
      .map(
        (job) => `
      <article class="tl-item reveal">
        <div class="tl-item__dot" aria-hidden="true"></div>
        <div class="tl-item__card">
          <div class="tl-item__head">
            <h3>${job.role}</h3>
            <span class="tl-item__period">${job.period}</span>
          </div>
          <p class="tl-item__meta">${job.company} · ${job.location}</p>
          <ul class="tl-item__points">
            ${job.points.map((p) => `<li>${p}</li>`).join("")}
          </ul>
        </div>
      </article>`
      )
      .join("");
  }

  /* ---------- Render: Projects ---------- */
  function renderProjects() {
    const root = $("#projects-grid");
    if (!root) return;
    root.innerHTML = PORTFOLIO_DATA.projects
      .map(
        (proj) => `
      <article class="card reveal">
        <div class="card__top">
          <span class="card__icon">${proj.icon}</span>
          <span class="card__year">${proj.year}</span>
        </div>
        <h3 class="card__title">${proj.title}</h3>
        <ul class="card__points">
          ${proj.points.map((p) => `<li>${p}</li>`).join("")}
        </ul>
        <div class="card__tags">
          ${proj.tags.map((t) => `<span class="tag">${t}</span>`).join("")}
        </div>
      </article>`
      )
      .join("");
  }

  /* ---------- Render: Skills ---------- */
  function renderSkills() {
    const root = $("#skills-grid");
    if (!root) return;
    root.innerHTML = PORTFOLIO_DATA.skills
      .map(
        (group) => `
      <div class="skill-group reveal">
        <h3 class="skill-group__title">${group.group}</h3>
        <div class="skill-group__items">
          ${group.items.map((i) => `<span class="chip">${i}</span>`).join("")}
        </div>
      </div>`
      )
      .join("");
  }

  /* ---------- Render: Achievements ---------- */
  function renderAchievements() {
    const awards = $("#awards-list");
    const certs = $("#certs-list");
    if (awards) {
      awards.innerHTML = PORTFOLIO_DATA.awards
        .map((a) => `<li>${a}</li>`)
        .join("");
    }
    if (certs) {
      certs.innerHTML = PORTFOLIO_DATA.certifications
        .map((c) => `<li>${c}</li>`)
        .join("");
    }
  }

  /* ---------- Render: Education ---------- */
  function renderEducation() {
    const root = $("#education-grid");
    if (!root) return;
    root.innerHTML = PORTFOLIO_DATA.education
      .map(
        (edu) => `
      <article class="edu reveal">
        <div class="edu__score">${edu.score}</div>
        <div class="edu__body">
          <h3>${edu.institution}</h3>
          <p>${edu.degree}</p>
          <span class="edu__year">${edu.year}</span>
        </div>
      </article>`
      )
      .join("");
  }

  /* ---------- Typed effect in hero ---------- */
  function initTyped() {
    const el = $("#typed");
    if (!el) return;
    const roles = PORTFOLIO_DATA.roles;
    let roleIdx = 0;
    let charIdx = 0;
    let deleting = false;

    function tick() {
      const current = roles[roleIdx];
      if (deleting) {
        charIdx--;
      } else {
        charIdx++;
      }
      el.textContent = current.slice(0, charIdx);

      let delay = deleting ? 45 : 90;
      if (!deleting && charIdx === current.length) {
        delay = 1800;
        deleting = true;
      } else if (deleting && charIdx === 0) {
        deleting = false;
        roleIdx = (roleIdx + 1) % roles.length;
        delay = 400;
      }
      setTimeout(tick, delay);
    }
    tick();
  }

  /* ---------- Scroll reveal ---------- */
  function initReveal() {
    const els = $$(".reveal");
    if (!("IntersectionObserver" in window)) {
      els.forEach((el) => el.classList.add("is-visible"));
      return;
    }
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    els.forEach((el) => obs.observe(el));
  }

  /* ---------- Animated counters ---------- */
  function initCounters() {
    const counters = $$(".stat__num");
    if (!counters.length) return;
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const target = parseFloat(el.dataset.target);
          const isFloat = target % 1 !== 0;
          let cur = 0;
          const step = target / 40;
          const run = () => {
            cur += step;
            if (cur >= target) {
              el.textContent = isFloat ? target.toFixed(2) : target;
            } else {
              el.textContent = isFloat ? cur.toFixed(2) : Math.floor(cur);
              requestAnimationFrame(run);
            }
          };
          run();
          obs.unobserve(el);
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((c) => obs.observe(c));
  }

  /* ---------- Nav: scroll state + mobile toggle ---------- */
  function initNav() {
    const nav = $("#nav");
    const toggle = $("#navToggle");
    const links = $("#navLinks");

    window.addEventListener("scroll", () => {
      if (window.scrollY > 40) nav.classList.add("nav--scrolled");
      else nav.classList.remove("nav--scrolled");
    });

    if (toggle && links) {
      toggle.addEventListener("click", () => {
        links.classList.toggle("is-open");
        toggle.classList.toggle("is-active");
      });
      $$("a", links).forEach((a) =>
        a.addEventListener("click", () => {
          links.classList.remove("is-open");
          toggle.classList.remove("is-active");
        })
      );
    }
  }

  /* ---------- Footer year ---------- */
  function initYear() {
    const y = $("#year");
    if (y) y.textContent = new Date().getFullYear();
  }

  /* ---------- Init ---------- */
  document.addEventListener("DOMContentLoaded", () => {
    renderExperience();
    renderProjects();
    renderSkills();
    renderAchievements();
    renderEducation();
    initTyped();
    initReveal();
    initCounters();
    initNav();
    initYear();
  });
})();
