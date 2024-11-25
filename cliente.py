import socket

def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endereco = ('127.0.0.1', 50000)
    
    try:
        cliente.connect(endereco)
        print("Conectado ao servidor!")
        
        while True:
            mensagem = cliente.recv(1024).decode() 
            print(mensagem)  
            
            if "Deseja jogar novamente?" in mensagem:
                resposta = input("Digite 's' para sim ou 'n' para não: ").strip().lower()
                while resposta not in ['s', 'n']:
                    resposta = input("Resposta inválida. Digite 's' para sim ou 'n' para não: ").strip().lower()
                cliente.send(resposta.encode())  # Envia a resposta ao servidor
                if resposta == 'n':  
                    print("Você escolheu não jogar novamente. Encerrando...")
                    break
            elif "Obrigado por jogar!" in mensagem:
                print("O jogo foi encerrado pelo servidor.")
                break
            elif "Escolha uma coluna" in mensagem:
                coluna = input("Digite a coluna onde deseja jogar (0-6): ").strip()
                while not coluna.isdigit() or int(coluna) < 0 or int(coluna) > 6:
                    coluna = input("Entrada inválida. Digite um número entre 0 e 6: ").strip()
                cliente.send(coluna.encode())  # Envia a coluna escolhida

    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor. Certifique-se de que ele está rodando.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        cliente.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    main()
