class LinhaDeProducao:
    custo_das_tarefas: list[float]
    grafo_precedencia_tarefas: list[list[int]]

    def __init__(self, nome_arquivo: str):
        pass

    def ler_arquivo(self, nome_arquivo: str):
        custo_tarefas: list[float] = list()
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
