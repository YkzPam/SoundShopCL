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
  const scrollCue = document.querySelector("[data-scroll-cue]");
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
      ".editorial-card",
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
