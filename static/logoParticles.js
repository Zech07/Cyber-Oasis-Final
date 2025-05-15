document.addEventListener('DOMContentLoaded', () => {
    const logo = document.getElementById('logo-glow');
    if (!logo) return;

    logo.addEventListener('mouseenter', (e) => {
        for (let i = 0; i < 30; i++) {
            createParticle(e, logo);
        }
    });
});

function createParticle(e, logo) {
    const particle = document.createElement('span');
    particle.classList.add('gold-particle');

    const size = Math.random() * 6 + 4;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;

    // Center of logo element using bounding rect
    const rect = logo.getBoundingClientRect();
    particle.style.left = `${rect.left + rect.width / 2}px`;
    particle.style.top = `${rect.top + rect.height / 2}px`;

    document.body.appendChild(particle);

    const randX = Math.random() * 2 - 1;
    const randY = Math.random() * 2 - 1;
    particle.animate([
        { transform: 'translate(0,0) scale(1)', opacity: 1 },
        { transform: `translate(${randX * 60}px, ${randY * 60}px) scale(0.5)`, opacity: 0 }
    ], {
        duration: 1000,
        easing: 'ease-out',
        fill: 'forwards'
    });

    setTimeout(() => {
        particle.remove();
    }, 1000);
}
