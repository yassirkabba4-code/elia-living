/* Elia Living — interaction & motion layer.
   Everything here is progressive: without this file every page still reads completely. */
(() => {
  "use strict";
  const root = document.documentElement;
  const body = document.body;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const easeOut = t => 1 - Math.pow(1 - t, 3);
  const easeIO = t => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const store = {
    get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} },
    del(k) { try { sessionStorage.removeItem(k); } catch (e) {} }
  };
  const WA = "34645054102";
  const EMAIL = "info@elialiving.es";

  /* ---------------- toast ---------------- */
  let toastEl;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); body.appendChild(toastEl); }
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastEl._t);
    toastEl._t = setTimeout(() => toastEl.classList.remove("show"), 2400);
  }

  /* ---------------- page curtain transitions ---------------- */
  const curtain = $(".curtain");
  function arrive() {
    if (!curtain) return;
    if (root.classList.contains("is-arriving")) {
      const wait = root.classList.contains("intro") ? 1100 : 60;
      setTimeout(() => requestAnimationFrame(() => {
        curtain.classList.add("leave");
        root.classList.remove("is-arriving");
        root.classList.remove("intro");
        setTimeout(() => curtain.classList.remove("leave"), 1100);
      }), wait);
    }
    store.del("el-nav");
  }
  function isInternal(a) {
    if (!a || a.target === "_blank" || a.hasAttribute("download")) return false;
    const href = a.getAttribute("href") || "";
    if (!href || href.startsWith("#") || /^(mailto|tel|https?|sms|whatsapp):/i.test(href)) return false;
    return /\.html(#.*)?$/.test(href);
  }
  document.addEventListener("click", e => {
    const a = e.target.closest("a");
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    if (!isInternal(a)) return;
    const url = a.href;
    if (url.split("#")[0] === location.href.split("#")[0]) return;
    if (reduce || !curtain) return;
    e.preventDefault();
    closeMenu(true);
    store.set("el-nav", "1");
    curtain.classList.remove("leave");
    curtain.classList.add("enter");
    setTimeout(() => { location.href = url; }, 760);
  });
  window.addEventListener("pageshow", ev => {
    if (ev.persisted && curtain) { curtain.classList.remove("enter", "leave"); root.classList.remove("is-arriving"); }
  });

  /* ---------------- smooth scroll ---------------- */
  let lenis = null;
  if (!reduce && fine && window.Lenis) {
    try {
      lenis = new window.Lenis({ duration: 1.15, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
    } catch (e) { lenis = null; }
  }
  function scrollToEl(el, offset = 0) {
    if (!el) return;
    if (lenis) lenis.scrollTo(el, { offset: -offset, duration: 1.4 });
    else window.scrollTo({ top: el.getBoundingClientRect().top + scrollY - offset, behavior: reduce ? "auto" : "smooth" });
  }
  document.addEventListener("click", e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute("href").slice(1);
    const el = id && document.getElementById(id);
    if (!el) return;
    e.preventDefault();
    closeMenu(true);
    scrollToEl(el, 140);
    history.replaceState(null, "", "#" + id);
  });

  /* ---------------- header ---------------- */
  const header = $(".site-header");
  let lastY = scrollY, solidAfter = 40;
  function computeSolidAfter() {
    const h = $("[data-hero-end]");
    solidAfter = h ? Math.max(40, h.offsetTop + h.offsetHeight - window.innerHeight * .9) : 40;
  }
  function headerTick(y) {
    if (!header) return;
    header.classList.toggle("is-solid", y > solidAfter);
    const goingDown = y > lastY + 4, goingUp = y < lastY - 4;
    if (y > Math.max(solidAfter, 240) && goingDown && !body.classList.contains("menu-open")) header.classList.add("is-hidden");
    else if (goingUp || y < 120) header.classList.remove("is-hidden");
    body.classList.toggle("header-shown", !header.classList.contains("is-hidden") && y > 120);
    lastY = y;
  }

  /* ---------------- menu ---------------- */
  const menuBtn = $(".menu-btn");
  const menu = $(".menu");
  function openMenu() {
    body.classList.add("menu-open"); root.classList.add("menu-open");
    menuBtn && menuBtn.setAttribute("aria-expanded", "true");
    menu && menu.setAttribute("aria-hidden", "false");
    lenis && lenis.stop();
    header && header.classList.remove("is-hidden");
  }
  function closeMenu(silent) {
    if (!body.classList.contains("menu-open")) return;
    body.classList.remove("menu-open"); root.classList.remove("menu-open");
    menuBtn && menuBtn.setAttribute("aria-expanded", "false");
    menu && menu.setAttribute("aria-hidden", "true");
    lenis && lenis.start();
    if (!silent) menuBtn && menuBtn.focus();
  }
  menuBtn && menuBtn.addEventListener("click", () => body.classList.contains("menu-open") ? closeMenu() : openMenu());
  document.addEventListener("keydown", e => { if (e.key === "Escape") closeMenu(); });
  if (menu) {
    const imgs = $$(".menu__preview img", menu);
    $$(".menu__links a", menu).forEach(a => a.addEventListener("mouseenter", () => {
      const k = a.dataset.preview;
      imgs.forEach(i => i.classList.toggle("on", i.dataset.key === k));
    }));
  }

  /* ---------------- split text ---------------- */
  $$(".split").forEach(el => {
    let wi = 0;
    const walk = node => {
      Array.from(node.childNodes).forEach(n => {
        if (n.nodeType === 3) {
          const parts = n.textContent.split(/(\s+)/);
          const frag = document.createDocumentFragment();
          parts.forEach(p => {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            const w = document.createElement("span"); w.className = "w";
            const i = document.createElement("span"); i.textContent = p; i.style.setProperty("--wi", wi++);
            w.appendChild(i); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && !n.classList.contains("w")) walk(n);
      });
    };
    walk(el);
    if (!el.hasAttribute("data-reveal")) el.setAttribute("data-reveal", "fade");
  });

  /* statement words lit by scroll */
  $$(".statement__big").forEach(el => {
    const txt = el.textContent.trim().split(/\s+/);
    el.innerHTML = txt.map(w => `<span class="sw">${w}</span>`).join(" ");
  });

  /* ---------------- reveal on view ---------------- */
  const revealEls = $$("[data-reveal]");
  if (!root.classList.contains("motion")) revealEls.forEach(el => el.classList.add("in"));
  else if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
    }), { rootMargin: "0px 0px -8% 0px", threshold: 0.01 });
    revealEls.forEach(el => io.observe(el));
  } else revealEls.forEach(el => el.classList.add("in"));

  /* ---------------- scroll scenes ---------------- */
  const vh = () => window.innerHeight;
  const vw = () => window.innerWidth;
  const scenes = [];
  const sceneProgress = el => { const r = el.getBoundingClientRect(); const span = r.height - vh(); return span > 0 ? clamp(-r.top / span) : 0; };
  const inView = el => { const r = el.getBoundingClientRect(); return r.bottom > -100 && r.top < vh() + 100; };

  // Home hero: full bleed → Mediterranean arch
  const heroScene = $(".hero-scene");
  if (heroScene && !reduce) {
    const media = $(".hero__media", heroScene), img = $(".hero__media img", heroScene);
    const l1 = $(".hero__title .l1", heroScene), l2 = $(".hero__title .l2", heroScene);
    const title = $(".hero__title", heroScene), meta = $(".hero__meta", heroScene), after = $(".hero__after", heroScene), shade = $(".hero__shade", heroScene);
    scenes.push(() => {
      if (!inView(heroScene)) return;
      const p = sceneProgress(heroScene);
      const t = easeIO(clamp(p / .78));
      const W = vw(), H = vh(), mob = W < 700;
      const side = lerp(0, mob ? W * .1 : W * .31, t);
      const top = lerp(0, mob ? H * .16 : H * .13, t);
      const bot = lerp(0, mob ? H * .2 : H * .17, t);
      const rad = ((W - side * 2) / 2) * t;
      media.style.clipPath = `inset(${top}px ${side}px ${bot}px ${side}px round ${rad}px ${rad}px 0px 0px)`;
      img.style.transform = `scale(${1.14 - .14 * t}) translateY(${t * -2}%)`;
      if (l1) l1.style.transform = `translateX(${-t * 10}vw)`;
      if (l2) l2.style.transform = `translateX(${t * 10}vw)`;
      title.style.opacity = 1 - clamp(p * 2.4);
      meta.style.opacity = 1 - clamp(p * 4);
      shade.style.opacity = 1 - t;
      after.style.opacity = clamp((p - .55) / .25);
      after.style.transform = `translateY(${(1 - clamp((p - .55) / .25)) * 24}px)`;
      body.classList.toggle("hdr-ink", p > .2);
    });
  }

  // Horizontal residences
  $$(".hscroll").forEach(sec => {
    const track = $(".hscroll__track", sec), bar = $(".hscroll__progress i", sec);
    let dist = 0;
    const size = () => {
      if (vw() <= 900 || reduce) { sec.style.height = ""; track.style.transform = ""; dist = 0; return; }
      dist = Math.max(0, track.scrollWidth - vw());
      sec.style.height = (vh() + dist) + "px";
    };
    size(); window.addEventListener("resize", size); window.addEventListener("load", size);
    scenes.push(() => {
      if (!dist || !inView(sec)) return;
      const p = sceneProgress(sec);
      track.style.transform = `translate3d(${-dist * p}px,0,0)`;
      if (bar) bar.style.transform = `scaleX(${p})`;
    });
  });

  // Expanding editorial frame
  $$(".fx-scene").forEach(sec => {
    if (reduce) return;
    const clip = $(".fx__img", sec), img = $(".fx__img img", sec);
    const a = $(".fx__label .a", sec), b = $(".fx__label .b", sec), cap = $(".fx__caption", sec), shade = $(".fx__shade", sec);
    scenes.push(() => {
      if (!inView(sec)) return;
      const p = sceneProgress(sec);
      const t = easeIO(clamp(p / .7));
      const mob = vw() < 700;
      const sy = lerp(mob ? 26 : 22, 0, t), sx = lerp(mob ? 12 : 33, 0, t);
      clip.style.clipPath = `inset(${sy}% ${sx}% ${sy}% ${sx}%)`;
      img.style.transform = `scale(${1.25 - .25 * t})`;
      const off = t * 30;
      if (a) { a.style.transform = `translateY(${-off}vh)`; a.style.opacity = 1 - clamp(t * 1.6); }
      if (b) { b.style.transform = `translateY(${off}vh)`; b.style.opacity = 1 - clamp(t * 1.6); }
      const c = clamp((p - .68) / .18);
      cap.style.opacity = c; cap.style.transform = `translateY(${(1 - c) * 20}px)`;
      cap.style.pointerEvents = c > .5 ? "auto" : "none";
      shade.style.opacity = c;
    });
  });

  // Property hero: framed image opens to full bleed
  $$(".p-heroimg-scene").forEach(sec => {
    if (reduce) return;
    const clip = $(".p-heroimg__clip", sec), img = $("img", clip);
    scenes.push(() => {
      if (!inView(sec)) return;
      const p = sceneProgress(sec);
      const t = easeOut(clamp(p / .7));
      const g = parseFloat(getComputedStyle(root).getPropertyValue("--gutter")) || 24;
      const gut = Math.min(64, Math.max(18, vw() * .042));
      const side = lerp(gut, 0, t), bot = lerp(vh() * .12, 0, t);
      clip.style.clipPath = `inset(0px ${side}px ${bot}px ${side}px)`;
      img.style.transform = `scale(${1.12 - .12 * t})`;
      void g;
    });
  });

  // Statement words
  $$(".statement__big").forEach(el => {
    const words = $$(".sw", el);
    if (reduce) { words.forEach(w => w.classList.add("lit")); return; }
    scenes.push(() => {
      const r = el.getBoundingClientRect();
      if (r.bottom < -50 || r.top > vh()) return;
      const p = clamp((vh() * .82 - r.top) / (r.height + vh() * .35));
      const n = Math.round(p * words.length * 1.05);
      words.forEach((w, i) => w.classList.toggle("lit", i < n));
    });
  });

  // Parallax
  const para = $$("[data-parallax]");
  if (!reduce) scenes.push(() => {
    para.forEach(el => {
      const host = el.parentElement;
      const r = host.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh() + 200) return;
      const f = parseFloat(el.dataset.parallax) || .12;
      const c = (r.top + r.height / 2 - vh() / 2);
      el.style.transform = `translate3d(0,${-c * f}px,0)`;
    });
  });

  function frame(t) {
    if (lenis) lenis.raf(t);
    const y = lenis ? lenis.scroll : scrollY;
    headerTick(y);
    for (const s of scenes) s();
    requestAnimationFrame(frame);
  }
  computeSolidAfter();
  window.addEventListener("resize", computeSolidAfter);
  window.addEventListener("load", computeSolidAfter);
  requestAnimationFrame(frame);

  /* ---------------- cursor ---------------- */
  if (fine && !reduce) {
    const c = document.createElement("div"); c.className = "cursor"; c.innerHTML = "<span></span>"; body.appendChild(c);
    const lab = c.firstChild;
    let x = -100, y = -100, cx = x, cy = y;
    window.addEventListener("pointermove", e => { x = e.clientX; y = e.clientY; c.classList.add("on"); }, { passive: true });
    document.addEventListener("pointerleave", () => c.classList.remove("on"));
    document.addEventListener("pointerover", e => {
      const t = e.target.closest("[data-cursor]");
      if (t) { lab.textContent = t.dataset.cursor; c.classList.add("big"); } else c.classList.remove("big");
    });
    (function loop() { cx = lerp(cx, x, .2); cy = lerp(cy, y, .2); c.style.transform = `translate3d(${cx}px,${cy}px,0)`; requestAnimationFrame(loop); })();
  }

  /* ---------------- towns floating preview ---------------- */
  const tf = $(".towns__float");
  if (tf && fine) {
    const list = $(".towns__list"), imgs = $$("img", tf);
    let tx = 0, ty = 0, fx = 0, fy = 0, on = false;
    list.addEventListener("pointermove", e => { tx = e.clientX; ty = e.clientY; });
    $$(".town a", list).forEach(a => a.addEventListener("mouseenter", () => {
      imgs.forEach(i => i.classList.toggle("on", i.dataset.key === a.dataset.key));
      on = true; tf.style.opacity = 1;
    }));
    list.addEventListener("mouseleave", () => { on = false; tf.style.opacity = 0; });
    (function loop() { fx = lerp(fx, tx, .14); fy = lerp(fy, ty, .14); tf.style.transform = `translate3d(${fx}px,${fy}px,0) translate(-50%,-50%) scale(${on ? 1 : .85}) rotate(${(tx - fx) * .02}deg)`; requestAnimationFrame(loop); })();
  }

  /* ---------------- properties filter ---------------- */
  const grid = $(".pgrid");
  if (grid) {
    const cards = $$(".pcard", grid);
    const empty = $(".pgrid__empty");
    const count = $(".filters__count");
    const state = { loc: "all", beds: "any", sort: "featured", q: "" };
    const apply = () => {
      let shown = cards.filter(c => {
        const okLoc = state.loc === "all" || c.dataset.loc === state.loc;
        const okBeds = state.beds === "any" || +c.dataset.beds >= +state.beds;
        const q = state.q.trim().toLowerCase();
        const okQ = !q || (c.dataset.ref + " " + c.dataset.name + " " + c.dataset.loc).toLowerCase().includes(q);
        return okLoc && okBeds && okQ;
      });
      const order = [...cards];
      if (state.sort === "price-asc") order.sort((a, b) => a.dataset.price - b.dataset.price);
      if (state.sort === "price-desc") order.sort((a, b) => b.dataset.price - a.dataset.price);
      if (state.sort === "featured") order.sort((a, b) => a.dataset.order - b.dataset.order);
      cards.forEach(c => c.classList.add("is-out"));
      setTimeout(() => {
        order.forEach(c => grid.insertBefore(c, empty));
        cards.forEach(c => { c.hidden = !shown.includes(c); });
        requestAnimationFrame(() => shown.forEach((c, i) => setTimeout(() => c.classList.remove("is-out"), i * 70)));
        empty.hidden = shown.length > 0;
        count.textContent = shown.length === 1 ? "1 residence" : `${shown.length} residences`;
      }, reduce ? 0 : 280);
    };
    $$(".chip[data-loc]").forEach(b => b.addEventListener("click", () => {
      state.loc = b.dataset.loc;
      $$(".chip[data-loc]").forEach(x => x.setAttribute("aria-pressed", x === b ? "true" : "false"));
      apply();
    }));
    const bedsSel = $("#f-beds"), sortSel = $("#f-sort"), q = $("#f-ref");
    bedsSel && bedsSel.addEventListener("change", () => { state.beds = bedsSel.value; apply(); });
    sortSel && sortSel.addEventListener("change", () => { state.sort = sortSel.value; apply(); });
    q && q.addEventListener("input", () => { state.q = q.value; clearTimeout(q._t); q._t = setTimeout(apply, 180); });
    const reset = $("#f-reset");
    reset && reset.addEventListener("click", () => {
      state.loc = "all"; state.beds = "any"; state.q = ""; state.sort = "featured";
      if (bedsSel) bedsSel.value = "any"; if (sortSel) sortSel.value = "featured"; if (q) q.value = "";
      $$(".chip[data-loc]").forEach(x => x.setAttribute("aria-pressed", x.dataset.loc === "all" ? "true" : "false"));
      apply();
    });
  }

  /* ---------------- gallery + lightbox ---------------- */
  $$("[data-gallery]").forEach(g => {
    const slides = $$(".gallery__slide", g), thumbs = $$(".gallery__thumbs button", g);
    const cur = $(".gallery__count b", g);
    const n = slides.length; let i = 0;
    const load = k => { const s = slides[(k + n) % n]; const im = s && $("img", s); if (im && im.dataset.src) { im.src = im.dataset.src; im.removeAttribute("data-src"); } };
    const go = k => {
      i = (k + n) % n;
      slides.forEach((s, j) => s.classList.toggle("on", j === i));
      thumbs.forEach((t, j) => t.classList.toggle("on", j === i));
      load(i); load(i + 1); load(i - 1);
      if (cur) cur.textContent = String(i + 1).padStart(2, "0");
      const th = thumbs[i];
      if (th) { const bar = th.parentElement; bar.scrollTo({ left: th.offsetLeft - bar.clientWidth / 2 + th.clientWidth / 2, behavior: reduce ? "auto" : "smooth" }); }
    };
    $(".gprev", g) && $(".gprev", g).addEventListener("click", () => go(i - 1));
    $(".gnext", g) && $(".gnext", g).addEventListener("click", () => go(i + 1));
    thumbs.forEach((t, j) => t.addEventListener("click", () => go(j)));
    const stage = $(".gallery__stage", g);
    let sx = null, moved = false;
    stage.addEventListener("pointerdown", e => { sx = e.clientX; moved = false; });
    stage.addEventListener("pointerup", e => {
      if (sx === null) return;
      const dx = e.clientX - sx; sx = null;
      if (Math.abs(dx) > 40) { moved = true; go(i + (dx < 0 ? 1 : -1)); }
    });
    stage.addEventListener("click", () => { if (!moved) openLB(i); });
    g.addEventListener("keydown", e => { if (e.key === "ArrowRight") go(i + 1); if (e.key === "ArrowLeft") go(i - 1); });
    go(0);

    // lightbox
    const lb = $(".lightbox");
    if (!lb) return;
    const lbImg = $(".lightbox__img img", lb), lbCount = $(".lightbox__count", lb);
    let li = 0;
    const full = k => { const s = slides[k]; const im = $("img", s); return im.dataset.src || im.getAttribute("src"); };
    const show = k => {
      li = (k + n) % n;
      lbImg.style.opacity = 0;
      const src = full(li);
      const pre = new Image(); pre.onload = pre.onerror = () => { lbImg.src = src; lbImg.style.opacity = 1; }; pre.src = src;
      lbCount.textContent = `${String(li + 1).padStart(2, "0")} / ${String(n).padStart(2, "0")}`;
    };
    function openLB(k) { lb.classList.add("open"); lb.setAttribute("aria-hidden", "false"); lenis && lenis.stop(); show(k); $(".lightbox__close", lb).focus(); }
    function closeLB() { lb.classList.remove("open"); lb.setAttribute("aria-hidden", "true"); lenis && lenis.start(); go(li); }
    $(".lightbox__close", lb).addEventListener("click", closeLB);
    $(".lbprev", lb).addEventListener("click", () => show(li - 1));
    $(".lbnext", lb).addEventListener("click", () => show(li + 1));
    document.addEventListener("keydown", e => {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") closeLB();
      if (e.key === "ArrowRight") show(li + 1);
      if (e.key === "ArrowLeft") show(li - 1);
    });
    let lx = null;
    lb.addEventListener("pointerdown", e => { lx = e.clientX; });
    lb.addEventListener("pointerup", e => { if (lx === null) return; const dx = e.clientX - lx; lx = null; if (Math.abs(dx) > 50) show(li + (dx < 0 ? 1 : -1)); });
  });

  /* ---------------- section-aware indexes ---------------- */
  function spy(linkSel, attr) {
    const links = $$(linkSel); if (!links.length || !("IntersectionObserver" in window)) return;
    const map = new Map(links.map(a => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { links.forEach(l => l.classList.remove(attr)); const a = map.get(en.target.id); a && a.classList.add(attr); }
    }), { rootMargin: "-40% 0px -55% 0px" });
    map.forEach((a, id) => { const el = document.getElementById(id); el && io.observe(el); });
  }
  spy(".story__nav a", "on");
  spy(".svc-index a", "on");

  /* ---------------- team bios ---------------- */
  $$(".member__more").forEach(b => b.addEventListener("click", () => {
    const m = b.closest(".member"); const o = m.classList.toggle("open");
    b.textContent = o ? "Show less" : "Read more"; b.setAttribute("aria-expanded", o);
  }));

  /* ---------------- town tabs ---------------- */
  $$(".townx").forEach(t => {
    const tabs = $$("[role=tab]", t), imgs = $$(".townx__stage img", t), cap = $(".townx__cap", t);
    const sel = k => {
      tabs.forEach(b => b.setAttribute("aria-selected", b.dataset.key === k ? "true" : "false"));
      imgs.forEach(i => i.classList.toggle("on", i.dataset.key === k));
      const b = tabs.find(x => x.dataset.key === k); if (cap && b) cap.textContent = b.dataset.cap;
    };
    tabs.forEach(b => { b.addEventListener("click", () => sel(b.dataset.key)); if (fine) b.addEventListener("mouseenter", () => sel(b.dataset.key)); });
    t.addEventListener("keydown", e => {
      const idx = tabs.findIndex(b => b.getAttribute("aria-selected") === "true");
      if (e.key === "ArrowDown" || e.key === "ArrowRight") { e.preventDefault(); const n = tabs[(idx + 1) % tabs.length]; sel(n.dataset.key); n.focus(); }
      if (e.key === "ArrowUp" || e.key === "ArrowLeft") { e.preventDefault(); const n = tabs[(idx - 1 + tabs.length) % tabs.length]; sel(n.dataset.key); n.focus(); }
    });
  });

  /* ---------------- drag-to-scroll rails ---------------- */
  $$(".nature").forEach(r => {
    if (!fine) return;
    let down = false, sx = 0, sl = 0;
    r.addEventListener("pointerdown", e => { down = true; sx = e.clientX; sl = r.scrollLeft; r.classList.add("drag"); });
    window.addEventListener("pointerup", () => { down = false; r.classList.remove("drag"); });
    r.addEventListener("pointermove", e => { if (down) r.scrollLeft = sl - (e.clientX - sx); });
    r.addEventListener("wheel", e => { if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) return; e.stopPropagation(); }, { passive: true });
  });

  /* ---------------- video ---------------- */
  $$(".videoband").forEach(v => {
    const vid = $("video", v), btn = $(".vtoggle", v);
    if (!vid) return;
    if (reduce) { vid.removeAttribute("autoplay"); vid.pause(); if (btn) btn.textContent = "Play film"; }
    btn && btn.addEventListener("click", () => { if (vid.paused) { vid.play(); btn.textContent = "Pause film"; } else { vid.pause(); btn.textContent = "Play film"; } });
    vid.addEventListener("error", () => { v.hidden = true; }, true);
  });

  /* ---------------- copy buttons ---------------- */
  $$("[data-copy]").forEach(b => b.addEventListener("click", () => {
    const val = b.dataset.copy;
    const done = () => toast("Copied: " + val);
    if (navigator.clipboard) navigator.clipboard.writeText(val).then(done, () => toast(val));
    else toast(val);
  }));

  /* ---------------- forms ---------------- */
  $$("form[data-form]").forEach(f => {
    const ready = $(".form__ready", f);
    f.addEventListener("submit", e => {
      e.preventDefault();
      let ok = true;
      $$("[required]", f).forEach(inp => {
        const fld = inp.closest(".field");
        const bad = inp.type === "checkbox" ? !inp.checked : (!inp.value.trim() || (inp.type === "email" && !/^\S+@\S+\.\S+$/.test(inp.value)));
        if (fld) fld.classList.toggle("bad", bad);
        if (bad) ok = false;
      });
      if (!ok) { const first = $(".field.bad input, .field.bad textarea, .field.bad select", f); first && first.focus(); return; }
      const kind = f.dataset.form;
      const fd = new FormData(f);
      const lines = [];
      const subject = f.dataset.subject || "Enquiry via elialiving.es";
      for (const [k, v] of fd.entries()) { if (v && String(v).trim()) lines.push(`${k}: ${v}`); }
      const text = (kind === "newsletter" ? "Please add me to the Elia Living newsletter.\n" : "") + lines.join("\n");
      if (kind === "newsletter") {
        location.href = `mailto:${EMAIL}?subject=${encodeURIComponent("Newsletter subscription")}&body=${encodeURIComponent(text)}`;
        toast("Opening your email app to confirm");
        return;
      }
      if (ready) {
        $(".ready-wa", ready).href = `https://wa.me/${WA}?text=${encodeURIComponent(subject + "\n\n" + text)}`;
        $(".ready-mail", ready).href = `mailto:${EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(text)}`;
        ready.hidden = false;
        ready.scrollIntoView({ block: "nearest", behavior: reduce ? "auto" : "smooth" });
      }
    });
    $$("input,textarea,select", f).forEach(inp => inp.addEventListener("input", () => { const fld = inp.closest(".field"); fld && fld.classList.remove("bad"); }));
  });

  /* ---------------- image fallbacks & fade ---------------- */
  $$("img[data-fb]").forEach(im => {
    im.addEventListener("error", function once() { im.removeEventListener("error", once); if (im.dataset.fb && im.src !== im.dataset.fb) im.src = im.dataset.fb; });
  });

  arrive();
})();
