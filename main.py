from collections import deque

class GrafoContagios:
    def __init__(self):
        self.pessoas = {} 
        self.adjacencias = {} 

    def adicionar_pessoa(self, id_pessoa, nome, status_saude="Suscetível"):
        """Adiciona um vértice ao grafo."""
        if id_pessoa not in self.pessoas:
            self.pessoas[id_pessoa] = {
                "nome": nome,
                "status": status_saude
            }
            self.adjacencias[id_pessoa] = set()

    def registrar_contato(self, id1, id2):
        """Cria uma aresta não-direcionada entre duas pessoas."""
        if id1 in self.pessoas and id2 in self.pessoas:
            self.adjacencias[id1].add(id2)
            self.adjacencias[id2].add(id1)
        else:
            print("Erro: Ambas as pessoas precisam estar cadastradas.")

    def identificar_super_espalhadores(self, top_n=3):
        """
        Calcula a Centralidade de Grau: 
        Retorna os nós com o maior número de arestas.
        """
        graus = [(p, len(contatos)) for p, contatos in self.adjacencias.items()]
        graus.sort(key=lambda x: x[1], reverse=True)
        
        resultado = []
        for id_p, grau in graus[:top_n]:
            resultado.append((self.pessoas[id_p]["nome"], grau))
        return resultado

    def rastrear_arvore_infeccao(self, paciente_zero_id):
        """
        Executa uma Busca em Largura (BFS) para descobrir a cadeia de contágio.
        Retorna a distância (grau de separação) de cada pessoa até o paciente zero.
        """
        if paciente_zero_id not in self.pessoas:
            return None

        visitados = set()
        fila = deque([(paciente_zero_id, 0)]) 
        visitados.add(paciente_zero_id)
        
        arvore_contagio = []

        while fila:
            vertice_atual, distancia = fila.popleft()
            nome_atual = self.pessoas[vertice_atual]["nome"]
            status_atual = self.pessoas[vertice_atual]["status"]
            
            arvore_contagio.append({
                "id": vertice_atual,
                "nome": nome_atual,
                "status": status_atual,
                "grau_separacao": distancia
            })

            for vizinho in self.adjacencias[vertice_atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append((vizinho, distancia + 1))
                    
        return arvore_contagio

if __name__ == "__main__":
    grafo = GrafoContagios()

    grafo.adicionar_pessoa("p1", "João", "Infectado") # Paciente Zero
    grafo.adicionar_pessoa("p2", "Maria", "Suscetível")
    grafo.adicionar_pessoa("p3", "Carlos", "Suscetível")
    grafo.adicionar_pessoa("p4", "Ana", "Recuperada")
    grafo.adicionar_pessoa("p5", "Pedro", "Suscetível")

    grafo.registrar_contato("p1", "p2")
    grafo.registrar_contato("p1", "p3")
    grafo.registrar_contato("p2", "p4")
    grafo.registrar_contato("p2", "p5")
    grafo.registrar_contato("p3", "p5")

    print("--- Super-espalhadores (Centralidade de Grau) ---")
    espalhadores = grafo.identificar_super_espalhadores(top_n=2)
    for nome, grau in espalhadores:
        print(f"{nome}: {grau} contatos registrados.")

    print("\n--- Árvore de Contágio (BFS a partir de João) ---")
    arvore = grafo.rastrear_arvore_infeccao("p1")
    for no in arvore:
        print(f"Grau {no['grau_separacao']} | {no['nome']} (Status: {no['status']})")