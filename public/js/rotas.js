// exemplo: produtos.js
import ApiService from './ApiService.js';
import { verificarLogin } from './auth.js';

const token = verificarLogin();
const api = new ApiService(token);

// agora é só usar:
const produtos = await api.get('api/produto/listar.php');
const novo = await api.post('api/produto/cadastrar.php', { nome, preco });
const atualizado = await api.put('api/produto/editar.php', id, { nome, preco });
await api.delete('api/produto/excluir.php', id);