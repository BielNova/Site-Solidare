const container = document.querySelector('.container');
const cadastroBtn = document.querySelector('.registro-btn');
const loginBtn = document.querySelector('.login-btn');

cadastroBtn.addEventListener('click', () => {
    container.classList.add('active');
});
loginBtn.addEventListener('click', () => {
    container.classList.remove('active');
});
