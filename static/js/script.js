(function () {
  // Blocage du clic droit
  // document.addEventListener("contextmenu", function (e) {
  //   e.preventDefault();
  //   alert("Contenu protégé par Le Baouly !");
  // });

  // Blocage des touches Ctrl+C, Ctrl+S, Ctrl+X
  document.addEventListener("keydown", function (e) {
    if (e.ctrlKey && ["c", "C", "x", "X", "s", "S"].includes(e.key)) {
      e.preventDefault();
      alert("Action interdite : contenu protégé par Le Baouly !");
    }
  });
  const menuBtn = document.getElementById("menuBtn");
  const menuCloseBtn = document.getElementById("menuCloseBtn");
  const mobileMenu = document.getElementById("mobileMenu");
  const menuOverlay = document.getElementById("menuOverlay");

  const searchBtn = document.getElementById("searchBtn");
  const searchPanel = document.getElementById("searchPanel");
  const searchInput = document.getElementById("q");
  const mobileSearchInput = document.getElementById("q_mobile");

  // Tailwind "md" breakpoint ~ 768px
  const mdQuery = window.matchMedia("(min-width:768px)");

  function getTopOffset() {
    const topbar = document.querySelector(".topbar");
    const header = document.querySelector("header.mainnav");
    const topbarH = topbar ? topbar.offsetHeight : 0;
    const headerH = header ? header.offsetHeight : 0;
    return topbarH + headerH;
  }

  function positionSearchPanel() {
    if (!searchPanel) return;
    const top = getTopOffset() + 8 + window.scrollY;
    searchPanel.style.top = `${top}px`;
  }

  // OVERLAY (desktop)
  function openOverlay() {
    positionSearchPanel();
    searchPanel.classList.remove("hidden");
    searchPanel.setAttribute("aria-hidden", "false");
    searchBtn?.setAttribute("aria-expanded", "true");
    setTimeout(() => (searchInput ? searchInput.focus() : null), 40);
    document.addEventListener("keydown", handleEsc);
    document.addEventListener("click", handleOutsideClick);
    window.addEventListener("resize", positionSearchPanel);
    window.addEventListener("scroll", positionSearchPanel, { passive: true });
  }

  function closeOverlay() {
    searchPanel.classList.add("hidden");
    searchPanel.setAttribute("aria-hidden", "true");
    searchBtn?.setAttribute("aria-expanded", "false");
    document.removeEventListener("keydown", handleEsc);
    document.removeEventListener("click", handleOutsideClick);
    window.removeEventListener("resize", positionSearchPanel);
    window.removeEventListener("scroll", positionSearchPanel);
    searchBtn?.focus();
  }

  function handleOutsideClick(e) {
    if (!searchPanel || !searchBtn) return;
    const target = e.target;
    if (!searchPanel.contains(target) && !searchBtn.contains(target)) {
      if (!searchPanel.classList.contains("hidden")) closeOverlay();
    }
  }

  function handleEsc(e) {
    if (e.key === "Escape" || e.key === "Esc") {
      if (!searchPanel.classList.contains("hidden")) closeOverlay();
      if (!mobileMenu.classList.contains("-translate-x-full")) closeMenu();
    }
  }

  // MOBILE MENU
  function openMenu() {
    mobileMenu.classList.remove("-translate-x-full");
    mobileMenu.setAttribute("aria-hidden", "false");
    menuOverlay.classList.remove("opacity-0", "pointer-events-none");
    menuOverlay.classList.add("opacity-100");
    menuBtn?.setAttribute("aria-expanded", "true");
    setTimeout(() => {
      (mobileSearchInput && mobileSearchInput.focus()) ||
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

  // Unified search button behaviour
  function onSearchClicked(e) {
    e.preventDefault();
    if (mdQuery.matches) {
      if (searchPanel.classList.contains("hidden")) openOverlay();
      else closeOverlay();
    } else {
      if (mobileMenu.classList.contains("-translate-x-full")) {
        openMenu();
        setTimeout(
          () => (mobileSearchInput ? mobileSearchInput.focus() : null),
          180
        );
      } else {
        mobileSearchInput ? mobileSearchInput.focus() : closeMenu();
      }
    }
  }

  // Event wiring
  menuBtn?.addEventListener("click", openMenu);
  menuCloseBtn?.addEventListener("click", closeMenu);
  menuOverlay?.addEventListener("click", closeMenu);

  searchBtn?.addEventListener("click", onSearchClicked);

  // Close overlay when switching to mobile
  mdQuery.addEventListener("change", (ev) => {
    if (!ev.matches) {
      if (!searchPanel.classList.contains("hidden")) closeOverlay();
    } else {
      positionSearchPanel();
    }
  });

  // init
  if (mdQuery.matches) positionSearchPanel();

  // small safety: close search/menu on navigation clicks inside mobileMenu
  mobileMenu
    .querySelectorAll("a")
    .forEach((a) => a.addEventListener("click", closeMenu));
})();




