import React, { useState } from 'react';

export default function App() {
  const [pessoas, setPessoas] = useState({});
  const [adjacencias, setAdjacencias] = useState({});
  
  const [nomeForm, setNomeForm] = useState('');
  const [statusForm, setStatusForm] = useState('Suscetível');
  const [contatoP1, setContatoP1] = useState('');
  const [contatoP2, setContatoP2] = useState('');
  const [pacienteZero, setPacienteZero] = useState('');
  
  const [arvoreBfs, setArvoreBfs] = useState([]);
  const [superEspalhadores, setSuperEspalhadores] = useState([]);

  
  const adicionarPessoa = (e) => {
    e.preventDefault();
    if (!nomeForm) return;
    
    const id = `p_${Date.now()}`; 
    setPessoas({ ...pessoas, [id]: { id, nome: nomeForm, status: statusForm } });
    setAdjacencias({ ...adjacencias, [id]: [] }); 
    setNomeForm('');
  };

  const registrarContato = (e) => {
    e.preventDefault();
    if (contatoP1 && contatoP2 && contatoP1 !== contatoP2) {
      setAdjacencias((prev) => {
        const novasAdj = { ...prev };
        if (!novasAdj[contatoP1].includes(contatoP2)) novasAdj[contatoP1] = [...novasAdj[contatoP1], contatoP2];
        if (!novasAdj[contatoP2].includes(contatoP1)) novasAdj[contatoP2] = [...novasAdj[contatoP2], contatoP1];
        return novasAdj;
      });
    }
  };


  const identificarSuperEspalhadores = () => {
    const graus = Object.keys(adjacencias).map((id) => ({
      id,
      nome: pessoas[id].nome,
      grau: adjacencias[id].length
    }));
    
    graus.sort((a, b) => b.grau - a.grau);
    setSuperEspalhadores(graus.slice(0, 3)); 
  };

  const rastrearInfeccao = (e) => {
    e.preventDefault();
    if (!pacienteZero || !pessoas[pacienteZero]) return;

    const visitados = new Set();
    const fila = [{ id: pacienteZero, distancia: 0 }];
    visitados.add(pacienteZero);
    
    const resultado = [];

    while (fila.length > 0) {
      const atual = fila.shift(); 
      const dadosPessoa = pessoas[atual.id];
      
      resultado.push({
        ...dadosPessoa,
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
    setArvoreBfs(resultado);
  };

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
      <h1>🦠 ContágioGraph - Rastreador Epidemiológico</h1>
      
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        {/* PAINEL 1: Cadastro de Vértices */}
        <div style={{ border: '1px solid #ccc', padding: '15px', flex: 1 }}>
          <h3>Adicionar Indivíduo (Vértice)</h3>
          <form onSubmit={adicionarPessoa}>
            <input 
              type="text" placeholder="Nome" value={nomeForm} 
              onChange={(e) => setNomeForm(e.target.value)} required 
              style={{ display: 'block', marginBottom: '10px', width: '100%' }}
            />
            <select 
              value={statusForm} onChange={(e) => setStatusForm(e.target.value)}
              style={{ display: 'block', marginBottom: '10px', width: '100%' }}
            >
              <option value="Suscetível">Suscetível (Azul)</option>
              <option value="Infectado">Infectado (Vermelho)</option>
              <option value="Recuperado">Recuperado (Verde)</option>
            </select>
            <button type="submit">Salvar Indivíduo</button>
          </form>
        </div>

        <div style={{ border: '1px solid #ccc', padding: '15px', flex: 1 }}>
          <h3>Registrar Contato (Aresta)</h3>
          <form onSubmit={registrarContato}>
            <select value={contatoP1} onChange={(e) => setContatoP1(e.target.value)} required style={{ display: 'block', marginBottom: '10px', width: '100%' }}>
              <option value="">Selecione a Pessoa A...</option>
              {Object.values(pessoas).map(p => <option key={p.id} value={p.id}>{p.nome}</option>)}
            </select>
            <select value={contatoP2} onChange={(e) => setContatoP2(e.target.value)} required style={{ display: 'block', marginBottom: '10px', width: '100%' }}>
              <option value="">Selecione a Pessoa B...</option>
              {Object.values(pessoas).map(p => <option key={p.id} value={p.id}>{p.nome}</option>)}
            </select>
            <button type="submit">Criar Conexão</button>
          </form>
        </div>
      </div>

      <div style={{ border: '1px solid #0056b3', padding: '15px', backgroundColor: '#f4f8ff' }}>
        <h2>Análise do Grafo</h2>
        
        <div style={{ marginBottom: '20px' }}>
          <button onClick={identificarSuperEspalhadores}>Calcular Super-espalhadores (Centralidade)</button>
          {superEspalhadores.length > 0 && (
            <ul>
              {superEspalhadores.map(se => (
                <li key={se.id}><strong>{se.nome}</strong>: {se.grau} contatos registrados</li>
              ))}
            </ul>
          )}
        </div>

        <hr />

        <div>
          <h3>Rastrear Cadeia de Infecção (BFS)</h3>
          <form onSubmit={rastrearInfeccao} style={{ display: 'flex', gap: '10px' }}>
            <select value={pacienteZero} onChange={(e) => setPacienteZero(e.target.value)} required>
              <option value="">Selecione o Paciente Zero...</option>
              {Object.values(pessoas).filter(p => p.status === 'Infectado').map(p => (
                <option key={p.id} value={p.id}>{p.nome}</option>
              ))}
            </select>
            <button type="submit">Gerar Árvore</button>
          </form>
          
          {arvoreBfs.length > 0 && (
            <table style={{ width: '100%', marginTop: '15px', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#ddd' }}>
                  <th style={{ padding: '8px', border: '1px solid #ccc' }}>Grau de Exposição</th>
                  <th style={{ padding: '8px', border: '1px solid #ccc' }}>Nome</th>
                  <th style={{ padding: '8px', border: '1px solid #ccc' }}>Status Atual</th>
                </tr>
              </thead>
              <tbody>
                {arvoreBfs.map(no => (
                  <tr key={no.id}>
                    <td style={{ padding: '8px', border: '1px solid #ccc', textAlign: 'center' }}>
                      {no.grau_separacao === 0 ? 'Paciente Zero' : `Grau ${no.grau_separacao}`}
                    </td>
                    <td style={{ padding: '8px', border: '1px solid #ccc' }}>{no.nome}</td>
                    <td style={{ padding: '8px', border: '1px solid #ccc' }}>{no.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}