      (function() {
        // elements
        const menuBtn = document.getElementById('menuBtn');
        const menuCloseBtn = document.getElementById('menuCloseBtn');
        const mobileMenu = document.getElementById('mobileMenu');
        const menuOverlay = document.getElementById('menuOverlay');
        const searchBtn = document.getElementById('searchBtn');
        const searchPanel = document.getElementById('searchPanel');
        const searchInput = document.getElementById('q');
        // utility open/close for mobile menu
        function openMenu() {
          mobileMenu.classList.remove('-translate-x-full');
          mobileMenu.setAttribute('aria-hidden', 'false');
          menuOverlay.classList.remove('opacity-0', 'pointer-events-none');
          menuOverlay.classList.add('opacity-100');
          menuBtn?.setAttribute('aria-expanded', 'true');
          // trap focus simply: focus first link in menu
          setTimeout(() => mobileMenu.querySelector('a')?.focus(), 150);
        }

        function closeMenu() {
          mobileMenu.classList.add('-translate-x-full');
          mobileMenu.setAttribute('aria-hidden', 'true');
          menuOverlay.classList.add('opacity-0', 'pointer-events-none');
          menuOverlay.classList.remove('opacity-100');
          menuBtn?.setAttribute('aria-expanded', 'false');
          menuBtn?.focus();
        }
        // search toggle
        function toggleSearch() {
          const isHidden = searchPanel.classList.contains('hidden');
          if (isHidden) {
            searchPanel.classList.remove('hidden');
            searchBtn.setAttribute('aria-expanded', 'true');
            // autofocus champ recherche
            setTimeout(() => searchInput?.focus(), 50);
          } else {
            searchPanel.classList.add('hidden');
            searchBtn.setAttribute('aria-expanded', 'false');
            searchBtn.focus();
          }
        }
        // events menu
        menuBtn?.addEventListener('click', (e) => {
          openMenu();
        });
        menuCloseBtn?.addEventListener('click', (e) => {
          closeMenu();
        });
        menuOverlay?.addEventListener('click', (e) => {
          closeMenu();
        });
        // keyboard ESC to close
        document.addEventListener('keydown', (e) => {
          if (e.key === 'Escape') {
            // close both
            if (!mobileMenu.classList.contains('-translate-x-full')) closeMenu();
            if (!searchPanel.classList.contains('hidden')) {
              searchPanel.classList.add('hidden');
              searchBtn?.setAttribute('aria-expanded', 'false');
            }
          }
        });
        // events search
        searchBtn?.addEventListener('click', (e) => {
          e.preventDefault();
          toggleSearch();
        });
        // optional: close search if click outside (desktop)
        document.addEventListener('click', (e) => {
          if (!searchPanel || !searchBtn) return;
          const target = e.target;
          if (!searchPanel.contains(target) && !searchBtn.contains(target)) {
            if (!searchPanel.classList.contains('hidden')) {
              searchPanel.classList.add('hidden');
              searchBtn.setAttribute('aria-expanded', 'false');
            }
          }
        });
      })();