import socket
import sys

class Connect4:
    def __init__(self):
        self.tabuleiro = [[' ' for _ in range(7)] for _ in range(6)]  # 6x7 tabuleiro
        self.jogador_atual = 'X'  # Jogador 'X' começa

    def mostrar_tabuleiro(self):
        """
        Exibe o tabuleiro formatado com índices de colunas.
        """
        print("***************************")
        print("  ".join(str(i) for i in range(7)))  # Índices das colunas
        for linha in self.tabuleiro:
            print('|'.join(linha))
            print('-' * 13)

    def formatar_tabuleiro(self):
        """
        Retorna o tabuleiro formatado como string para envio aos jogadores.
        """
        linhas_formatadas = []
        linhas_formatadas.append("  ".join(str(i) for i in range(7)))  # Índices das colunas
        for linha in self.tabuleiro:
            linhas_formatadas.append('|'.join(linha))
            linhas_formatadas.append('-' * 13)
        return '\n'.join(linhas_formatadas)

    def fazer_jogada(self, coluna):
        """
        Faz a jogada na coluna escolhida.
        """
        if coluna < 0 or coluna >= 7 or self.tabuleiro[0][coluna] != ' ':
            return False
        for i in range(5, -1, -1):
            if self.tabuleiro[i][coluna] == ' ':
                self.tabuleiro[i][coluna] = self.jogador_atual
                return i, coluna
        return False

    def checar_vitoria(self, linha, coluna):
        """
        Verifica se o jogador atual venceu a partir da posição fornecida.
        """
        direcoes = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Verticais, horizontais e diagonais
        for direcao in direcoes:
            count = 1
            for i in range(1, 4):
                r = linha + direcao[0] * i
                c = coluna + direcao[1] * i
                if 0 <= r < 6 and 0 <= c < 7 and self.tabuleiro[r][c] == self.jogador_atual:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r = linha - direcao[0] * i
                c = coluna - direcao[1] * i
                if 0 <= r < 6 and 0 <= c < 7 and self.tabuleiro[r][c] == self.jogador_atual:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

    def trocar_jogador(self):
        """
        Alterna entre os jogadores.
        """
        self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'

    def resetar_tabuleiro(self):
        """
        Reseta o tabuleiro para uma nova partida.
        """
        self.tabuleiro = [[' ' for _ in range(7)] for _ in range(6)]
        self.jogador_atual = 'X'


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endereco = ('127.0.0.1', 50000)
    servidor.bind(endereco)
    servidor.listen(2)

    print('Aguardando jogadores...')
    jogador1, _ = servidor.accept()
    print('Jogador 1 conectado.')

    jogador2, _ = servidor.accept()
    print('Jogador 2 conectado.')

    jogo = Connect4()

    # Variáveis de pontuação
    score_jogador1 = 0
    score_jogador2 = 0

    while True:
        # Loop da partida
        while True:
            # Turno do Jogador 1
            jogador1.send('Sua vez, jogador 1 (X). Escolha uma coluna (0-6): '.encode())
            coluna = int(jogador1.recv(1).decode())

            while True:
                resultado = jogo.fazer_jogada(coluna)
                if not resultado:
                    jogador1.send('Jogada inválida, tente novamente.\n'.encode())
                    coluna = int(jogador1.recv(1).decode())
                else:
                    linha, coluna = resultado
                    break

            tabuleiro_formatado = jogo.formatar_tabuleiro()
            jogador1.send(f"***************************\n{tabuleiro_formatado}\n".encode())
            jogador2.send(f"***************************\n{tabuleiro_formatado}\n".encode())

            if jogo.checar_vitoria(linha, coluna):
                score_jogador1 += 1  # Incrementa a pontuação do jogador 1
                jogador1.send('Você venceu!\n'.encode())
                jogador2.send('Você perdeu! Jogador 1 venceu!\n'.encode())
                break

            # Turno do Jogador 2
            jogador2.send('Sua vez, jogador 2 (O). Escolha uma coluna (0-6): '.encode())
            coluna = int(jogador2.recv(1).decode())

            while True:
                resultado = jogo.fazer_jogada(coluna)
                if not resultado:
                    jogador2.send('Jogada inválida, tente novamente.\n'.encode())
                    coluna = int(jogador2.recv(1).decode())
                else:
                    linha, coluna = resultado
                    break

            tabuleiro_formatado = jogo.formatar_tabuleiro()
            jogador1.send(f"***************************\n{tabuleiro_formatado}\n".encode())
            jogador2.send(f"***************************\n{tabuleiro_formatado}\n".encode())

            if jogo.checar_vitoria(linha, coluna):
                score_jogador2 += 1  # Incrementa a pontuação do jogador 2
                jogador2.send('Você venceu!\n'.encode())
                jogador1.send('Você perdeu! Jogador 2 venceu!\n'.encode())
                break

            jogo.trocar_jogador()

        # Exibe o placar ao final da partida
        placar = f"Placar atual:\nJogador 1 (X): {score_jogador1} vitória(s)\nJogador 2 (O): {score_jogador2} vitória(s)\n"
        jogador1.send(placar.encode())
        jogador2.send(placar.encode())

        # Pergunta se desejam jogar novamente
        jogador1.send("Deseja jogar novamente? (s/n): ".encode())
        jogador2.send("Deseja jogar novamente? (s/n): ".encode())

        resposta1 = jogador1.recv(1).decode().strip().lower()
        resposta2 = jogador2.recv(1).decode().strip().lower()

        if resposta1 == 's' and resposta2 == 's':
            jogo.resetar_tabuleiro()
            continue
        else:
            jogador1.send("Obrigado por jogar! Saindo...\n".encode())
            jogador2.send("Obrigado por jogar! Saindo...\n".encode())
            break

    servidor.close()


if __name__ == '__main__':
    main()
