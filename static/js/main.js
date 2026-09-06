document.addEventListener("DOMContentLoaded", () => {
  const root = document.documentElement;
  const systemMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const reducedMotion = { get matches() { return systemMotion.matches || root.dataset.motion === "reduce"; } };

  const menuButton = document.querySelector("[data-menu-button]");
  const mobileMenu = document.querySelector("[data-mobile-menu]");
  const siteHeader = document.querySelector('.site-header');
  if (siteHeader) {
    const syncHeaderHeight = () => root.style.setProperty('--site-header-height', `${siteHeader.offsetHeight}px`);
    syncHeaderHeight();
    new ResizeObserver(syncHeaderHeight).observe(siteHeader);
  }

  if (menuButton && mobileMenu) {
    const pageRegions = [...document.querySelectorAll('.site-main, .site-footer')];
    const closeMenu = () => {
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.setAttribute("aria-label", "Abrir menú");
      mobileMenu.classList.add("hidden");
      document.body.classList.remove("menu-is-open");
      pageRegions.forEach(region => { region.inert = false; });
    };
    menuButton.addEventListener("click", () => {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
      menuButton.setAttribute("aria-label", isOpen ? "Abrir menú" : "Cerrar menú");
      mobileMenu.classList.toggle("hidden", isOpen);
      document.body.classList.toggle("menu-is-open", !isOpen);
      pageRegions.forEach(region => { region.inert = !isOpen; });
      if (!isOpen) document.querySelector('.search-popover')?.removeAttribute('open');
      if (!isOpen) mobileMenu.querySelector('input, a, button')?.focus();
    });
    siteHeader.addEventListener("click", (event) => {
      if (event.target.closest("a")) closeMenu();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Tab" && menuButton.getAttribute("aria-expanded") === "true") {
        const controls = [...siteHeader.querySelectorAll('a, input, button, summary')].filter(control => control.getClientRects().length && !control.disabled);
        const first = controls[0], last = controls[controls.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
      if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
        closeMenu();
        menuButton.focus();
      }
    });
    window.matchMedia('(min-width: 1101px)').addEventListener('change', event => {
      if (event.matches) {
        const restoreFocus = mobileMenu.contains(document.activeElement) || document.activeElement === menuButton;
        closeMenu();
        if (restoreFocus) siteHeader.querySelector('.desktop-nav .is-active, .desktop-nav a')?.focus();
      }
    });
  }

  const searchPopover = document.querySelector('.search-popover');
  if (searchPopover) {
    searchPopover.addEventListener('toggle', () => {
      if (searchPopover.open) searchPopover.querySelector('input')?.focus();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && searchPopover.open) {
        searchPopover.open = false;
        searchPopover.querySelector('summary').focus();
      }
    });
    document.addEventListener('click', event => {
      if (!searchPopover.contains(event.target)) searchPopover.open = false;
    });
  }

  const themeButton = document.querySelector("[data-theme-toggle]");
  const themeLabel = document.querySelector("[data-theme-label]");
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
  let themeTransitionTimer;

  const getStoredTheme = () => {
    try {
      return localStorage.getItem("soundshop-theme");
    } catch {
      return null;
    }
  };

  const applyTheme = (theme, persist = false) => {
    const activeTheme = theme === "dark" ? "dark" : "light";

    if (persist && !reducedMotion.matches) {
      window.clearTimeout(themeTransitionTimer);
      root.classList.add("theme-changing");
      themeTransitionTimer = window.setTimeout(() => root.classList.remove("theme-changing"), 360);
    }

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
      darkModeIsActive ? "#121212" : "#F4F0E8",
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

  const quickViewDialog = document.querySelector("[data-quick-view-dialog]");
  const quickViewBody = document.querySelector("[data-quick-view-body]");
  const miniCartDialog = document.querySelector("[data-mini-cart]");
  const miniCartLines = document.querySelector("[data-mini-cart-lines]");
  const miniCartFooter = document.querySelector("[data-mini-cart-footer]");
  const miniCartTotal = document.querySelector("[data-mini-cart-total]");
  const imageViewer = document.querySelector("[data-image-viewer]");
  const imageViewerImage = document.querySelector("[data-image-viewer-image]");
  const imageViewerCaption = document.querySelector("[data-image-viewer-caption]");
  let quickViewOpener;
  let miniCartOpener;
  let imageViewerOpener;

  const openDialog = (dialog) => {
    if (!dialog || typeof dialog.showModal !== "function") return false;
    if (!dialog.open) dialog.showModal();
    return true;
  };

  const closeDialog = (dialog) => {
    if (dialog?.open) dialog.close();
  };

  const closeOnBackdrop = (dialog) => {
    dialog?.addEventListener("click", (event) => {
      if (event.target === dialog) closeDialog(dialog);
    });
  };

  document.addEventListener("click", (event) => {
    const quickViewButton = event.target.closest("[data-quick-view]");
    if (!quickViewButton) return;

    const productCard = quickViewButton.closest("[data-product-card]");
    const template = productCard?.querySelector("[data-quick-view-template]");
    const detailLink = productCard?.querySelector('.product-card__image[href]');

    if (!quickViewDialog || !quickViewBody || !template) {
      if (detailLink) window.location.assign(detailLink.href);
      return;
    }

    quickViewBody.replaceChildren(template.content.cloneNode(true));
    quickViewOpener = quickViewButton;
    if (!openDialog(quickViewDialog) && detailLink) window.location.assign(detailLink.href);
  });

  document.querySelector("[data-quick-view-close]")?.addEventListener("click", () => closeDialog(quickViewDialog));
  quickViewDialog?.addEventListener("close", () => {
    quickViewBody?.replaceChildren();
    quickViewOpener?.focus();
    quickViewOpener = null;
  });
  closeOnBackdrop(quickViewDialog);

  const createElement = (tagName, className, text) => {
    const element = document.createElement(tagName);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  };

  const renderMiniCart = (lines, total) => {
    if (!miniCartLines) return;
    miniCartLines.replaceChildren();

    if (!Array.isArray(lines) || lines.length === 0) {
      const empty = createElement("div", "mini-cart__empty");
      empty.dataset.miniCartEmpty = "";
      empty.append(
        createElement("span", "", "00"),
        createElement("h3", "", "Aún no has elegido productos."),
        createElement("p", "", "Abre una vista rápida o recorre el catálogo para comenzar."),
      );
      miniCartLines.append(empty);
      miniCartFooter?.classList.add("is-empty");
    } else {
      lines.forEach((line) => {
        const article = createElement("article", "mini-cart__item");
        const imageLink = createElement("a");
        imageLink.href = line.detalle_url;
        const image = createElement("img");
        image.src = line.imagen;
        image.alt = line.nombre;
        imageLink.append(image);

        const information = createElement("div");
        const brand = createElement("p", "", line.marca);
        const title = createElement("h3");
        const productLink = createElement("a", "", line.nombre);
        productLink.href = line.detalle_url;
        title.append(productLink);
        const quantityLabel = `${line.cantidad} ${line.cantidad === 1 ? "unidad" : "unidades"}`;
        information.append(brand, title, createElement("span", "", quantityLabel));

        article.append(imageLink, information, createElement("strong", "", line.subtotal_formateado));
        miniCartLines.append(article);
      });
      miniCartFooter?.classList.remove("is-empty");
    }

    if (miniCartTotal) miniCartTotal.textContent = total;
  };

  const openMiniCart = (opener) => {
    miniCartOpener = opener || document.activeElement;
    return openDialog(miniCartDialog);
  };

  document.querySelectorAll("[data-cart-toggle]").forEach((link) => {
    link.addEventListener("click", (event) => {
      if (
        event.defaultPrevented
        || event.button !== 0
        || event.metaKey
        || event.ctrlKey
        || event.shiftKey
        || event.altKey
      ) {
        return;
      }
      if (openMiniCart(link)) event.preventDefault();
    });
  });

  document.querySelector("[data-mini-cart-close]")?.addEventListener("click", () => closeDialog(miniCartDialog));
  miniCartDialog?.addEventListener("close", () => {
    miniCartOpener?.focus?.();
    miniCartOpener = null;
  });
  closeOnBackdrop(miniCartDialog);

  const cartToast = document.querySelector("[data-cart-toast]");
  const cartToastImage = document.querySelector("[data-cart-toast-image]");
  const cartToastLabel = document.querySelector("[data-cart-toast-label]");
  const cartToastName = document.querySelector("[data-cart-toast-name]");
  const cartToastMeta = document.querySelector("[data-cart-toast-meta]");
  const cartToastAction = document.querySelector("[data-cart-toast-cart]");
  let cartToastTimer;

  const hideCartToast = () => {
    if (!cartToast) return;
    cartToast.classList.remove("is-visible");
    cartToast.setAttribute("aria-hidden", "true");
    window.clearTimeout(cartToastTimer);
  };

  const showCartToast = (data, isError = false) => {
    if (!cartToast || !cartToastName || !cartToastMeta || !cartToastLabel || !cartToastImage) return;
    const product = data.producto_agregado;
    const requiresSession = Boolean(data.requiere_sesion);

    cartToast.classList.toggle("is-error", isError);
    cartToast.classList.toggle("is-auth-required", requiresSession);
    cartToastLabel.textContent = requiresSession
      ? "Inicio de sesión requerido"
      : isError
        ? "No se pudo agregar"
        : "Agregado al carrito";
    cartToastName.textContent = isError ? data.mensaje : product?.nombre || "Producto agregado";
    cartToastMeta.textContent = requiresSession
      ? "Activa tu cuenta y vuelve al producto para continuar."
      : isError
        ? "Revisa la cantidad e inténtalo nuevamente."
      : `${product?.cantidad_en_carrito || 0} en el carrito · ${product?.subtotal_formateado || data.total_formateado}`;
    cartToastImage.hidden = isError || !product?.imagen;
    if (!cartToastImage.hidden) {
      cartToastImage.src = product.imagen;
      cartToastImage.alt = product.nombre;
    }

    if (cartToastAction) {
      cartToastAction.hidden = isError && !requiresSession;
      cartToastAction.textContent = requiresSession ? "Iniciar sesión" : "Ver carrito";
      if (requiresSession) {
        cartToastAction.dataset.destination = data.registro_url || "/registro/";
      } else {
        delete cartToastAction.dataset.destination;
      }
    }

    cartToast.classList.remove("is-visible");
    void cartToast.offsetWidth;
    cartToast.classList.add("is-visible");
    cartToast.setAttribute("aria-hidden", "false");
    window.clearTimeout(cartToastTimer);
    cartToastTimer = window.setTimeout(hideCartToast, isError ? 5600 : 4600);
  };

  document.querySelector("[data-cart-toast-close]")?.addEventListener("click", hideCartToast);
  cartToastAction?.addEventListener("click", (event) => {
    const destination = event.currentTarget.dataset.destination;
    hideCartToast();
    if (destination) {
      window.location.assign(destination);
      return;
    }
    openMiniCart(event.currentTarget);
  });

  const updateCartUi = (data) => {
    document.querySelectorAll("[data-cart-count]").forEach((counter) => {
      counter.textContent = data.cantidad;
      counter.classList.toggle("hidden", data.cantidad === 0);
    });
    document.querySelectorAll("[data-cart-toggle]").forEach((link) => {
      link.setAttribute("aria-label", `Carrito con ${data.cantidad} productos`);
    });
    renderMiniCart(data.lineas, data.total_formateado);
  };

  document.addEventListener("submit", async (event) => {
    const form = event.target.closest("[data-ajax-cart]");
    if (!form || typeof window.fetch !== "function") return;
    event.preventDefault();

    const submitButton = event.submitter || form.querySelector('button[type="submit"]');
    const previousLabel = submitButton?.innerHTML;
    form.setAttribute("aria-busy", "true");
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Agregando…";
    }

    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "X-Requested-With": "XMLHttpRequest",
        },
      });
      const data = await response.json();

      if (!response.ok || !data.ok) {
        showCartToast(data, true);
        return;
      }

      updateCartUi(data);
      closeDialog(quickViewDialog);
      showCartToast(data);
    } catch {
      showCartToast({ mensaje: "No fue posible conectar con la tienda." }, true);
    } finally {
      form.removeAttribute("aria-busy");
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.innerHTML = previousLabel;
      }
    }
  });

  document.addEventListener("click", (event) => {
    const imageButton = event.target.closest("[data-image-viewer-open]");
    if (!imageButton || !imageViewer || !imageViewerImage || !imageViewerCaption) return;
    imageViewerOpener = imageButton;
    imageViewerImage.src = imageButton.dataset.image;
    imageViewerImage.alt = imageButton.dataset.caption;
    imageViewerCaption.textContent = imageButton.dataset.caption;
    openDialog(imageViewer);
  });

  document.querySelector("[data-image-viewer-close]")?.addEventListener("click", () => closeDialog(imageViewer));
  imageViewer?.addEventListener("close", () => {
    imageViewerImage?.removeAttribute("src");
    imageViewerOpener?.focus();
    imageViewerOpener = null;
  });
  closeOnBackdrop(imageViewer);

  // La entrada de cada página se resuelve en CSS. Los enlaces siguen
  // siendo nativos: no se retrasa la navegación ni se interceptan modificadores.

  const progressBar = document.querySelector(".scroll-progress");
  const scrollCue = document.querySelector("[data-scroll-cue]");

  const updateScrollProgress = () => {
    if (!progressBar) return;
    const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = scrollableHeight > 0 ? window.scrollY / scrollableHeight : 0;
    progressBar.style.setProperty("--scroll-progress", String(Math.min(1, Math.max(0, progress))));
  };

  if (!reducedMotion.matches) {
    const revealSelector = [
      "[data-reveal]",
      ".section-heading",
      ".category-tile",
      ".editorial-card",
      ".about-section__visual",
      ".about-section__copy",
      ".product-card",
      ".service-note__inner",
      ".account-section__copy",
      ".account-section__form",
      ".account-entry-card",
      ".account-profile-card",
      ".page-intro__grid",
      ".filter-desktop",
      ".catalog-toolbar",
      ".collection-guide__heading",
      ".collection-guide__item",
      ".about-composition",
      ".about-story",
      ".about-beliefs__heading",
      ".about-beliefs__list article",
      ".about-outro",
      ".category-help__inner",
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

  const parallaxImages = [...document.querySelectorAll("[data-parallax]")];
  const scrollScenes = [...document.querySelectorAll("[data-scroll-scene]")];
  let visualFrameRequested = false;
  const heroImage = document.querySelector(".home-hero__image img");
  const desktopMotion = window.matchMedia("(hover: hover) and (min-width: 761px)");

  const updateScrollVisuals = () => {
    const viewportHeight = window.innerHeight;
    if (heroImage) {
      const offset = !reducedMotion.matches && desktopMotion.matches ? Math.min(window.scrollY * 0.045, 14) : 0;
      heroImage.style.setProperty("--hero-y", `${offset}px`);
    }
    parallaxImages.forEach((image) => {
      if (reducedMotion.matches) {
        image.style.setProperty("--parallax-y", "0px");
        return;
      }
      const rect = image.parentElement?.getBoundingClientRect();
      if (!rect || rect.bottom < -100 || rect.top > viewportHeight + 100) return;
      const distanceFromCenter = viewportHeight / 2 - (rect.top + rect.height / 2);
      const normalizedDistance = Math.min(1, Math.max(-1, distanceFromCenter / viewportHeight));
      const maximumOffset = Number.parseFloat(image.dataset.parallax || "24");
      image.style.setProperty("--parallax-y", `${(normalizedDistance * maximumOffset).toFixed(2)}px`);
    });
    scrollScenes.forEach((scene) => {
      const rect = scene.getBoundingClientRect();
      if (!reducedMotion.matches && (rect.bottom < 0 || rect.top > viewportHeight)) return;
      const progress = Math.min(1, Math.max(0, (viewportHeight - rect.top) / (viewportHeight + rect.height)));
      const shift = reducedMotion.matches ? 0 : (progress - .5) * 36;
      scene.style.setProperty("--scene-y", `${shift.toFixed(2)}px`);
      scene.style.setProperty("--scene-turn", `${(shift * .35).toFixed(2)}deg`);
      scene.style.setProperty("--scene-progress", reducedMotion.matches ? "0" : progress.toFixed(3));
    });
    scrollCue?.classList.toggle("is-hidden", window.scrollY > 80);
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
  if (precisePointer.matches) {
    document.querySelectorAll("[data-product-tilt]").forEach((visual) => {
      const image = visual.querySelector("img");
      if (!image) return;

      visual.addEventListener("pointermove", (event) => {
        if (reducedMotion.matches) return;
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

  document.querySelectorAll("[data-motion-surface]").forEach((surface) => {
    let frame;
    let latestPointer;
    const reset = () => {
      cancelAnimationFrame(frame);
      surface.style.removeProperty("--pointer-shift-x");
      surface.style.removeProperty("--pointer-rotate");
      surface.style.removeProperty("--pointer-x");
      surface.style.removeProperty("--pointer-y");
      frame = null;
    };
    surface.addEventListener("pointermove", (event) => {
      if (reducedMotion.matches || !precisePointer.matches || event.pointerType === "touch") return;
      latestPointer = { x: event.clientX, y: event.clientY };
      if (frame) return;
      frame = requestAnimationFrame(() => {
        const rect = surface.getBoundingClientRect();
        const x = Math.min(1, Math.max(0, (latestPointer.x - rect.left) / rect.width));
        const y = Math.min(1, Math.max(0, (latestPointer.y - rect.top) / rect.height));
        surface.style.setProperty("--pointer-x", `${(x * 100).toFixed(1)}%`);
        surface.style.setProperty("--pointer-y", `${(y * 100).toFixed(1)}%`);
        surface.style.setProperty("--pointer-shift-x", `${((x - .5) * 8).toFixed(2)}px`);
        surface.style.setProperty("--pointer-rotate", `${((x - .5) * 1.6).toFixed(2)}deg`);
        frame = null;
      });
    }, { passive: true });
    surface.addEventListener("pointerleave", reset);
    surface.addEventListener("pointercancel", reset);
  });

  const motionButton = document.querySelector("[data-motion-toggle]");
  const motionLabel = document.querySelector("[data-motion-label]");
  const applyMotionPreference = () => {
    let saved = "";
    try { saved = localStorage.getItem("soundshop-motion"); } catch { /* Preferencia solo durante la visita. */ }
    root.dataset.motion = systemMotion.matches || saved === "reduce" ? "reduce" : "full";
    if (motionButton) {
      motionButton.hidden = false;
      motionButton.disabled = systemMotion.matches;
      motionButton.setAttribute("aria-pressed", String(reducedMotion.matches));
    }
    if (motionLabel) motionLabel.textContent = systemMotion.matches
      ? "Movimiento reducido por el sistema"
      : reducedMotion.matches ? "Activar movimiento" : "Reducir movimiento";
    requestVisualUpdate();
  };
  motionButton?.addEventListener("click", () => {
    const next = reducedMotion.matches ? "full" : "reduce";
    try { localStorage.setItem("soundshop-motion", next); } catch {
      root.dataset.motion = next;
      motionButton.setAttribute("aria-pressed", String(next === "reduce"));
      if (motionLabel) motionLabel.textContent = next === "reduce" ? "Activar movimiento" : "Reducir movimiento";
      requestVisualUpdate();
      return;
    }
    applyMotionPreference();
  });
  systemMotion.addEventListener("change", applyMotionPreference);
  applyMotionPreference();
});
