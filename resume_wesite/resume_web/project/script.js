document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const headerOffset = document.querySelector('header').offsetHeight; // Get header height
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Optional: Add active class to nav links on scroll
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-links li a');

    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.7 // Adjust as needed, percentage of section visible
    };

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href').includes(entry.target.id)) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        sectionObserver.observe(section);
    });

    // Special handling for the 'hero' section which might not always meet threshold
    window.addEventListener('scroll', () => {
        const heroSection = document.getElementById('hero');
        const firstNavLink = document.querySelector('.nav-links li a[href="#hero"]');
        if (heroSection && firstNavLink) {
            const heroRect = heroSection.getBoundingClientRect();
            // If hero section is mostly visible at the top
            if (heroRect.top <= 0 && heroRect.bottom >= window.innerHeight * 0.5) {
                navLinks.forEach(link => link.classList.remove('active'));
                firstNavLink.classList.add('active');
            } else if (window.scrollY === 0) { // At the very top of the page
                navLinks.forEach(link => link.classList.remove('active'));
                firstNavLink.classList.add('active');
            }
        }
    });

    // Initialize active state for the first section on load
    if (document.querySelector('.nav-links li a[href="#hero"]')) {
         document.querySelector('.nav-links li a[href="#hero"]').classList.add('active');
    }
});