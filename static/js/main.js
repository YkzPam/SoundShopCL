document.addEventListener("DOMContentLoaded", () => {
  const root = document.documentElement;
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  const menuButton = document.querySelector("[data-menu-button]");
  const mobileMenu = document.querySelector("[data-mobile-menu]");

  if (menuButton && mobileMenu) {
    menuButton.addEventListener("click", () => {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
      menuButton.setAttribute("aria-label", isOpen ? "Abrir menú" : "Cerrar menú");
      mobileMenu.classList.toggle("hidden", isOpen);
    });
  }

  const themeButton = document.querySelector("[data-theme-toggle]");
  const themeLabel = document.querySelector("[data-theme-label]");
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");

  const getStoredTheme = () => {
    try {
      return localStorage.getItem("soundshop-theme");
    } catch {
      return null;
    }
  };

  const applyTheme = (theme, persist = false) => {
    const activeTheme = theme === "dark" ? "dark" : "light";
    root.dataset.theme = activeTheme;

    if (persist) {
      try {
        localStorage.setItem("soundshop-theme", activeTheme);
      } catch {
        // El tema sigue activo durante la visita aunque el navegador bloquee el almacenamiento.
      }
    }

    const darkModeIsActive = activeTheme === "dark";
    const nextAction = darkModeIsActive ? "Activar modo claro" : "Activar modo oscuro";
    themeButton?.setAttribute("aria-pressed", String(darkModeIsActive));
    themeButton?.setAttribute("aria-label", nextAction);
    if (themeLabel) themeLabel.textContent = nextAction;

    document.querySelector('meta[name="theme-color"]')?.setAttribute(
      "content",
      darkModeIsActive ? "#050b14" : "#0a1323",
    );
  };

  applyTheme(root.dataset.theme || (systemTheme.matches ? "dark" : "light"));

  themeButton?.addEventListener("click", () => {
    applyTheme(root.dataset.theme === "dark" ? "light" : "dark", true);
  });

  systemTheme.addEventListener?.("change", (event) => {
    if (!getStoredTheme()) applyTheme(event.matches ? "dark" : "light");
  });

  document.querySelectorAll("[data-dismiss-message]").forEach((button) => {
    button.addEventListener("click", () => button.closest("[data-message]")?.remove());
  });

  const copyButton = document.querySelector("[data-copy-order]");
  if (copyButton) {
    copyButton.addEventListener("click", async () => {
      const orderCode = copyButton.dataset.copyOrder;
      try {
        await navigator.clipboard.writeText(orderCode);
        copyButton.textContent = "Código copiado";
      } catch {
        copyButton.textContent = orderCode;
      }
    });
  }

  if (!reducedMotion.matches) {
    document.querySelectorAll('.product-card a[href*="/productos/"], .feature-frame a[href*="/productos/"]').forEach((link) => {
      link.addEventListener("click", (event) => {
        if (
          event.defaultPrevented
          || event.button !== 0
          || event.metaKey
          || event.ctrlKey
          || event.shiftKey
          || event.altKey
          || link.target === "_blank"
        ) {
          return;
        }

        const destination = new URL(link.href, window.location.href);
        if (destination.origin !== window.location.origin) return;

        event.preventDefault();
        const productSurface = link.closest(".product-card, .feature-frame");
        productSurface?.classList.add("is-selected");
        productSurface?.setAttribute("aria-busy", "true");
        window.setTimeout(() => window.location.assign(destination.href), 230);
      });
    });
  }

  const progressBar = document.querySelector(".scroll-progress");
  const nativeScrollTimeline = window.CSS?.supports?.("animation-timeline: scroll()") ?? false;

  const updateScrollProgress = () => {
    if (!progressBar || nativeScrollTimeline) return;
    const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = scrollableHeight > 0 ? window.scrollY / scrollableHeight : 0;
    progressBar.style.setProperty("--scroll-progress", String(Math.min(1, Math.max(0, progress))));
  };

  if (!reducedMotion.matches) {
    const revealSelector = [
      ".section-heading",
      ".category-tile",
      ".product-card",
      ".service-note__inner",
      ".account-section__copy",
      ".account-section__form",
      ".account-profile-card",
      ".page-intro__grid",
      ".catalog-layout",
      ".category-row",
      ".product-detail__visual",
      ".product-detail__info",
      ".cart-item",
      ".order-summary",
      ".confirmation-card",
      ".account-page__info",
      ".account-page__form",
      ".account-confirmation__card",
      ".site-footer__grid",
    ].join(",");

    const revealElements = [...document.querySelectorAll(revealSelector)];
    revealElements.forEach((element, index) => {
      element.setAttribute("data-reveal", "");
      element.style.setProperty("--reveal-order", String(index % 4));
    });
    root.classList.add("motion-ready");

    if ("IntersectionObserver" in window) {
      const revealObserver = new IntersectionObserver(
        (entries, observer) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          });
        },
        { rootMargin: "0px 0px -8%", threshold: 0.1 },
      );

      requestAnimationFrame(() => revealElements.forEach((element) => revealObserver.observe(element)));
    } else {
      revealElements.forEach((element) => element.classList.add("is-visible"));
    }
  }

  const parallaxImages = reducedMotion.matches
    ? []
    : [...document.querySelectorAll("[data-parallax]")];
  let visualFrameRequested = false;

  const updateScrollVisuals = () => {
    const viewportHeight = window.innerHeight;
    parallaxImages.forEach((image) => {
      const rect = image.parentElement?.getBoundingClientRect();
      if (!rect || rect.bottom < -100 || rect.top > viewportHeight + 100) return;
      const distanceFromCenter = viewportHeight / 2 - (rect.top + rect.height / 2);
      const normalizedDistance = Math.min(1, Math.max(-1, distanceFromCenter / viewportHeight));
      const maximumOffset = Number.parseFloat(image.dataset.parallax || "24");
      image.style.setProperty("--parallax-y", `${(normalizedDistance * maximumOffset).toFixed(2)}px`);
    });
    updateScrollProgress();
    visualFrameRequested = false;
  };

  const requestVisualUpdate = () => {
    if (visualFrameRequested) return;
    visualFrameRequested = true;
    requestAnimationFrame(updateScrollVisuals);
  };

  window.addEventListener("scroll", requestVisualUpdate, { passive: true });
  window.addEventListener("resize", requestVisualUpdate, { passive: true });
  requestVisualUpdate();

  const precisePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  if (!reducedMotion.matches && precisePointer.matches) {
    document.querySelectorAll("[data-product-tilt]").forEach((visual) => {
      const image = visual.querySelector("img");
      if (!image) return;

      visual.addEventListener("pointermove", (event) => {
        const rect = visual.getBoundingClientRect();
        const horizontal = (event.clientX - rect.left) / rect.width - 0.5;
        const vertical = (event.clientY - rect.top) / rect.height - 0.5;
        image.style.setProperty("--tilt-x", `${(-vertical * 3.2).toFixed(2)}deg`);
        image.style.setProperty("--tilt-y", `${(horizontal * 3.2).toFixed(2)}deg`);
      });

      visual.addEventListener("pointerleave", () => {
        image.style.setProperty("--tilt-x", "0deg");
        image.style.setProperty("--tilt-y", "0deg");
      });
    });
  }
});
