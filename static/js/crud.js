import ApiService from "../ApiService.js";
import { verificarLogin } from "./auth.js";

export default async function iniciarCrud(recurso, entidade, campoId, campos) {
    const token = verificarLogin();
    if (!token) return;

    const api = new ApiService(token);
    const rota = "/api/v1/" + recurso;
    const formulario = document.getElementById("formCrud");
    const tabela = document.getElementById("registros");
    const filtro = document.getElementById("filtro");
    const mensagem = document.getElementById("mensagem");
    const salvar = document.getElementById("salvar");
    const cancelar = document.getElementById("cancelar");
    const modo = document.getElementById("modo");
    let registros = [];
    let idEdicao = null;

    function mostrar(texto, erro) {
        mensagem.textContent = texto;
        mensagem.className = erro ? "text-danger" : "text-success";
    }

    function limparFormulario() {
        idEdicao = null;
        formulario.reset();
        modo.textContent = "Novo cadastro";
        salvar.textContent = "Cadastrar";
        cancelar.hidden = true;
    }

    function botao(texto, classe) {
        const elemento = document.createElement("button");
        elemento.type = "button";
        elemento.className = classe;
        elemento.textContent = texto;
        return elemento;
    }

    function renderizar() {
        tabela.textContent = "";
        const busca = filtro.value.trim().toLowerCase();
        for (const registro of registros) {
            const valores = [registro[campoId]];
            for (const campo of campos) valores.push(registro[campo]);
            if (!valores.join(" ").toLowerCase().includes(busca)) continue;

            const linha = document.createElement("tr");
            for (const valor of valores) {
                const celula = document.createElement("td");
                celula.textContent = valor;
                linha.appendChild(celula);
            }
            const acoes = document.createElement("td");
            const editar = botao("Editar", "btn btn-sm btn-outline-primary me-2");
            editar.onclick = () => {
                idEdicao = registro[campoId];
                for (const campo of campos) formulario.elements[campo].value = registro[campo];
                modo.textContent = "Editando registro #" + idEdicao;
                salvar.textContent = "Salvar alterações";
                cancelar.hidden = false;
                formulario.elements[campos[0]].focus();
            };
            const excluir = botao("Excluir", "btn btn-sm btn-outline-danger");
            excluir.onclick = async () => {
                const id = registro[campoId];
                const aviso = recurso === "pedidos" ? "" : " Os pedidos associados também serão removidos.";
                if (!confirm("Excluir o registro #" + id + "?" + aviso)) return;
                excluir.disabled = true;
                const resposta = await api.delete(rota, id);
                excluir.disabled = false;
                if (!resposta || !resposta.success) {
                    mostrar(resposta?.message || "Não foi possível excluir.", true);
                    return;
                }
                if (idEdicao === id) limparFormulario();
                mostrar("Registro excluído.", false);
                await carregar();
            };
            acoes.appendChild(editar);
            acoes.appendChild(excluir);
            linha.appendChild(acoes);
            tabela.appendChild(linha);
        }
    }

    async function carregar() {
        const resposta = await api.get(rota);
        if (!resposta || !resposta.success) {
            mostrar(resposta?.message || "Não foi possível carregar os registros.", true);
            return;
        }
        registros = resposta.data[recurso];
        renderizar();
    }

    cancelar.onclick = limparFormulario;
    filtro.oninput = renderizar;
    formulario.onsubmit = async (evento) => {
        evento.preventDefault();
        const dados = {};
        for (const campo of campos) {
            const input = formulario.elements[campo];
            dados[campo] = input.type === "number" ? Number(input.value) : input.value.trim();
        }
        const corpo = {};
        corpo[entidade] = dados;
        salvar.disabled = true;
        let resposta;
        if (idEdicao === null) resposta = await api.post(rota, corpo);
        else resposta = await api.put(rota, idEdicao, corpo);
        salvar.disabled = false;
        if (!resposta || !resposta.success) {
            mostrar(resposta?.error?.details?.message || resposta?.message || "Não foi possível salvar.", true);
            return;
        }
        limparFormulario();
        mostrar(resposta.message, false);
        await carregar();
    };
    await carregar();
}
