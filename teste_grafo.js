const pessoas = {};
const adjacencias = {};

function adicionarPessoa(id, nome, status) {
  pessoas[id] = { id, nome, status };
  adjacencias[id] = [];
}

function registrarContato(id1, id2) {
  if (!adjacencias[id1].includes(id2)) adjacencias[id1].push(id2);
  if (!adjacencias[id2].includes(id1)) adjacencias[id2].push(id1);
}

function identificarSuperEspalhadores() {
  const graus = Object.keys(adjacencias).map(id => ({
    nome: pessoas[id].nome,
    grau: adjacencias[id].length
  }));
  graus.sort((a, b) => b.grau - a.grau);
  return graus.slice(0, 3);
}

function rastrearInfeccao(pacienteZeroId) {
  const visitados = new Set();
  const fila = [{ id: pacienteZeroId, distancia: 0 }];
  visitados.add(pacienteZeroId);
  
  const arvore = [];

  while (fila.length > 0) {
    const atual = fila.shift();
    arvore.push({
      nome: pessoas[atual.id].nome,
      grau_separacao: atual.distancia
    });

    const vizinhos = adjacencias[atual.id];
    for (let vizinho of vizinhos) {
      if (!visitados.has(vizinho)) {
        visitados.add(vizinho);
        fila.push({ id: vizinho, distancia: atual.distancia + 1 });
      }
    }
  }
  return arvore;
}

console.log("--- INICIANDO TESTES DO GRAFO ---\n");

// A. Populando Vrtices
adicionarPessoa("p1", "João", "Infectado");
adicionarPessoa("p2", "Maria", "Suscetível");
adicionarPessoa("p3", "Carlos", "Suscetível");
adicionarPessoa("p4", "Ana", "Recuperada");
console.log("✔️ Vértices criados com sucesso.");

registrarContato("p1", "p2"); // João e Maria
registrarContato("p1", "p3"); // João e Carlos
registrarContato("p2", "p4"); // Maria e Ana
console.log("✔️ Arestas (Contatos) registradas com sucesso.\n");

console.log("--- TESTE: SUPER-ESPALHADORES ---");
console.table(identificarSuperEspalhadores());
console.log("\n");

console.log("--- TESTE: ÁRVORE DE INFECÇÃO (BFS a partir do João) ---");
console.table(rastrearInfeccao("p1"));