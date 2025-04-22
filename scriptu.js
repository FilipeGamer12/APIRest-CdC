const listaUsuarios = document.getElementById('lista-usuarios');

fetch('http://127.0.0.1:5000/usuarios')
  .then(response => response.json())
  .then(usuarios => {
    usuarios.forEach(usuario => {
      const itemUsuario = document.createElement('li');
      itemUsuario.innerHTML = `${usuario.nome} - ${usuario.email} - ${usuario.telefone} - Administrador: ${usuario.administrador ? 'Sim' : 'Não'}`;
      listaUsuarios.appendChild(itemUsuario);
    });
  })
  .catch(error => {
    console.error('Erro ao buscar usuários:', error);
    alert('Falha ao carregar a lista de usuários.');
  });