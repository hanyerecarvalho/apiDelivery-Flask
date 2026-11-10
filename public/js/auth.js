// auth.js
export function verificarLogin() {
    const token = localStorage.getItem('jwt');
    if (!token) {
        window.location.href = 'login.html';
    }
    return token;
}