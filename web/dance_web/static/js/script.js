document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.toggle-description');
    
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const description = this.closest('.event-details').querySelector('.description');
            if (description.style.height === '40px' || !description.style.height) {
                description.style.height = description.scrollHeight + 'px';
                this.textContent = '↑';
            } else {
                description.style.height = '40px';
                this.textContent = '↓';
            }
        });
    });
});

function toggleMenu() {
    const menu = document.getElementById("menu");
    menu.classList.toggle("show");
}

// JavaScript to handle scroll-sensitive menu
let lastScrollTop = 0;
const header = document.getElementById('header');
const isHomepage = window.location.pathname === '/'

window.addEventListener('scroll', () => {
    const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (currentScrollTop > lastScrollTop) {
        // Scrolling down - hide menu
        header.classList.add('hidden');
    } else {
        // Scrolling up - show menu
        header.classList.remove('hidden');
    }

    lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop; // For mobile or negative scrolling

    if (isHomepage) {
        if (window.scrollY > 200) {
            header.classList.add('solid');
        } else {
            header.classList.remove('solid');
        }
    }
});

