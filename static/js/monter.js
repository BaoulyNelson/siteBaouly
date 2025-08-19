  const backToTop = document.getElementById("backToTop");

  // Afficher / cacher quand on scrolle
  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
      backToTop.classList.remove("hidden");
    } else {
      backToTop.classList.add("hidden");
    }
  });

  // Cliquer = scroll en haut
  backToTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
