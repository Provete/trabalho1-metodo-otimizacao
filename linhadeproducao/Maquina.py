class Maquina:
    def __init__(self, maximo_tarefas: int):
        self.tarefas: set[int] = set()
        self.maximo_tarefas: int = maximo_tarefas

    tarefas: set[int]
    maximo_tarefas: int

    def adicionar_tarefa(self, tarefa: int):
        if len(self.tarefas) <= self.maximo_tarefas:
            self.tarefas.add(tarefa)

    def pode_adicionar_tarefa(self):
        return len(self.tarefas) <= self.maximo_tarefas
