(function () {
  const menuBtn = document.getElementById("menuBtn");
  const menuCloseBtn = document.getElementById("menuCloseBtn");
  const mobileMenu = document.getElementById("mobileMenu");
  const menuOverlay = document.getElementById("menuOverlay");

  function openMenu() {
    mobileMenu.classList.remove("-translate-x-full");
    mobileMenu.setAttribute("aria-hidden", "false");
    menuOverlay.classList.remove("opacity-0", "pointer-events-none");
    menuOverlay.classList.add("opacity-100");
    menuBtn?.setAttribute("aria-expanded", "true");
    setTimeout(() => {
      mobileMenu.querySelector("a")?.focus();
    }, 150);
    document.addEventListener("keydown", trapTabInMenu);
  }

  function closeMenu() {
    mobileMenu.classList.add("-translate-x-full");
    mobileMenu.setAttribute("aria-hidden", "true");
    menuOverlay.classList.add("opacity-0", "pointer-events-none");
    menuOverlay.classList.remove("opacity-100");
    menuBtn?.setAttribute("aria-expanded", "false");
    menuBtn?.focus();
    document.removeEventListener("keydown", trapTabInMenu);
  }

  function trapTabInMenu(e) {
    if (e.key !== "Tab") return;
    const focusable = mobileMenu.querySelectorAll(
      'a,button,input,select,textarea,[tabindex]:not([tabindex="-1"])'
    );
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  menuBtn?.addEventListener("click", openMenu);
  menuCloseBtn?.addEventListener("click", closeMenu);
  menuOverlay?.addEventListener("click", closeMenu);

  // Close menu when a link inside is clicked
  mobileMenu
    .querySelectorAll("a")
    .forEach((a) => a.addEventListener("click", closeMenu));
})();
