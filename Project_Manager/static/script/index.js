
document.addEventListener('DOMContentLoaded', function() {
    const menuOpen = document.getElementById('menu-open');
    const menuClose = document.getElementById('menu-close');
    const mobileMenu = document.getElementById('mobile-menu');
    
    menuOpen.addEventListener('click', function() {
      mobileMenu.classList.remove('hidden');
    });
    
    menuClose.addEventListener('click', function() {
      mobileMenu.classList.add('hidden');
    });
});