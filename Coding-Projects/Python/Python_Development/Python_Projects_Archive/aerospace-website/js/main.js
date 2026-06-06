console.log('Astra Dynamics Systems Online');

// Simple parallax effect for the planet
document.addEventListener('mousemove', (e) => {
    const planet = document.querySelector('.planet');
    if (planet) {
        const x = (window.innerWidth - e.pageX * 2) / 100;
        const y = (window.innerHeight - e.pageY * 2) / 100;
        planet.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
    }
});


// Scroll Animation Observer
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

document.querySelectorAll('.reveal').forEach((element) => {
    observer.observe(element);
});

// Rocket Scroll Animation
const rocket = document.getElementById('scroll-rocket');
const specsSection = document.getElementById('specs');
const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

window.addEventListener('scroll', () => {
    if (!rocket) return;

    const scrollY = window.scrollY;
    const scrollProgress = Math.min(scrollY / maxScroll, 1);

    // Activate flame when scrolling
    if (scrollY > 100) {
        rocket.classList.add('active');
    } else {
        rocket.classList.remove('active');
    }

    // Calculate position
    // Start from bottom (-100px) and go up to center of screen or specific point
    // Let's make it rise from bottom to about 80% up the screen as you scroll
    const windowHeight = window.innerHeight;
    const targetY = windowHeight * 0.8 * scrollProgress;

    // Calculate rotation
    // Spin as it rises. 
    const rotation = scrollY * 0.2; // Adjust speed of rotation

    // Apply styles
    // We use 'bottom' for vertical position and transform for rotation
    // Actually, let's use transform for everything for better performance
    // Initial position is fixed at bottom: 20px, left: 50%

    // Let's keep it simple:
    // It stays fixed at the bottom initially.
    // As you scroll, it moves UP the screen.

    const bottomPos = -100 + (windowHeight + 100) * scrollProgress;

    // Check if we reached the specs section
    if (specsSection) {
        const specsRect = specsSection.getBoundingClientRect();
        if (specsRect.top < windowHeight / 2) {
            // Rocket has arrived at specs
            // Maybe lock it there or do a landing animation?
            // For now, let's just let it fly past or stay
        }
    }

    // Update rocket style
    // We want it to rise up.
    // Let's map scroll progress to bottom position from -100px to 50% of screen
    // But user wants it to "rise when scrolling"

    const riseAmount = Math.min(scrollProgress * 100, 80); // Rise up to 80% of viewport height

    rocket.style.bottom = `${riseAmount}%`;
    rocket.style.transform = `translateX(-50%) rotate(${rotation}deg)`;
});

