document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    // Chamar a API para fazer a autenticação
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email, senha: senha })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.usuario.administrador) {
                // Redirecionar para a página de administração
                window.location.href = 'admin.html'; // Você pode criar uma página admin.html
            } else {
                // Redirecionar para a página de compra
                window.location.href = 'compra.html'; // Você pode criar uma página de compra
            }
        } else {
            // Exibir mensagem de erro
            document.getElementById('error-message').innerText = 'Email ou senha inválidos';
        }
    })
    .catch(error => {
        console.error('Erro de login:', error);
        document.getElementById('error-message').innerText = 'Erro ao tentar fazer login';
    });
});