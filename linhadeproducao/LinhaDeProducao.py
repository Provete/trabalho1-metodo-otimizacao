from linhadeproducao.Maquina import Maquina
import math
import sys
import time
import random
import copy

NOME_ARQUIVO_SOLUCAO = 'solução.txt'


class LinhaDeProducao:
    tarefas: list[int]
    lista_predecessao: list[tuple[int, int]]
    grafo_precedencia_tarefas: list[list[bool]]
    digrafo_precedencia_tarefas: list[list[bool]]
    tempo_execucao: float
    maquinas: list[Maquina]
    quantidade_tarefas: int

    def __init__(self, nome_arquivo: str, numero_maquinas: int, tarefa_inicial: int):
        self.maquinas = list()
        self.tempo_execucao = 0
        self.tarefas = list()
        self.grafo_precedencia_tarefas = list()
        self.digrafo_precedencia_tarefas = list()
        self.lista_predecessao = list()
        self.quantidade_tarefas = 0
        self.ler_arquivo(nome_arquivo)
        self.inicializar_maquinas(numero_maquinas)
        self.criar_solucao_inicial_BFS(tarefa_inicial)

    def inicializar_maquinas(self, numero_maquinas: int):
        tarefas_por_maquina: int = int(math.floor(self.quantidade_tarefas / numero_maquinas))
        restante: int = self.quantidade_tarefas % numero_maquinas
        index_ultima_maquina: int = numero_maquinas - 1

        for i in range(0, index_ultima_maquina):
            nova_maquina: Maquina = Maquina(tarefas_por_maquina)
            self.maquinas.append(nova_maquina)

        ultima_maquina: Maquina = Maquina(tarefas_por_maquina + restante)
        self.maquinas.append(ultima_maquina)

    def ler_arquivo(self, nome_arquivo: str):

        with open(nome_arquivo, 'r') as arquivo:
            self.quantidade_tarefas: int = int(arquivo.readline())
            quantidade_tarefas = self.quantidade_tarefas

            for i in range(0, quantidade_tarefas):
                custo_tarefa = int(arquivo.readline())
                self.tarefas.append(custo_tarefa)

                self.grafo_precedencia_tarefas.append([False] * quantidade_tarefas)
                self.digrafo_precedencia_tarefas.append([False] * quantidade_tarefas)

            for l in arquivo:
                predecessor, sucessor = l.split(',')
                predecessor = int(predecessor) - 1
                sucessor = int(sucessor) - 1

                if predecessor == -2 or sucessor == -2:
                    continue
                self.grafo_precedencia_tarefas[predecessor][sucessor] = True
                self.digrafo_precedencia_tarefas[predecessor][sucessor] = True

                self.grafo_precedencia_tarefas[sucessor][predecessor] = True
                self.lista_predecessao.append((predecessor, sucessor))

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

    def adicionar_tarefas_antecessoras(self, tarefa: int, fila: list[int]):
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
        self.tempo_inicial: float = time.perf_counter()

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

    def imprimir_maquinas(self):
        for i, m in enumerate(self.maquinas):
            print(f'Maquina {i}:', end=' ')
            for t in m.tarefas:
                print(f'{t}', end=',')
            print()

    def pegar_maior_FO(self):
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
        print(f'FO: {self.pegar_maior_FO()}')

    def imprimir_tempo_segundos(self):
        print(str(self.tempo_execucao) + ' segundos')

    def calcular_FO(self, index_maquina: int) -> int:
        FO: int = 0
        for tarefa in self.maquinas[index_maquina].tarefas:
            FO += self.tarefas[tarefa]
        return FO

    def pegar_index_maquina_maior_FO(self) -> int:
        index_maquina_maior_FO: int = 0
        maior_FO: int = self.calcular_FO(index_maquina_maior_FO)

        for i in range(len(self.maquinas)):
            maquina_FO: int = self.calcular_FO(i)

            if maior_FO < maquina_FO:
                index_maquina_maior_FO = i
                maior_FO = maquina_FO

        return index_maquina_maior_FO

    def pegar_index_maquina_menor_FO(self, index_maquinas: list[int] = None) -> int:
        if index_maquinas is None:
            index_maquinas = list(range(len(self.maquinas)))

        index_maquina_menor_FO: int = index_maquinas.pop()
        menor_FO: int = self.calcular_FO(index_maquina_menor_FO)

        for i in index_maquinas:
            maquina_FO: int = self.calcular_FO(i)

            if menor_FO > maquina_FO:
                index_maquina_menor_FO = i
                menor_FO = maquina_FO

        return index_maquina_menor_FO

    def pegar_tarefas_adjacentes(self, tarefa) -> set[int]:
        tarefas_adjacentes = set()

        for i, possui_adjacencia in enumerate(self.grafo_precedencia_tarefas[tarefa]):
            if possui_adjacencia:
                tarefas_adjacentes.add(i)

        return tarefas_adjacentes

    def pegar_index_maquinas_adjacentes(self, index_maquina) -> list[int]:
        maquinas_adjacente: list[int] = list()

        for tarefa in self.maquinas[index_maquina].tarefas:
            tarefas_adjacentes: set[int] = self.pegar_tarefas_adjacentes(tarefa)
            tarefas_adjacentes = tarefas_adjacentes - set(self.maquinas[index_maquina].tarefas)

            for tarefa_adjacente in tarefas_adjacentes:
                for i in range(len(self.maquinas)):
                    if i == index_maquina:
                        continue
                    if i in maquinas_adjacente:
                        continue

                    if tarefa_adjacente in self.maquinas[i].tarefas:
                        maquinas_adjacente.append(i)

        return list(maquinas_adjacente)

    def pegar_index_maquina_adjacente_menor_FO(self, index_maquina) -> int:
        maquinas_adjacente: list[int] = self.pegar_index_maquinas_adjacentes(index_maquina)
        return self.pegar_index_maquina_menor_FO(maquinas_adjacente)

    def pegar_tarefas_sucessoras_entre_maquinas(self, index_maquina_fonte: int, index_maquina_destino) -> list[int]:
        tarefas_sucessoras = list()

        for tarefa_fonte in self.maquinas[index_maquina_fonte].tarefas:
            tarefas_sucessoras_a_fonte = self.pegar_tarefas_sucessoras(tarefa_fonte)

            for tarefa_sucessora_a_fonte in tarefas_sucessoras_a_fonte:
                if tarefa_sucessora_a_fonte in self.maquinas[
                    index_maquina_destino].tarefas and tarefa_sucessora_a_fonte not in tarefas_sucessoras:
                    tarefas_sucessoras.append(tarefa_sucessora_a_fonte)

        return tarefas_sucessoras

    def pegar_tarefa_maior_custo(self, tarefas: list[int]) -> int:
        tarefa_maior_custo: int = tarefas.pop()

        for tarefa in tarefas:
            if self.tarefas[tarefa_maior_custo] < self.tarefas[tarefa]:
                tarefa_maior_custo = tarefa

        return tarefa_maior_custo

    def salvar_solucao(self):
        with open(NOME_ARQUIVO_SOLUCAO, 'w+') as arquivo_solucao:
            stdout_original = sys.stdout
            sys.stdout = arquivo_solucao
            self.imprimir_solucao()
            self.imprimir_tempo_segundos()
            sys.stdout = stdout_original

    def esta_precedencias_respeitada(self) -> bool:
        for predecessor, sucessor in self.lista_predecessao:
            index_maquina_predecessor: int = 0
            index_maquina_sucessor: int = 0

            for i in range(len(self.maquinas)):
                if predecessor in self.maquinas[i].tarefas:
                    index_maquina_predecessor = i
                if sucessor in self.maquinas[i].tarefas:
                    index_maquina_sucessor = i

            if index_maquina_predecessor > index_maquina_sucessor:
                return False
        return True

    def doar_tarefa(self, index_doador, index_recebedor, tarefa):
        self.maquinas[index_doador].remover_tarefa(tarefa)
        self.maquinas[index_recebedor].forcar_adicionar_tarefa(tarefa)

    def refinar_solucao(self, numero_iteracoes: int) -> None:

        if numero_iteracoes <= 0:
            print("Erro: Numero de iterações menor ou igual a zero")
            return

        for i in range(numero_iteracoes):
            FO_anterior: int = self.pegar_maior_FO()

            index_maquina_maior_FO = self.pegar_index_maquina_maior_FO()
            index_maquinas_adjacentes = self.pegar_index_maquinas_adjacentes(index_maquina_maior_FO)

            for index_maquina_adjacente in index_maquinas_adjacentes:
                bandeira_mudanca_legal = False

                tarefas_adjacentes_na_maquina_maior_FO = self.pegar_tarefas_sucessoras_entre_maquinas(
                    index_maquina_adjacente, index_maquina_maior_FO)

                if not tarefas_adjacentes_na_maquina_maior_FO:
                    temp = index_maquina_adjacente
                    index_maquina_adjacente = index_maquina_maior_FO
                    index_maquina_maior_FO = temp

                    tarefas_adjacentes_na_maquina_maior_FO = self.pegar_tarefas_sucessoras_entre_maquinas(
                        index_maquina_adjacente, index_maquina_maior_FO)
                    for tarefa in tarefas_adjacentes_na_maquina_maior_FO:
                        self.doar_tarefa(index_maquina_maior_FO, index_maquina_adjacente, tarefa)
                        FO_nova = self.pegar_maior_FO()

                        if not self.esta_precedencias_respeitada() or FO_nova > FO_anterior:
                            self.doar_tarefa(index_maquina_adjacente, index_maquina_maior_FO, tarefa)
                        else:
                            bandeira_mudanca_legal = True
                            break

                    if bandeira_mudanca_legal:
                        break
                else:
                    for tarefa in tarefas_adjacentes_na_maquina_maior_FO:
                        self.doar_tarefa(index_maquina_maior_FO, index_maquina_adjacente, tarefa)
                        FO_nova = self.pegar_maior_FO()

                        if not self.esta_precedencias_respeitada() or FO_nova > FO_anterior:
                            self.doar_tarefa(index_maquina_adjacente, index_maquina_maior_FO, tarefa)
                        else:
                            bandeira_mudanca_legal = True
                            break

                    if bandeira_mudanca_legal:
                        break
        tempo_final = time.perf_counter()
        self.tempo_execucao = tempo_final - self.tempo_inicial

    def perturbar_solucao(self, maximo_iteracoes):
        index_maquina_aleatoria: int = random.randrange(0, stop=len(self.maquinas), step=1)
        index_maquinas_adjacentes: list[int] = self.pegar_index_maquinas_adjacentes(index_maquina_aleatoria)

        index_maquina_adjacente_aleatoria: int = random.choice(index_maquinas_adjacentes)

        tarefas_adjascentes_maquina_escolhida = self.pegar_tarefas_sucessoras_entre_maquinas(
            index_maquina_adjacente_aleatoria, index_maquina_aleatoria)

        for i in range(maximo_iteracoes):
            if not tarefas_adjascentes_maquina_escolhida:
                temp = index_maquina_aleatoria
                index_maquina_aleatoria = index_maquina_adjacente_aleatoria
                index_maquina_adjacente_aleatoria = temp

                tarefas_adjascentes_maquina_escolhida = self.pegar_tarefas_sucessoras_entre_maquinas(
                    index_maquina_adjacente_aleatoria, index_maquina_aleatoria)

                for tarefa in tarefas_adjascentes_maquina_escolhida:
                    self.doar_tarefa(index_maquina_aleatoria, index_maquina_adjacente_aleatoria, tarefa)

                    if not self.esta_precedencias_respeitada() or len(
                            self.maquinas[index_maquina_aleatoria].tarefas) == 0:
                        self.doar_tarefa(index_maquina_adjacente_aleatoria, index_maquina_aleatoria, tarefa)
                    else:
                        return

            else:
                for tarefa in tarefas_adjascentes_maquina_escolhida:
                    self.doar_tarefa(index_maquina_aleatoria, index_maquina_adjacente_aleatoria, tarefa)

                    if not self.esta_precedencias_respeitada() or len(
                            self.maquinas[index_maquina_aleatoria].tarefas) == 0:
                        self.doar_tarefa(index_maquina_adjacente_aleatoria, index_maquina_aleatoria, tarefa)
                    else:
                        return

    def calcular_FO_solucao(self, lista_maquinas: list[Maquina]):
        maior_FO = 0
        for m in lista_maquinas:
            FO_da_maquina = 0
            for t in m.tarefas:
                FO_da_maquina += self.tarefas[t]

            if FO_da_maquina > maior_FO:
                maior_FO = FO_da_maquina

        return maior_FO

    def simulated_annealling(self, divisor_temperatura, temperatura_inicial, temperatura_controle,
                             iteracoes_por_temperatura):
        tempo_inicial = time.perf_counter()

        melhor_solucao = copy.deepcopy(self.maquinas)
        temperatura_corrente = temperatura_inicial

        while temperatura_corrente >= temperatura_controle:
            for i in range(iteracoes_por_temperatura):
                solucao_inicial = copy.deepcopy(self.maquinas)
                self.perturbar_solucao(12)

                FO_inicial = self.calcular_FO_solucao(solucao_inicial)
                FO_perturbada = self.pegar_maior_FO()
                FO_melhor_solucao = self.calcular_FO_solucao(melhor_solucao)
                variacao = FO_perturbada - FO_inicial

                if variacao < 0:
                    if FO_perturbada < FO_melhor_solucao:
                        melhor_solucao = copy.deepcopy(self.maquinas)
                else:
                    valor_aleatorio = random.random()
                    if valor_aleatorio > math.exp((-variacao) / temperatura_corrente):
                        self.maquinas = solucao_inicial

            temperatura_corrente /= divisor_temperatura

        self.maquinas = melhor_solucao

        tempo_final = time.perf_counter()
        self.tempo_execucao = tempo_final - tempo_inicial
