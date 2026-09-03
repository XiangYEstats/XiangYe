(() => {
  "use strict";

  const root = document.documentElement;
  const header = document.querySelector("[data-header]");
  const languageToggle = document.querySelector("[data-language-toggle]");
  const themeToggle = document.querySelector("[data-theme-toggle]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const navigation = document.querySelector("[data-navigation]");
  const backToTop = document.querySelector("[data-back-to-top]");
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  const messages = {
    en: {
      switchLanguage: "Switch site language to Chinese",
      useInkTheme: "Use ink theme",
      useLightTheme: "Use celadon light theme",
      openNavigation: "Open navigation",
      closeNavigation: "Close navigation",
      backToTop: "Back to top",
    },
    zh: {
      switchLanguage: "切换至英文",
      useInkTheme: "切换至墨色主题",
      useLightTheme: "切换至青瓷浅色主题",
      openNavigation: "展开导航菜单",
      closeNavigation: "收起导航菜单",
      backToTop: "返回页首",
    },
  };

  function currentLanguage() {
    return root.dataset.language === "zh" ? "zh" : "en";
  }

  function updateThemeLabel() {
    if (!themeToggle) return;
    const copy = messages[currentLanguage()];
    themeToggle.setAttribute(
      "aria-label",
      root.dataset.theme === "ink" ? copy.useLightTheme : copy.useInkTheme
    );
  }

  function updateMenuLabel() {
    if (!menuToggle) return;
    const copy = messages[currentLanguage()];
    const isOpen = Boolean(header?.classList.contains("is-menu-open"));
    menuToggle.setAttribute("aria-label", isOpen ? copy.closeNavigation : copy.openNavigation);
  }

  function updateLocalizedAttributes(language) {
    const attributeSuffix = language === "zh" ? "zh" : "en";

    document.querySelectorAll("[data-label-en][data-label-zh]").forEach((element) => {
      element.setAttribute("aria-label", element.getAttribute(`data-label-${attributeSuffix}`));
    });

    document.querySelectorAll("[data-alt-en][data-alt-zh]").forEach((element) => {
      element.setAttribute("alt", element.getAttribute(`data-alt-${attributeSuffix}`));
    });

    document.querySelectorAll("[data-content-en][data-content-zh]").forEach((element) => {
      element.setAttribute("content", element.getAttribute(`data-content-${attributeSuffix}`));
    });

    const title = document.querySelector("title[data-title-en][data-title-zh]");
    if (title) title.textContent = title.getAttribute(`data-title-${attributeSuffix}`);

    languageToggle?.setAttribute("aria-label", messages[language].switchLanguage);
    backToTop?.setAttribute("aria-label", messages[language].backToTop);
    updateThemeLabel();
    updateMenuLabel();
  }

  function setLanguage(language, persist = true) {
    const nextLanguage = language === "zh" ? "zh" : "en";
    root.dataset.language = nextLanguage;
    root.lang = nextLanguage === "zh" ? "zh-Hans" : "en";
    updateLocalizedAttributes(nextLanguage);

    if (persist) {
      try {
        localStorage.setItem("xiangye-language", nextLanguage);
      } catch (error) {
        /* Language switching still works when browser storage is disabled. */
      }
    }
  }

  function setTheme(theme, persist = true) {
    // The dark palette is called "ink" to match the Southern Song art system.
    const nextTheme = theme === "ink" ? "ink" : "light";
    root.dataset.theme = nextTheme;

    if (themeToggle) themeToggle.setAttribute("aria-pressed", String(nextTheme === "ink"));
    updateThemeLabel();

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

  setLanguage(root.dataset.language, false);
  setTheme(root.dataset.theme, false);

  languageToggle?.addEventListener("click", () => {
    setLanguage(currentLanguage() === "en" ? "zh" : "en");
  });

  themeToggle?.addEventListener("click", () => {
    setTheme(root.dataset.theme === "ink" ? "light" : "ink");
  });

  function closeMenu() {
    if (!header || !menuToggle) return;
    header.classList.remove("is-menu-open");
    menuToggle.setAttribute("aria-expanded", "false");
    updateMenuLabel();
    document.body.style.removeProperty("overflow");
  }

  function toggleMenu() {
    if (!header || !menuToggle) return;
    const willOpen = !header.classList.contains("is-menu-open");
    header.classList.toggle("is-menu-open", willOpen);
    menuToggle.setAttribute("aria-expanded", String(willOpen));
    updateMenuLabel();
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
