from linhadeproducao.Maquina import Maquina

class LinhaDeProducao:
    tarefas: list[int]
    grafo_precedencia_tarefas: list[list[int]]
    maquinas: list[Maquina]

    def __init__(self, nome_arquivo: str):
        self.maquinas = list()
        self.ler_arquivo(nome_arquivo)

    def ler_arquivo(self, nome_arquivo: str):
        custo_tarefas: list[int] = list()
        grafo_precedencia_tarefas: list[list[bool]] = list()

        with open(nome_arquivo, 'r') as arquivo:
            quantidade_tarefas: int = int(arquivo.readline())

            for i in range(0, quantidade_tarefas):
                custo_tarefa = int(arquivo.readline())
                custo_tarefas.append(custo_tarefa)

                grafo_precedencia_tarefas.append( [False]*quantidade_tarefas )

            for l in arquivo:
                predecessor, sucessor = l.split(',')
                predecessor = int(predecessor)
                sucessor = int(sucessor)

                grafo_precedencia_tarefas[predecessor-1][sucessor-1] = True

        self.grafo_precedencia_tarefas = grafo_precedencia_tarefas
        self.tarefas = custo_tarefas

    def imprimir_grafo(self):
        for l in self.grafo_precedencia_tarefas:
            for v in l:
                print(f'{int(v)} ', end=' ')
            print()
