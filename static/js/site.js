(() => {
  "use strict";

  const root = document.documentElement;
  const header = document.querySelector("[data-header]");
  const themeToggle = document.querySelector("[data-theme-toggle]");
  const likeToggle = document.querySelector("[data-like-toggle]");
  const likeCount = document.querySelector("[data-like-count]");
  const likeStatus = document.querySelector("[data-like-status]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const navigation = document.querySelector("[data-navigation]");
  const backToTop = document.querySelector("[data-back-to-top]");
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function setTheme(theme, persist = true) {
    // The dark palette is called "ink" to match the Southern Song art system.
    const nextTheme = theme === "ink" ? "ink" : "light";
    root.dataset.theme = nextTheme;

    if (themeToggle) {
      const isInk = nextTheme === "ink";
      themeToggle.setAttribute("aria-label", isInk ? "Use celadon light theme" : "Use ink theme");
      themeToggle.setAttribute("aria-pressed", String(isInk));
    }

    if (themeMeta) {
      themeMeta.setAttribute("content", nextTheme === "ink" ? "#18241f" : "#dce4dc");
    }

    if (persist) {
      try {
        localStorage.setItem("xiangye-theme", nextTheme);
      } catch (error) {
        /* Theme switching still works when browser storage is disabled. */
      }
    }
  }

  setTheme(root.dataset.theme, false);

  themeToggle?.addEventListener("click", () => {
    setTheme(root.dataset.theme === "ink" ? "light" : "ink");
  });

  const likeEndpoint = likeToggle?.dataset.likeEndpoint?.trim() || "";
  const likeNumberFormatter = new Intl.NumberFormat("en", {
    notation: "compact",
    maximumFractionDigits: 1,
  });
  let sharedLikeCount = null;

  function updateLikeLabel(liked) {
    if (!likeToggle) return;

    const action = liked ? "Remove your like" : "Like this website";
    const countText = Number.isInteger(sharedLikeCount)
      ? `. ${sharedLikeCount.toLocaleString("en")} ${sharedLikeCount === 1 ? "like" : "likes"}.`
      : ".";
    const titleCount = Number.isInteger(sharedLikeCount)
      ? ` · ${sharedLikeCount.toLocaleString("en")} ${sharedLikeCount === 1 ? "like" : "likes"}`
      : "";
    likeToggle.setAttribute("aria-label", `${action}${countText}`);
    likeToggle.setAttribute(
      "title",
      `${liked ? "Thank you — click to remove your like" : "Like this website"}${titleCount}`
    );
  }

  function setLikeCount(count) {
    if (!likeToggle || !likeCount) return;

    if (Number.isInteger(count) && count >= 0) {
      sharedLikeCount = count;
      likeCount.textContent = likeNumberFormatter.format(count);
      likeToggle.dataset.countState = "ready";
    } else {
      sharedLikeCount = null;
      likeCount.textContent = "—";
      likeToggle.dataset.countState = likeEndpoint ? "unavailable" : "local";
    }

    updateLikeLabel(likeToggle.getAttribute("aria-pressed") === "true");
  }

  function setLiked(liked, persist = true, announcement = "") {
    if (!likeToggle) return;

    likeToggle.setAttribute("aria-pressed", String(liked));
    updateLikeLabel(liked);

    if (announcement && likeStatus) {
      likeStatus.textContent = announcement;
    }

    if (persist) {
      try {
        localStorage.setItem("xiangye-site-liked", String(liked));
      } catch (error) {
        /* The control still works for this visit when storage is unavailable. */
      }
    }
  }

  function getLikeVisitorId() {
    const storageKey = "xiangye-like-visitor";

    try {
      const saved = localStorage.getItem(storageKey);
      if (saved && /^[A-Za-z0-9_-]{20,80}$/.test(saved)) return saved;

      let visitorId;
      if (typeof crypto.randomUUID === "function") {
        visitorId = crypto.randomUUID();
      } else {
        const randomBytes = new Uint8Array(20);
        crypto.getRandomValues(randomBytes);
        visitorId = [...randomBytes].map((byte) => byte.toString(16).padStart(2, "0")).join("");
      }

      localStorage.setItem(storageKey, visitorId);
      return visitorId;
    } catch (error) {
      return null;
    }
  }

  async function fetchLikeData(options = {}) {
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 6500);

    try {
      const response = await fetch(likeEndpoint, {
        ...options,
        cache: "no-store",
        signal: controller.signal,
      });
      if (!response.ok) throw new Error(`Like counter returned ${response.status}`);

      const data = await response.json();
      if (!Number.isInteger(data.count) || data.count < 0) {
        throw new Error("Like counter returned an invalid count");
      }
      return data;
    } finally {
      window.clearTimeout(timeout);
    }
  }

  let savedLike = false;
  try {
    savedLike = localStorage.getItem("xiangye-site-liked") === "true";
  } catch (error) {
    /* An unliked heart is the safe default. */
  }
  setLiked(savedLike, false);
  setLikeCount(null);

  if (likeEndpoint) {
    fetchLikeData()
      .then((data) => setLikeCount(data.count))
      .catch(() => setLikeCount(null));
  }

  likeToggle?.addEventListener("click", async () => {
    const willLike = likeToggle.getAttribute("aria-pressed") !== "true";
    let didLike = false;

    if (!likeEndpoint) {
      const message = willLike
        ? "Thank you for liking this website. The shared counter is not connected yet."
        : "Your local like was removed.";
      setLiked(willLike, true, message);
      didLike = willLike;
    } else {
      const visitorId = getLikeVisitorId();
      if (!visitorId) {
        if (likeStatus) likeStatus.textContent = "This browser could not save your like.";
        return;
      }

      likeToggle.disabled = true;
      likeToggle.setAttribute("aria-busy", "true");

      try {
        const data = await fetchLikeData({
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ visitor_id: visitorId, liked: willLike }),
        });
        const confirmedLike = typeof data.liked === "boolean" ? data.liked : willLike;
        const message = confirmedLike
          ? `Thank you. This website now has ${data.count.toLocaleString("en")} ${data.count === 1 ? "like" : "likes"}.`
          : `Your like was removed. ${data.count.toLocaleString("en")} ${data.count === 1 ? "like remains" : "likes remain"}.`;
        setLiked(confirmedLike, true, message);
        setLikeCount(data.count);
        didLike = confirmedLike;
      } catch (error) {
        setLikeCount(null);
        if (likeStatus) likeStatus.textContent = "The shared like counter is temporarily unavailable. Please try again.";
      } finally {
        likeToggle.disabled = false;
        likeToggle.removeAttribute("aria-busy");
      }
    }

    if (didLike && !reduceMotion.matches) {
      likeToggle.classList.remove("just-liked");
      window.requestAnimationFrame(() => likeToggle.classList.add("just-liked"));
    }
  });

  function closeMenu() {
    if (!header || !menuToggle) return;
    header.classList.remove("is-menu-open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Open navigation");
    document.body.style.removeProperty("overflow");
  }

  function toggleMenu() {
    if (!header || !menuToggle) return;
    const willOpen = !header.classList.contains("is-menu-open");
    header.classList.toggle("is-menu-open", willOpen);
    menuToggle.setAttribute("aria-expanded", String(willOpen));
    menuToggle.setAttribute("aria-label", willOpen ? "Close navigation" : "Open navigation");
    document.body.style.overflow = willOpen ? "hidden" : "";
  }

  menuToggle?.addEventListener("click", toggleMenu);
  navigation?.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 1040) closeMenu();
  });

  let scrollFrame = 0;
  function updateOnScroll() {
    const y = window.scrollY;
    header?.classList.toggle("is-scrolled", y > 18);
    backToTop?.classList.toggle("is-visible", y > 650);
    scrollFrame = 0;
  }

  window.addEventListener(
    "scroll",
    () => {
      if (!scrollFrame) scrollFrame = window.requestAnimationFrame(updateOnScroll);
    },
    { passive: true }
  );
  updateOnScroll();

  backToTop?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: reduceMotion.matches ? "auto" : "smooth" });
  });

  const revealItems = [...document.querySelectorAll("[data-reveal]")];
  if (reduceMotion.matches || !("IntersectionObserver" in window)) {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  } else {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -7% 0px" }
    );
    revealItems.forEach((item) => revealObserver.observe(item));
  }

  const portrait = document.querySelector("[data-parallax]");
  const finePointer = window.matchMedia("(pointer: fine)");
  if (portrait && finePointer.matches && !reduceMotion.matches) {
    let pointerFrame = 0;
    let nextX = 0;
    let nextY = 0;

    function renderPortrait() {
      portrait.style.transform = `perspective(900px) rotateX(${nextY}deg) rotateY(${nextX}deg)`;
      pointerFrame = 0;
    }

    portrait.addEventListener("pointermove", (event) => {
      const bounds = portrait.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width - 0.5;
      const y = (event.clientY - bounds.top) / bounds.height - 0.5;
      nextX = x * 5;
      nextY = y * -4;
      if (!pointerFrame) pointerFrame = window.requestAnimationFrame(renderPortrait);
    });

    portrait.addEventListener("pointerleave", () => {
      nextX = 0;
      nextY = 0;
      if (!pointerFrame) pointerFrame = window.requestAnimationFrame(renderPortrait);
    });
  }
})();
