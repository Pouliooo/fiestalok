document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu toggle
  const toggle = document.querySelector('.navbar__toggle');
  const navLinks = document.querySelector('.navbar__links');

  toggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('navbar__links--open');
    toggle.setAttribute('aria-expanded', isOpen);
    toggle.textContent = isOpen ? '✕' : '☰';
  });

  // Close menu on link click
  navLinks.querySelectorAll('.navbar__link').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('navbar__links--open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = '☰';
    });
  });

  // Active link highlight on scroll
  const sections = document.querySelectorAll('section[id]');
  const navItems = document.querySelectorAll('.navbar__link');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY + 100;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollY >= top && scrollY < top + height) {
        navItems.forEach(item => {
          item.classList.remove('navbar__link--active');
          if (item.getAttribute('href') === '#' + id) {
            item.classList.add('navbar__link--active');
          }
        });
      }
    });
  });

  // Form submission
  const form = document.getElementById('contact-form');

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    // Validate required fields
    if (!data.name || !data.email || !data['event-type'] || !data.date) {
      alert('Remplis tous les champs obligatoires stp ! 🙏');
      return;
    }

    // Sanitize name for display
    const safeName = data.name.replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // For now, show success message (replace with actual API call later)
    form.innerHTML = '<div style="text-align: center; padding: 3rem 1rem;">' +
      '<div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>' +
      '<h3 style="font-family: var(--font-display); font-size: 1.5rem; letter-spacing: 1px; margin-bottom: 1rem;">' +
      'DEMANDE ENVOYÉE !' +
      '</h3>' +
      '<p style="color: var(--color-text-light);">' +
      'Merci ' + safeName + ' ! On te recontacte en moins d\'1h.<br>' +
      'Prépare-toi, ta fiesta arrive bientôt ! 🚀' +
      '</p>' +
      '</div>';
  });
});
