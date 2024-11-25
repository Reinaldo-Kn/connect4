import socket
import sys


class Connect4:
    def __init__(self):
        self.tabuleiro = [[' ' for _ in range(7)] for _ in range(6)]  
        self.jogador_atual = 'X'  

    def resetar_tabuleiro(self):
        """
        Reseta o tabuleiro para uma nova partida
        """
        self.tabuleiro = [[' ' for _ in range(7)] for _ in range(6)]

    def mostrar_tabuleiro(self):
        """
        Exibe o tabuleiro no terminal do servidor para depuração
        """
        print("***************************")
        for linha in self.tabuleiro:
            print('|'.join(linha))
            print('-' * 15)  

    def formatar_tabuleiro(self):
        """
        Formata o tabuleiro para exibição no terminal dos jogadores
        """
        
        indices_colunas = '   '.join(map(str, range(7)))
        linhas_formatadas = [f"  {indices_colunas}"]  

        for linha in self.tabuleiro:
            linhas_formatadas.append('| ' + ' | '.join(linha) + ' |')
            linhas_formatadas.append('+---' * 7 + '+')  

        return '\n'.join(linhas_formatadas)

    def fazer_jogada(self, coluna, simbolo):
        """
        Realiza a jogada em uma coluna específica.
        """
        if coluna < 0 or coluna >= 7 or self.tabuleiro[0][coluna] != ' ':
            return False
        for i in range(5, -1, -1):
            if self.tabuleiro[i][coluna] == ' ':
                self.tabuleiro[i][coluna] = simbolo
                return i, coluna
        return False

    def checar_vitoria(self, linha, coluna):
        """
        Verifica se o jogador atual venceu após fazer uma jogada na posição (linha, coluna).
        """
        simbolo = self.tabuleiro[linha][coluna]
        direcoes = [(1, 0), (0, 1), (1, 1), (1, -1)]  
        for direcao in direcoes:
            count = 1
            for i in range(1, 4):
                r = linha + direcao[0] * i
                c = coluna + direcao[1] * i
                if 0 <= r < 6 and 0 <= c < 7 and self.tabuleiro[r][c] == simbolo:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r = linha - direcao[0] * i
                c = coluna - direcao[1] * i
                if 0 <= r < 6 and 0 <= c < 7 and self.tabuleiro[r][c] == simbolo:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False


def jogar_denovo(jogador1, jogador2):
    """
    Pergunta para ambos os jogadores se querem jogar novamente.
    """

    jogador1.send("Deseja jogar novamente? (s/n): ".encode())
    resposta1 = jogador1.recv(1).decode().strip().lower()

    jogador2.send("Deseja jogar novamente? (s/n): ".encode())
    resposta2 = jogador2.recv(1).decode().strip().lower()

    return resposta1 == 's' and resposta2 == 's'


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endereco = ('127.0.0.1', 50000)
    servidor.bind(endereco)
    servidor.listen(2)

    print('Aguardando jogador 1...')
    jogador1, _ = servidor.accept()
    print('Jogador 1 conectado.')

    print('Aguardando jogador 2...')
    jogador2, _ = servidor.accept()
    print('Jogador 2 conectado.')

    jogo = Connect4()
    score_jogador1 = 0
    score_jogador2 = 0
    while True:
        while True:
            jogador1.send('Sua vez, jogador 1 (X). Escolha uma coluna (0-6): '.encode())
            coluna = int(jogador1.recv(1).decode())

            while True:
                resultado = jogo.fazer_jogada(coluna, 'X')
                if not resultado:
                    jogador1.send('Jogada inválida, tente novamente.\n'.encode())
                    coluna = int(jogador1.recv(1).decode())
                else:
                    linha, coluna = resultado
                    break

            tabuleiro_formatado = jogo.formatar_tabuleiro()
            jogador1.send("***************************\n".encode())
            jogador1.send(f"{tabuleiro_formatado}\n\n".encode())
            jogador2.send("***************************\n".encode())
            jogador2.send(f"{tabuleiro_formatado}\n\n".encode())

            if jogo.checar_vitoria(linha, coluna):
                score_jogador1 += 1 
                placar = f"Placar atual:\nJogador 1 (X): {score_jogador1} vitória(s)\nJogador 2 (O): {score_jogador2} vitória(s)\n"
                jogador1.send(placar.encode())
                jogador2.send(placar.encode())
                jogador1.send('Você venceu!\n'.encode())
                jogador2.send('Você perdeu! Jogador 1 venceu!\n'.encode())
                break

            jogador2.send('Sua vez, jogador 2 (O). Escolha uma coluna (0-6): '.encode())
            coluna = int(jogador2.recv(1).decode())

            while True:
                resultado = jogo.fazer_jogada(coluna, 'O')
                if not resultado:
                    jogador2.send('Jogada inválida, tente novamente.\n'.encode())
                    coluna = int(jogador2.recv(1).decode())
                else:
                    linha, coluna = resultado
                    break

            tabuleiro_formatado = jogo.formatar_tabuleiro()
            jogador1.send("***************************\n".encode())
            jogador1.send(f"{tabuleiro_formatado}\n\n".encode())
            jogador2.send("***************************\n".encode())
            jogador2.send(f"{tabuleiro_formatado}\n\n".encode())

            if jogo.checar_vitoria(linha, coluna):
                score_jogador2 += 1
                placar = f"Placar atual:\nJogador 1 (X): {score_jogador1} vitória(s)\nJogador 2 (O): {score_jogador2} vitória(s)\n"
                jogador1.send(placar.encode())
                jogador2.send(placar.encode())
                jogador2.send('Você venceu!\n'.encode())
                jogador1.send('Você perdeu! Jogador 2 venceu!\n'.encode())
                break

        if not jogar_denovo(jogador1, jogador2):
            jogador1.send("Obrigado por jogar!\n".encode())
            jogador2.send("Obrigado por jogar!\n".encode())
            break

        jogo.resetar_tabuleiro()


if __name__ == '__main__':
    main()
