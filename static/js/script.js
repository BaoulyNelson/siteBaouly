  // Blocage du clic droit
  document.addEventListener("contextmenu", function (e) {
    e.preventDefault();
    alert("Contenu protégé par Le Baouly !");
  });

  // Blocage des touches Ctrl+C, Ctrl+S, Ctrl+X
  document.addEventListener("keydown", function (e) {
    if (e.ctrlKey && ["c", "C", "x", "X", "s", "S"].includes(e.key)) {
      e.preventDefault();
      alert("Action interdite : contenu protégé par Le Baouly !");
    }
  });
  