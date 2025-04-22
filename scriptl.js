const listaProdutos = document.getElementById('lista-produtos');

fetch('http://127.0.0.1:5000/produtos')
  .then(response => {
    console.log('Resposta da API:', response); // Exibe a resposta completa no console
    return response.json();
  })
  .then(produtos => {
    produtos.forEach(produto => {
      const itemProduto = document.createElement('li');
      itemProduto.innerHTML = `${produto.nome} - R$ ${produto.preco.toFixed(2)}`;
      listaProdutos.appendChild(itemProduto);
    });
  })
  .catch(error => {
    console.error('Erro na requisição:', error);
    alert('Falha ao se conectar com a API.');
  });