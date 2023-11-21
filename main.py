from linhadeproducao.LinhaDeProducao import LinhaDeProducao
import sys

#feito por: Gustavo Provete de Andrade

if __name__ == '__main__':
    LP: LinhaDeProducao = LinhaDeProducao(sys.argv[1], 6, 0)
    LP.imprimir_solucao()
    LP.imprimir_tempo_segundos()
    if LP.esta_precedencias_respeitada():
        LP.salvar_solucao()

