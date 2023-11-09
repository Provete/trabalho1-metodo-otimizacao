from linhadeproducao.Maquina import Maquina
import math
import sys
import time

NOME_ARQUIVO_SOLUCAO = 'solução.txt'


class LinhaDeProducao:
    tarefas: list[int]
    grafo_precedencia_tarefas: list[list[bool]]
    digrafo_precedencia_tarefas: list[list[bool]]
    tempo_execucao: float
    maquinas: list[Maquina]

    def __init__(self, nome_arquivo: str, numero_maquinas: int, tarefa_inicial: int):
        self.maquinas = list()
        self.tempo_execucao = 0
        self.ler_arquivo(nome_arquivo)
        self.inicializar_maquinas(numero_maquinas)
        self.criar_solucao_inicial_BFS(tarefa_inicial)

    def inicializar_maquinas(self, numero_maquinas: int):
        tarefas_por_maquina: int = int(math.floor(self.calcular_numero_de_tarefas() / numero_maquinas))
        restante: int = self.calcular_numero_de_tarefas() % numero_maquinas
        index_ultima_maquina: int = numero_maquinas - 1

        for i in range(0, index_ultima_maquina):
            nova_maquina: Maquina = Maquina(tarefas_por_maquina)
            self.maquinas.append(nova_maquina)

        ultima_maquina: Maquina = Maquina(tarefas_por_maquina + restante)
        self.maquinas.append(ultima_maquina)

    def ler_arquivo(self, nome_arquivo: str):
        custo_tarefas: list[int] = list()
        grafo_precedencia_tarefas: list[list[bool]] = list()
        digrafo_precedencia_tarefas: list[list[bool]] = list()

        with open(nome_arquivo, 'r') as arquivo:
            quantidade_tarefas: int = int(arquivo.readline())

            for i in range(0, quantidade_tarefas):
                custo_tarefa = int(arquivo.readline())
                custo_tarefas.append(custo_tarefa)

                grafo_precedencia_tarefas.append([False] * quantidade_tarefas)
                digrafo_precedencia_tarefas.append([False] * quantidade_tarefas)

            for l in arquivo:
                predecessor, sucessor = l.split(',')
                predecessor = int(predecessor) - 1
                sucessor = int(sucessor) - 1

                if predecessor == -2 or sucessor == -2:
                    continue

                grafo_precedencia_tarefas[predecessor][sucessor] = True
                digrafo_precedencia_tarefas[predecessor][sucessor] = True
                grafo_precedencia_tarefas[sucessor][predecessor] = True

        self.grafo_precedencia_tarefas = grafo_precedencia_tarefas
        self.digrafo_precedencia_tarefas = digrafo_precedencia_tarefas
        self.tarefas = custo_tarefas

    def imprimir_grafo(self):
        for l in self.grafo_precedencia_tarefas:
            for v in l:
                print(f'{int(v)} ', end=' ')
            print()

    def pegar_tarefas(self) -> list[int]:
        return list(range(0, len(self.grafo_precedencia_tarefas[0])))

    def calcular_numero_de_tarefas(self) -> int:
        return len(self.pegar_tarefas())

    def pegar_tarefas_sucessoras(self, tarefa: int) -> set[int]:
        tarefas_adjacentes: list[int] = self.digrafo_precedencia_tarefas[tarefa]
        tarefas_sucessoras: set[int] = set()

        for i in range(0, self.calcular_numero_de_tarefas()):
            if tarefas_adjacentes[i]:
                tarefas_sucessoras.add(i)

        return tarefas_sucessoras

    def pegar_tarefas_antecessoras(self, tarefa) -> list[int]:
        tarefas_antecessoras: list[int] = list()
        for i in range(0, self.calcular_numero_de_tarefas()):
            if self.digrafo_precedencia_tarefas[i][tarefa]:
                tarefas_antecessoras.append(i)

        return tarefas_antecessoras

    def adicionar_tarefas_antecessoras(self, tarefa: int,  fila: list[int]):
        tarefas_antecessoras = self.pegar_tarefas_antecessoras(tarefa)
        tarefas_antecessoras = list(set(tarefas_antecessoras) & set(fila))

        for tarefa_antecessora in tarefas_antecessoras:
            if tarefa_antecessora in fila:
                self.adicionar_tarefas_antecessoras(tarefa_antecessora, fila)

        index_maquina: int = 0
        while not self.maquinas[index_maquina].pode_adicionar_tarefa():
            index_maquina += 1

        self.maquinas[index_maquina].adicionar_tarefa(tarefa)
        if tarefa in fila:
            fila.remove(tarefa)

    def criar_solucao_inicial_BFS(self, tarefa_inicial):
        tempo_inicial: float = time.perf_counter()

        fila = self.pegar_tarefas()

        # coloca a tarefa inicial no inicio da fila
        visitados = [tarefa_inicial]
        fila.remove(tarefa_inicial)
        fila.insert(0, tarefa_inicial)

        while fila:
            tarefa = fila.pop(0)
            self.adicionar_tarefas_antecessoras(tarefa, fila)

            for tarefa_sucessora in self.pegar_tarefas_sucessoras(tarefa):
                if tarefa_sucessora not in visitados:
                    visitados.append(tarefa_sucessora)
                    fila.append(tarefa_sucessora)

        tempo_final: float = time.perf_counter()
        self.tempo_execucao = tempo_final - tempo_inicial

    def imprimir_maquinas(self):
        for i, m in enumerate(self.maquinas):
            print(f'Maquina {i+1}:', end=' ')
            for t in m.tarefas:
                print(f'{t+1}', end=',')
            print()

    def calcular_FO(self):
        maior_FO = 0
        for m in self.maquinas:
            FO_da_maquina = 0
            for t in m.tarefas:
                FO_da_maquina += self.tarefas[t]

            if FO_da_maquina > maior_FO:
                maior_FO = FO_da_maquina

        return maior_FO

    def imprimir_solucao(self):
        self.imprimir_maquinas()
        print(f'FO: {self.calcular_FO()}')

    def imprimir_tempo_segundos(self):
        print(str(self.tempo_execucao) + ' segundos')

    def salvar_solucao(self):
        with open(NOME_ARQUIVO_SOLUCAO, 'w+') as arquivo_solucao:
            stdout_original = sys.stdout
            sys.stdout = arquivo_solucao
            self.imprimir_solucao()
            self.imprimir_tempo_segundos()
            sys.stdout = stdout_original
