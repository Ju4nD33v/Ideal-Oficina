const API = "/api";
let currentPage = "dashboard";

const content = document.getElementById("content");
const pageTitle = document.getElementById("page-title");

const esc = (value) => String(value ?? "")
  .replaceAll("&", "&amp;").replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;").replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

const money = (value) => Number(value || 0).toLocaleString("pt-BR", {
  style: "currency", currency: "BRL"
});

const dateBR = (value) => {
  if (!value) return "—";
  const d = new Date(`${value}T00:00:00`);
  return Number.isNaN(d.getTime()) ? value : d.toLocaleDateString("pt-BR");
};

function statusClass(status) {
  const s = String(status || "").toLowerCase();
  if (s.includes("concl") || s.includes("final")) return "green";
  if (s.includes("andamento") || s.includes("análise") || s.includes("analise")) return "yellow";
  if (s.includes("cancel")) return "red";
  return "blue";
}

async function api(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options
  });
  let data = null;
  try { data = await response.json(); } catch (_) {}
  if (!response.ok) {
    const detail = data?.detail || "Não foi possível concluir a operação.";
    throw new Error(detail);
  }
  return data;
}

function toast(message, error = false) {
  const el = document.createElement("div");
  el.className = `toast${error ? " error" : ""}`;
  el.textContent = message;
  document.getElementById("toast-root").appendChild(el);
  setTimeout(() => el.remove(), 3500);
}

function modal(title, body) {
  const root = document.getElementById("modal-root");
  root.innerHTML = `
    <div class="modal-backdrop" id="modal-backdrop">
      <div class="modal">
        <div class="modal-head">
          <h2>${title}</h2>
          <button class="close" id="modal-close">×</button>
        </div>
        ${body}
      </div>
    </div>`;
  document.getElementById("modal-close").onclick = closeModal;
  document.getElementById("modal-backdrop").onclick = (e) => {
    if (e.target.id === "modal-backdrop") closeModal();
  };
}

function closeModal() {
  document.getElementById("modal-root").innerHTML = "";
}

function setActive(page) {
  currentPage = page;
  document.querySelectorAll(".nav-item").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.page === page);
  });
  const titles = {
    dashboard: "Dashboard",
    clientes: "Clientes",
    veiculos: "Veículos",
    ordens: "Ordens de serviço",
    mecanicos: "Mecânicos",
    pecas: "Peças"
  };
  pageTitle.textContent = titles[page];
}

document.querySelectorAll(".nav-item").forEach(btn => {
  btn.addEventListener("click", () => loadPage(btn.dataset.page));
});

document.getElementById("refresh-btn").addEventListener("click", () => loadPage(currentPage));

function loading(message = "Carregando dados...") {
  content.innerHTML = `<div class="card empty"><div class="empty-icon">◌</div><strong>${esc(message)}</strong><br><span class="small muted">Aguarde um instante.</span></div>`;
}

function emptyState(title, description, actionId = null, actionLabel = null) {
  const action = actionId && actionLabel
    ? `<button class="primary" id="${actionId}">${esc(actionLabel)}</button>`
    : "";
  return `<div class="empty-state"><div class="empty-icon">○</div><h3>${esc(title)}</h3><p>${esc(description)}</p>${action}</div>`;
}

function asList(value) {
  return Array.isArray(value) ? value : [];
}

async function loadPage(page) {
  setActive(page);
  loading();
  try {
    if (page === "dashboard") await renderDashboard();
    if (page === "clientes") await renderClientes();
    if (page === "veiculos") await renderVeiculos();
    if (page === "ordens") await renderOrdens();
    if (page === "mecanicos") await renderMecanicos();
    if (page === "pecas") await renderPecas();
  } catch (error) {
    content.innerHTML = `
      <div class="card empty error-state">
        <div class="empty-icon">!</div>
        <strong>Não foi possível carregar a página.</strong>
        <p class="small muted">${esc(error.message)}</p>
        <button class="primary" onclick="loadPage('${esc(page)}')">Tentar novamente</button>
      </div>`;
  }
}

async function renderDashboard() {
  const data = await api("/dashboard");
  const t = data.totais || {};
  const recent = asList(data.recentes);
  const statuses = asList(data.status);
  const maxStatus = Math.max(...statuses.map(x => Number(x.quantidade)), 1);

  content.innerHTML = `
    <div class="grid stats">
      ${stat("Clientes", t.clientes, "♙")}
      ${stat("Veículos", t.veiculos, "▣")}
      ${stat("Ordens", t.ordens, "⚙")}
      ${stat("Mecânicos", t.mecanicos, "⚒")}
      ${stat("Peças", t.pecas, "◇")}
    </div>
    <div class="grid two-col">
      <div class="card">
        <div class="card-head"><h2>Ordens recentes</h2><button class="secondary" onclick="loadPage('ordens')">Ver todas</button></div>
        <div class="table-wrap">
          ${recent.length ? `<table><thead><tr><th>OS</th><th>Cliente</th><th>Veículo</th><th>Status</th><th>Valor</th></tr></thead>
          <tbody>${recent.map(o => `<tr>
            <td>#${o.id}</td><td>${esc(o.cliente)}</td><td>${esc(o.veiculo)} · ${esc(o.placa)}</td>
            <td><span class="badge ${statusClass(o.status)}">${esc(o.status)}</span></td><td>${money(o.valor)}</td>
          </tr>`).join("")}</tbody></table>` : `<div class="empty">Nenhuma ordem de serviço cadastrada.</div>`}
        </div>
      </div>
      <div class="card">
        <div class="card-head"><h2>Status das ordens</h2></div>
        <div class="card-body kpis">
          ${statuses.length ? statuses.map(s => `<div class="kpi-row">
            <div class="kpi-label">${esc(s.status)}</div>
            <div class="kpi-bar"><div class="kpi-fill" style="width:${Number(s.quantidade)/maxStatus*100}%"></div></div>
            <div class="kpi-value">${s.quantidade}</div>
          </div>`).join("") : `<div class="empty">Ainda não existem ordens.</div>`}
        </div>
      </div>
    </div>`;
}

function stat(label, value, icon) {
  return `<div class="card stat"><div class="icon">${icon}</div><div class="label">${label}</div><div class="value">${value}</div></div>`;
}

async function renderClientes() {
  const data = asList(await api("/clientes"));
  content.innerHTML = `
    <div class="page-toolbar">
      <div class="toolbar-left"><input class="search" id="cliente-search" placeholder="Buscar por nome ou telefone"></div>
      <button class="primary" id="new-client">+ Novo cliente</button>
    </div>
    <div class="card"><div class="table-wrap">
      ${data.length ? `<table><thead><tr><th>ID</th><th>Nome</th><th>Telefone</th><th>Endereço</th></tr></thead>
      <tbody>${data.map(c => `<tr><td>#${c.id}</td><td><strong>${esc(c.nome)}</strong></td><td>${esc(c.telefone)}</td><td>${esc(c.endereco)}</td></tr>`).join("")}</tbody></table>` : emptyState("Nenhum cliente cadastrado", "Cadastre o primeiro cliente da oficina para começar.", "empty-new-client", "+ Cadastrar cliente")}
    </div></div>`;
  document.getElementById("new-client").onclick = showClienteModal;
  const emptyNewClient = document.getElementById("empty-new-client");
  if (emptyNewClient) emptyNewClient.onclick = showClienteModal;
  document.getElementById("cliente-search").addEventListener("input", debounce(async (e) => {
    try {
      const result = asList(await api(`/clientes?search=${encodeURIComponent(e.target.value)}`));
      const tableWrap = content.querySelector(".table-wrap");
      if (!tableWrap) return;
      tableWrap.innerHTML = result.length
        ? `<table><thead><tr><th>ID</th><th>Nome</th><th>Telefone</th><th>Endereço</th></tr></thead><tbody>${result.map(c => `<tr><td>#${c.id}</td><td><strong>${esc(c.nome)}</strong></td><td>${esc(c.telefone)}</td><td>${esc(c.endereco)}</td></tr>`).join("")}</tbody></table>`
        : emptyState("Nenhum cliente encontrado", "Não encontramos clientes para esta busca.");
    } catch (err) { toast(err.message, true); }
  }, 250));
}

function showClienteModal() {
  modal("Cadastrar cliente", `<form class="form" id="cliente-form">
    <div class="form-grid">
      <div class="field full"><label>Nome completo</label><input name="nome" required maxlength="45"></div>
      <div class="field"><label>Telefone</label><input name="telefone" required maxlength="45"></div>
      <div class="field"><label>Endereço</label><input name="endereco" required maxlength="100"></div>
    </div>
    <div class="form-actions"><button type="button" class="secondary" onclick="closeModal()">Cancelar</button><button class="primary">Cadastrar</button></div>
  </form>`);
  document.getElementById("cliente-form").onsubmit = async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    try { await api("/clientes", { method:"POST", body:JSON.stringify(data) }); closeModal(); toast("Cliente cadastrado."); renderClientes(); }
    catch (err) { toast(err.message, true); }
  };
}

async function renderVeiculos() {
  const data = asList(await api("/veiculos"));
  let clientes = [];
  try { clientes = asList(await api("/clientes")); } catch (err) { toast("Não foi possível carregar os clientes para o cadastro de veículos.", true); }
  content.innerHTML = `
    <div class="page-toolbar"><div class="toolbar-left"><span class="muted small">${data.length} veículo(s) cadastrado(s)</span></div><button class="primary" id="new-vehicle">+ Novo veículo</button></div>
    <div class="card"><div class="table-wrap">
      ${data.length ? `<table><thead><tr><th>Veículo</th><th>Placa</th><th>Cliente</th><th>Ano</th><th>Problema</th></tr></thead>
      <tbody>${data.map(v => `<tr><td><strong>${esc(v.modelo)}</strong><br><span class="muted small">${esc(v.cor)}</span></td><td>${esc(v.placa)}</td><td>${esc(v.cliente_nome)}</td><td>${esc(v.ano)}</td><td>${esc(v.problema)}</td></tr>`).join("")}</tbody></table>` : emptyState("Nenhum veículo cadastrado", "Cadastre um veículo para começar a controlar os atendimentos.", "empty-new-vehicle", "+ Cadastrar veículo")}
    </div></div>`;
  document.getElementById("new-vehicle").onclick = () => showVeiculoModal(clientes);
  const emptyNewVehicle = document.getElementById("empty-new-vehicle");
  if (emptyNewVehicle) emptyNewVehicle.onclick = () => showVeiculoModal(clientes);
}

function showVeiculoModal(clientes) {
  modal("Cadastrar veículo", `<form class="form" id="veiculo-form">
    <div class="form-grid">
      <div class="field full"><label>Cliente</label><select name="dono_veiculo" required>${clientes.map(c => `<option value="${c.id}">${esc(c.nome)} · ${esc(c.telefone)}</option>`).join("")}</select></div>
      <div class="field"><label>Modelo</label><input name="modelo" placeholder="Honda Civic" required></div>
      <div class="field"><label>Cor</label><input name="cor" required></div>
      <div class="field"><label>Ano</label><input name="ano" minlength="4" maxlength="4" required></div>
      <div class="field"><label>Placa</label><input name="placa" maxlength="45" required></div>
      <div class="field full"><label>Problema apresentado</label><textarea name="problema" required></textarea></div>
    </div>
    <div class="form-actions"><button type="button" class="secondary" onclick="closeModal()">Cancelar</button><button class="primary">Cadastrar</button></div>
  </form>`);
  if (!clientes.length) document.getElementById("veiculo-form").innerHTML = `<div class="empty">Cadastre um cliente antes de cadastrar um veículo.</div>`;
  document.getElementById("veiculo-form").onsubmit = async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    data.dono_veiculo = Number(data.dono_veiculo);
    try { await api("/veiculos", {method:"POST",body:JSON.stringify(data)}); closeModal(); toast("Veículo cadastrado."); renderVeiculos(); }
    catch (err) { toast(err.message, true); }
  };
}

async function renderMecanicos() {
  const data = asList(await api("/mecanicos"));
  content.innerHTML = `
    <div class="page-toolbar"><div class="toolbar-left"><span class="muted small">${data.length} mecânico(s) cadastrado(s)</span></div><button class="primary" id="new-mechanic">+ Novo mecânico</button></div>
    <div class="card"><div class="table-wrap">
      ${data.length ? `<table><thead><tr><th>Nome</th><th>Especialidade</th><th>Endereço</th><th>Código</th></tr></thead>
      <tbody>${data.map(m => `<tr><td><strong>${esc(m.nome)}</strong></td><td>${esc(m.especialidade)}</td><td>${esc(m.endereco)}</td><td><span class="badge blue">${esc(m.codigo_mecanico)}</span></td></tr>`).join("")}</tbody></table>` : emptyState("Nenhum mecânico cadastrado", "Cadastre os profissionais que trabalham na oficina.", "empty-new-mechanic", "+ Cadastrar mecânico")}
    </div></div>`;
  document.getElementById("new-mechanic").onclick = showMecanicoModal;
  const emptyNewMechanic = document.getElementById("empty-new-mechanic");
  if (emptyNewMechanic) emptyNewMechanic.onclick = showMecanicoModal;
}

function showMecanicoModal() {
  modal("Cadastrar mecânico", `<form class="form" id="mecanico-form">
    <div class="form-grid">
      <div class="field full"><label>Nome</label><input name="nome" required></div>
      <div class="field full"><label>Endereço</label><input name="endereco" required></div>
      <div class="field full"><label>Especialidade</label><input name="especialidade" placeholder="Motor, freios, elétrica..." required></div>
    </div>
    <div class="form-actions"><button type="button" class="secondary" onclick="closeModal()">Cancelar</button><button class="primary">Cadastrar</button></div>
  </form>`);
  document.getElementById("mecanico-form").onsubmit = async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    try {
      const result = await api("/mecanicos", {method:"POST",body:JSON.stringify(data)});
      closeModal();
      modal("Mecânico cadastrado", `<div class="form"><div class="detail"><span>Código de acesso</span><strong style="font-size:26px;letter-spacing:3px">${result.codigo_mecanico}</strong></div><p class="muted small">Guarde este código. Ele é gerado pelo sistema e será necessário para o acesso do mecânico.</p><div class="form-actions"><button class="primary" onclick="closeModal();renderMecanicos()">Concluir</button></div></div>`);
      toast("Mecânico cadastrado.");
    } catch (err) { toast(err.message, true); }
  };
}

async function renderPecas() {
  const data = asList(await api("/pecas"));
  content.innerHTML = `
    <div class="page-toolbar"><div class="toolbar-left"><span class="muted small">${data.length} peça(s) no catálogo</span></div><button class="primary" id="new-part">+ Nova peça</button></div>
    <div class="card"><div class="table-wrap">
      ${data.length ? `<table><thead><tr><th>Peça</th><th>Valor</th><th>Garantia</th><th>Descrição</th></tr></thead>
      <tbody>${data.map(p => `<tr><td><strong>${esc(p.nome)}</strong></td><td>${money(p.valor)}</td><td>${esc(p.garantia)}</td><td>${esc(p.descricao)}</td></tr>`).join("")}</tbody></table>` : emptyState("Nenhuma peça cadastrada", "Cadastre peças para utilizá-las nas ordens de serviço.", "empty-new-part", "+ Cadastrar peça")}
    </div></div>`;
  document.getElementById("new-part").onclick = showPecaModal;
  const emptyNewPart = document.getElementById("empty-new-part");
  if (emptyNewPart) emptyNewPart.onclick = showPecaModal;
}

function showPecaModal() {
  modal("Cadastrar peça", `<form class="form" id="peca-form">
    <div class="form-grid">
      <div class="field"><label>Nome</label><input name="nome" required></div>
      <div class="field"><label>Valor</label><input name="valor" type="number" min="0" step="0.01" required></div>
      <div class="field"><label>Garantia</label><input name="garantia" placeholder="12 meses" required></div>
      <div class="field full"><label>Descrição</label><textarea name="descricao" required></textarea></div>
    </div>
    <div class="form-actions"><button type="button" class="secondary" onclick="closeModal()">Cancelar</button><button class="primary">Cadastrar</button></div>
  </form>`);
  document.getElementById("peca-form").onsubmit = async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    data.valor = Number(data.valor);
    try { await api("/pecas", {method:"POST",body:JSON.stringify(data)}); closeModal(); toast("Peça cadastrada."); renderPecas(); }
    catch (err) { toast(err.message, true); }
  };
}

async function renderOrdens() {
  const ordens = asList(await api("/ordens-servico"));
  let veiculos = [], mecanicos = [], pecas = [];
  try { veiculos = asList(await api("/veiculos")); } catch (err) { toast("Não foi possível carregar os veículos.", true); }
  try { mecanicos = asList(await api("/mecanicos")); } catch (err) { toast("Não foi possível carregar os mecânicos.", true); }
  try { pecas = asList(await api("/pecas")); } catch (err) { toast("Não foi possível carregar as peças.", true); }
  content.innerHTML = `
    <div class="page-toolbar"><div class="toolbar-left"><span class="muted small">${ordens.length} ordem(ns) de serviço</span></div><button class="primary" id="new-os">+ Nova ordem</button></div>
    <div class="card"><div class="table-wrap">
      ${ordens.length ? `<table><thead><tr><th>OS</th><th>Cliente / veículo</th><th>Mecânico</th><th>Emissão</th><th>Conclusão</th><th>Status</th><th>Valor</th><th>Ação</th></tr></thead>
      <tbody>${ordens.map(o => `<tr>
        <td>#${o.id}</td>
        <td><strong>${esc(o.veiculo_modelo)}</strong><br><span class="muted small">${esc(o.placa)}</span></td>
        <td>${esc(o.mecanico_nome)}</td><td>${dateBR(o.data_emissao)}</td><td>${dateBR(o.data_conclusao)}</td>
        <td><span class="badge ${statusClass(o.status)}">${esc(o.status)}</span></td><td>${money(o.valor)}</td>
        <td><button class="secondary" onclick="changeStatus(${o.id}, '${esc(o.status)}')">Status</button></td>
      </tr>`).join("")}</tbody></table>` : `<div class="empty">Nenhuma ordem de serviço cadastrada.</div>`}
    </div></div>`;
  document.getElementById("new-os").onclick = () => showOSModal(veiculos, mecanicos, pecas);
  const emptyNewOS = document.getElementById("empty-new-os");
  if (emptyNewOS) emptyNewOS.onclick = () => showOSModal(veiculos, mecanicos, pecas);
}

function showOSModal(veiculos, mecanicos, pecas) {
  modal("Nova ordem de serviço", `<form class="form" id="os-form">
    <div class="form-grid">
      <div class="field full"><label>Veículo</label><select name="veiculo_id" required>${veiculos.map(v => `<option value="${v.id}">${esc(v.modelo)} · ${esc(v.placa)} · ${esc(v.cliente_nome)}</option>`).join("")}</select></div>
      <div class="field"><label>Mecânico responsável</label><select name="mecanico_id" required>${mecanicos.map(m => `<option value="${m.id}">${esc(m.nome)} · ${esc(m.especialidade)}</option>`).join("")}</select></div>
      <div class="field"><label>Peça</label><select name="peca_id" required>${pecas.map(p => `<option value="${p.id}">${esc(p.nome)} · ${money(p.valor)}</option>`).join("")}</select></div>
      <div class="field"><label>Status inicial</label><select name="status"><option>Em análise</option><option>Em andamento</option><option>Aguardando peça</option><option>Concluída</option></select></div>
      <div class="field"><label>Previsão de conclusão</label><input name="data_conclusao" type="date" required></div>
      <div class="field full"><label>Serviço / mão de obra</label><textarea name="mao_de_obra" required placeholder="Descrição do serviço que será realizado"></textarea></div>
      <div class="field"><label>Valor da mão de obra</label><input name="valor_mao_de_obra" type="number" min="0" step="0.01" required></div>
    </div>
    <p class="muted small">O valor total será calculado automaticamente: mão de obra + peça selecionada.</p>
    <div class="form-actions"><button type="button" class="secondary" onclick="closeModal()">Cancelar</button><button class="primary">Criar OS</button></div>
  </form>`);
  const form = document.getElementById("os-form");
  if (!veiculos.length || !mecanicos.length || !pecas.length) {
    form.insertAdjacentHTML("afterbegin", `<div class="badge yellow">Para criar uma OS, cadastre pelo menos um veículo, um mecânico e uma peça.</div>`);
  }
  form.onsubmit = async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    data.veiculo_id = Number(data.veiculo_id);
    data.mecanico_id = Number(data.mecanico_id);
    data.peca_id = Number(data.peca_id);
    data.valor_mao_de_obra = Number(data.valor_mao_de_obra);
    try { await api("/ordens-servico", {method:"POST",body:JSON.stringify(data)}); closeModal(); toast("Ordem de serviço criada."); renderOrdens(); }
    catch (err) { toast(err.message, true); }
  };
}

async function changeStatus(id, current) {
  modal(`Atualizar OS #${id}`, `<form class="form" id="status-form">
    <div class="field"><label>Novo status</label><select name="status">
      ${["Em análise","Em andamento","Aguardando peça","Concluída","Cancelada"].map(s => `<option ${s===current?"selected":""}>${s}</option>`).join("")}
    </select></div>
    <div class="form-actions"><button type="button" class="secondary" onclick="closeModal()">Cancelar</button><button class="primary">Salvar</button></div>
  </form>`);
  document.getElementById("status-form").onsubmit = async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    try { await api(`/ordens-servico/${id}/status`, {method:"PATCH",body:JSON.stringify(data)}); closeModal(); toast("Status atualizado."); renderOrdens(); }
    catch (err) { toast(err.message, true); }
  };
}

function debounce(fn, wait) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), wait); };
}

function tickClock() {
  document.getElementById("clock").textContent = new Date().toLocaleString("pt-BR", {
    dateStyle:"short", timeStyle:"short"
  });
}
setInterval(tickClock, 1000);
tickClock();
loadPage("dashboard");
