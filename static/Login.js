// login.js
import ApiService from './ApiService.js';

const api = new ApiService(); 

document.getElementById('formLogin').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    const data = await api.post('/api/v1/funcionarios/login', { email, senha });

    if (data && data.success) {
        localStorage.setItem('jwt', data.data.token);
        window.location.href = 'dashboard.html';
    } else {
        alert(data?.erro || 'Login inválido');
    }
});