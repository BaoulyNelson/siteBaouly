(function () {
  const searchBtn = document.getElementById("searchBtn");
  const searchPanel = document.getElementById("searchPanel");
  const searchInput = document.getElementById("q");
  const mobileSearchInput = document.getElementById("q_mobile");
  const mobileMenu = document.getElementById("mobileMenu");

  const mdQuery = window.matchMedia("(min-width:768px)");

  function getTopOffset() {
    const topbar = document.querySelector(".topbar");
    const header = document.querySelector("header");

    const topbarH = topbar ? topbar.offsetHeight : 0;
    const headerH = header ? header.offsetHeight : 0;

    return topbarH + headerH; // juste après le header
  }

  function positionSearchPanel() {
    if (!searchPanel) return;
    const top = getTopOffset() + window.scrollY;
    searchPanel.style.top = `${top}px`;
  }

  function openOverlay() {
    positionSearchPanel();
    searchPanel.classList.remove("hidden");
    searchPanel.setAttribute("aria-hidden", "false");
    searchBtn?.setAttribute("aria-expanded", "true");
    setTimeout(() => searchInput?.focus(), 40);
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
    if (!searchPanel.contains(e.target) && !searchBtn.contains(e.target)) {
      if (!searchPanel.classList.contains("hidden")) closeOverlay();
    }
  }

  function handleEsc(e) {
    if (e.key === "Escape" || e.key === "Esc") {
      if (!searchPanel.classList.contains("hidden")) closeOverlay();
    }
  }

  function onSearchClicked(e) {
    e.preventDefault();
    if (mdQuery.matches) {
      if (searchPanel.classList.contains("hidden")) openOverlay();
      else closeOverlay();
    } else {
      if (mobileMenu.classList.contains("-translate-x-full")) {
        mobileMenu.classList.remove("-translate-x-full");
        setTimeout(() => mobileSearchInput?.focus(), 180);
      } else {
        mobileSearchInput?.focus();
      }
    }
  }

  searchBtn?.addEventListener("click", onSearchClicked);

  mdQuery.addEventListener("change", (ev) => {
    if (!ev.matches) {
      if (!searchPanel.classList.contains("hidden")) closeOverlay();
    } else {
      positionSearchPanel();
    }
  });

  if (mdQuery.matches) positionSearchPanel();
})();
