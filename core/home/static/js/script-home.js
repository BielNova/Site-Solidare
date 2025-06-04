document.addEventListener("DOMContentLoaded", () => {
    // Fade-in para a seção de boas-vindas
    const welcomeSection = document.querySelector(".welcome-section");
    welcomeSection.style.opacity = "0";
    setTimeout(() => {
        welcomeSection.style.transition = "opacity 1.5s ease-in-out";
        welcomeSection.style.opacity = "1";
    }, 200);

    // Efeito de pulsação no botão "Saiba Mais"
    const saibaMaisButton = document.querySelector(".welcome-section button");
    saibaMaisButton.addEventListener("mouseover", () => {
        saibaMaisButton.style.animation = "pulse 0.5s infinite";
    });
    saibaMaisButton.addEventListener("mouseout", () => {
        saibaMaisButton.style.animation = "";
    });

    // Transição suave para o menu hamburguer
    const menuToggle = document.getElementById("menu-toggle");
    const navLinks = document.querySelector(".nav-links");
    const authLinks = document.querySelector(".auth-links");
    menuToggle.addEventListener("change", () => {
        if (menuToggle.checked) {
            navLinks.style.transition = "opacity 0.3s ease, transform 0.3s ease";
            navLinks.style.opacity = "1";
            navLinks.style.transform = "translateY(0)";
            authLinks.style.transition = "opacity 0.3s ease, transform 0.3s ease";
            authLinks.style.opacity = "1";
            authLinks.style.transform = "translateY(0)";
        } else {
            navLinks.style.transition = "opacity 0.3s ease, transform 0.3s ease";
            navLinks.style.opacity = "0";
            navLinks.style.transform = "translateY(-10px)";
            authLinks.style.transition = "opacity 0.3s ease, transform 0.3s ease";
            authLinks.style.opacity = "0";
            authLinks.style.transform = "translateY(-10px)";
        }
    });

    // Efeito de mudança de cor da navbar ao rolar
    const navbar = document.querySelector(".navbar");
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            navbar.style.backgroundColor = "#ffb129";
            navbar.style.transition = "background-color 0.5s ease";
        } else {
            navbar.style.backgroundColor = "#1a1a1a";
            navbar.style.transition = "background-color 0.5s ease";
        }
    });
});