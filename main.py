from collections import deque
import os

class GrafoContagios:
    def __init__(self):
        self.pessoas = {} 
        self.adjacencias = {} 

    def adicionar_pessoa(self, id_pessoa, nome, status_saude="Suscetível"):
        if id_pessoa not in self.pessoas:
            self.pessoas[id_pessoa] = {"nome": nome, "status": status_saude}
            self.adjacencias[id_pessoa] = set()
            return True
        return False

    def registrar_contato(self, id1, id2):
        if id1 in self.pessoas and id2 in self.pessoas:
            self.adjacencias[id1].add(id2)
            self.adjacencias[id2].add(id1)
            return True
        return False

    def listar_pessoas(self):
        if not self.pessoas:
            print("Nenhuma pessoa cadastrada.")
            return
        print(f"\n{'-'*40}")
        print(f"{'ID':<5} | {'NOME':<15} | {'STATUS':<12} | {'CONTATOS'}")
        print(f"{'-'*40}")
        for id_p, dados in self.pessoas.items():
            qtd_contatos = len(self.adjacencias[id_p])
            print(f"{id_p:<5} | {dados['nome']:<15} | {dados['status']:<12} | {qtd_contatos}")
        print(f"{'-'*40}\n")

    def editar_pessoa(self, id_pessoa, novo_nome=None, novo_status=None):
        if id_pessoa in self.pessoas:
            if novo_nome:
                self.pessoas[id_pessoa]["nome"] = novo_nome
            if novo_status:
                self.pessoas[id_pessoa]["status"] = novo_status
            return True
        return False

    def remover_pessoa(self, id_pessoa):
        if id_pessoa in self.pessoas:
            for vizinho in self.adjacencias[id_pessoa]:
                self.adjacencias[vizinho].remove(id_pessoa)
            
            del self.adjacencias[id_pessoa]
            del self.pessoas[id_pessoa]
            return True
        return False

    def remover_contato(self, id1, id2):
        if id1 in self.pessoas and id2 in self.pessoas:
            if id2 in self.adjacencias[id1]:
                self.adjacencias[id1].remove(id2)
                self.adjacencias[id2].remove(id1)
                return True
        return False

    def identificar_super_espalhadores(self, top_n=3):
        graus = [(p, len(contatos)) for p, contatos in self.adjacencias.items()]
        graus.sort(key=lambda x: x[1], reverse=True)
        
        resultado = []
        for id_p, grau in graus[:top_n]:
            resultado.append((self.pessoas[id_p]["nome"], grau))
        return resultado

    def rastrear_arvore_infeccao(self, paciente_zero_id):
        if paciente_zero_id not in self.pessoas:
            return None

        visitados = set()
        fila = deque([paciente_zero_id]) 
        visitados.add(paciente_zero_id)
        
        filhos_map = {}

        while fila:
            vertice_atual = fila.popleft()
            
            for vizinho in self.adjacencias[vertice_atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    if vertice_atual not in filhos_map:
                        filhos_map[vertice_atual] = []
                    filhos_map[vertice_atual].append(vizinho)
                    fila.append(vizinho)
                    
        return filhos_map

    def exibir_arvore(self, no_atual, filhos_map, prefixo="", e_ultimo=True, e_raiz=True):
        if e_raiz:
            print(f"[{self.pessoas[no_atual]['status']}] {self.pessoas[no_atual]['nome']}")
        else:
            marcador = "└── " if e_ultimo else "├── "
            print(f"{prefixo}{marcador}[{self.pessoas[no_atual]['status']}] {self.pessoas[no_atual]['nome']}")
        
        prefixo_filhos = prefixo + ("    " if e_ultimo else "│   ") if not e_raiz else ""
        
        filhos = filhos_map.get(no_atual, [])
        for i, filho in enumerate(filhos):
            ultimo_filho = (i == len(filhos) - 1)
            self.exibir_arvore(filho, filhos_map, prefixo_filhos, ultimo_filho, False)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_interativo():
    grafo = GrafoContagios()
    
    while True:
        print("\n" + "="*45)
        print(" 🦠 RASTREIO EPIDEMIOLÓGICO ")
        print("="*45)
        print("1. Cadastrar Pessoa (Vértice)")
        print("2. Registrar Contato (Aresta)")
        print("3. Listar População")
        print("4. Editar Status/Nome de Pessoa")
        print("5. Remover Pessoa")
        print("6. Remover Contato")
        print("7. Analisar Super-espalhadores (Centralidade)")
        print("8. Gerar Árvore de Contágio (BFS)")
        print("0. Sair")
        print("="*45)
        
        opcao = input("Escolha uma opção: ")
        limpar_tela()

        if opcao == "1":
            print("--- CADASTRAR PESSOA ---")
            id_p = input("Digite o ID (ex: 1): ")
            nome = input("Digite o Nome: ")
            print("Status: 1-Suscetível | 2-Infectado | 3-Recuperado")
            st_op = input("Escolha o status (padrão 1): ")
            status = "Infectado" if st_op == "2" else "Recuperada" if st_op == "3" else "Suscetível"
            
            if grafo.adicionar_pessoa(id_p, nome, status):
                print(f"Sucesso! {nome} adicionado(a).")
            else:
                print("Erro: ID já existe no sistema.")

        elif opcao == "2":
            print("--- REGISTRAR CONTATO ---")
            grafo.listar_pessoas()
            id1 = input("ID da Pessoa A: ")
            id2 = input("ID da Pessoa B: ")
            if grafo.registrar_contato(id1, id2):
                print("Contato registrado com sucesso!")
            else:
                print("Erro: Verifique se ambos os IDs existem e estão corretos.")

        elif opcao == "3":
            print("--- POPULAÇÃO CADASTRADA ---")
            grafo.listar_pessoas()

        elif opcao == "4":
            print("--- EDITAR PESSOA ---")
            grafo.listar_pessoas()
            id_p = input("ID da pessoa a editar: ")
            novo_nome = input("Novo Nome (deixe em branco para manter): ")
            print("Novo Status: 1-Suscetível | 2-Infectado | 3-Recuperado | (Deixe em branco para manter)")
            st_op = input("Escolha: ")
            novo_status = None
            if st_op == "1": novo_status = "Suscetível"
            elif st_op == "2": novo_status = "Infectado"
            elif st_op == "3": novo_status = "Recuperada"
            
            if grafo.editar_pessoa(id_p, novo_nome if novo_nome else None, novo_status):
                print("Cadastro atualizado!")
            else:
                print("Erro: Pessoa não encontrada.")

        elif opcao == "5":
            print("--- REMOVER PESSOA ---")
            grafo.listar_pessoas()
            id_p = input("Digite o ID da pessoa a ser removida: ")
            if grafo.remover_pessoa(id_p):
                print("Pessoa e todas as suas conexões foram apagadas do grafo.")
            else:
                print("Erro: Pessoa não encontrada.")

        elif opcao == "6":
            print("--- REMOVER CONTATO ---")
            id1 = input("ID da Pessoa A: ")
            id2 = input("ID da Pessoa B: ")
            if grafo.remover_contato(id1, id2):
                print("Conexão (aresta) removida com sucesso!")
            else:
                print("Erro: Contato não existe ou IDs inválidos.")

        elif opcao == "7":
            print("--- SUPER-ESPALHADORES ---")
            espalhadores = grafo.identificar_super_espalhadores()
            if not espalhadores:
                print("Grafo vazio ou sem conexões.")
            else:
                for nome, grau in espalhadores:
                    print(f"- {nome}: {grau} contatos")

        elif opcao == "8":
            print("--- ÁRVORE DE CONTÁGIO (BFS) ---")
            grafo.listar_pessoas()
            id_p = input("Digite o ID do Paciente Zero: ")
            arvore_map = grafo.rastrear_arvore_infeccao(id_p)
            
            if arvore_map is None:
                print("Erro: Paciente não encontrado.")
            else:
                print("\nVisualização da Cadeia de Infecção:\n")
                grafo.exibir_arvore(id_p, arvore_map)

        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            
        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    menu_interativo()