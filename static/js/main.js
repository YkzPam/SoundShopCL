document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.querySelector("[data-menu-button]");
  const mobileMenu = document.querySelector("[data-mobile-menu]");

  if (menuButton && mobileMenu) {
    menuButton.addEventListener("click", () => {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
      mobileMenu.classList.toggle("hidden", isOpen);
    });
  }

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
});
