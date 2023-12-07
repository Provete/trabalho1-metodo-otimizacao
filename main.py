from linhadeproducao.LinhaDeProducao import LinhaDeProducao
import sys

#feito por: Gustavo Provete de Andrade

if __name__ == '__main__':
    NOME_ARQUIVO: str = sys.argv[1]
    NUMERO_MAQUINAS: int = 6
    TAREFA_INICIAL: int = 0

    LP: LinhaDeProducao = LinhaDeProducao(NOME_ARQUIVO, NUMERO_MAQUINAS, TAREFA_INICIAL)
    LP.imprimir_solucao()
    LP.imprimir_tempo_segundos()
    if LP.esta_precedencias_respeitada():
        LP.salvar_solucao()

