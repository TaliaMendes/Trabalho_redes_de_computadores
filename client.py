import socket

HOST = '127.0.0.1' 
PORT = 30000

def iniciar_cliente():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT)) 

    acertos = 0 
    erros = 0

    nome = input("Digite seu nome: ")
    client_socket.send(nome.encode('utf-8'))
    print(f"Bem-vindo, {nome}!")
    
    while True:
        pergunta = input("Digite sua pergunta (ou 'sair' para encerrar): ")
        
        if pergunta.lower() == 'sair':
            break

        print(f"Enviando pergunta para o servidor: {pergunta}")
        client_socket.send(pergunta.encode('utf-8'))

        try:
            resposta_completa = client_socket.recv(4096).decode('utf-8')
            resposta, origem_resposta = resposta_completa.split('|')
            print(f"Resposta do servidor: {resposta}")

            chute = input("Você acha que a resposta foi de um humano ou IA? (h/ia): ")

            if chute.lower() == "h" and origem_resposta == "humano":
                acertou = "Acertou"
            elif chute.lower() == "ia" and origem_resposta == "ia":
                acertou = "Acertou"
            else:
                acertou = "Errou"

            print(acertou)

            if "Acertou" in acertou:
                acertos += 1
            else:
                erros += 1

            print("\n------ Quantidade de erros e acertos de Palpites ---------")
            print(f"Total de acertos: {acertos}")
            print(f"Total de erros: {erros}")

            # Enviar o feedback para o servidor (Acertou ou Errou)
            client_socket.send(acertou.encode('utf-8'))

        except Exception as e:
            print(f"Erro ao receber resposta do servidor: {e}")

    client_socket.close()

if __name__ == "__main__":
    iniciar_cliente()
