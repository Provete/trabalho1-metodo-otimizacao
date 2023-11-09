from linhadeproducao.LinhaDeProducao import LinhaDeProducao
import sys

#feito por: Gustavo Provete de Andrade

if __name__ == '__main__':
    if(len(sys.argv) == 4):
        LP: LinhaDeProducao = LinhaDeProducao(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
        LP.imprimir_solucao()
        LP.imprimir_tempo_segundos()
        LP.salvar_solucao()
    else:
        print('Parametros de linha de comando invalidos. Favor passar 3 argumentos por linha de comando: nome do arquivo, quantidade de '
              'maquinas e tarefa inicial')


