import socket
import threading
import http.client
import json

HOST = '127.0.0.1' 
PORT = 20000
MODE = None
DELAY = None
HISTORICO = []
USUARIOS = {}

def iniciar_servidor():
    global MODE, DELAY
    MODE, DELAY = obter_modo_servidor()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("\nServidor iniciado e aguardando conexões...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print("Conexão estabelecida com {}".format(addr))
            thread = threading.Thread(target=interagindo_cliente, args=(client_socket,))
            thread.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado manualmente.")
    finally:
        server_socket.close()

def obter_modo_servidor():
    print("Selecione o modo de operação:")
    print("1 - Automático (respostas sempre da IA)")
    print("2 - Controlado (escolha entre IA ou humano a cada pergunta)")
    mode = input("Escolha 1 ou 2: ")

    if mode not in ['1', '2']:
        mode = '1'

    delay = input("Defina o tempo de espera para respostas automáticas (em segundos): ")
    try:
        delay = int(delay)
    except ValueError:
        print("Entrada inválida! Usando 2 segundos como padrão.")
        delay = 2

    return mode, delay

def interagindo_cliente(client_socket):
    global MODE, DELAY, HISTORICO, USUARIOS

    try:
        nome_usuario = client_socket.recv(1024).decode('utf-8')
        print(f"Usuário conectado: {nome_usuario}")
        if nome_usuario not in USUARIOS:
            USUARIOS[nome_usuario] = {'total': 0, 'acertos': 0}

        while True:
            try:
                pergunta = client_socket.recv(4096).decode('utf-8')

                print(f"Recebendo pergunta do cliente: {pergunta}")

                if MODE == '1':  
                    origem_resposta = 'ia'
                    resposta = gerar_resposta_ia(pergunta)
                    print(f"Resposta gerada pela IA: {resposta}")
                else: 
                    escolha = input("Quem irá responder a proxima pergunta: 'ia' ou 'humano'")
                    origem_resposta = escolha

                    if origem_resposta == 'ia':
                        resposta = gerar_resposta_ia(pergunta)
                        print(f"Resposta gerada pela IA: {resposta}")
                    else:
                        print(f"\nPergunta do usuário {nome_usuario}: {pergunta}")
                        resposta = input("Digite a resposta humana: ")
                        print(f"Resposta enviada manualmente: {resposta}")

                print(f"Enviando resposta para o cliente: {resposta} (Origem: {origem_resposta})")
                client_socket.send(f"{resposta}|{origem_resposta}".encode('utf-8'))

                acertou = False 
                salvar_historico(nome_usuario, pergunta, resposta, origem_resposta, acertou)

            except Exception as e:
                print(f"Erro durante o processamento da pergunta: {e}")
                break

    except Exception as e:
        print(f"Erro ao lidar com o cliente: {e}")
    finally:
        client_socket.close()
        print(f"Conexão com {nome_usuario} encerrada.")

def gerar_resposta_ia(pergunta):
    try:
        conn = http.client.HTTPSConnection("chatgpt-42.p.rapidapi.com") 

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": pergunta
                }
            ],
            "web_access": False
        })

        headers = {
            'x-rapidapi-key': "7e7a22e58fmsh1f2c7eb99a94696p160deajsnd29e933bcd82",#"f901e15523msh5061a69d622dfa1p1c9355jsn8611b192bc15",chave ivyna #
            'x-rapidapi-host': "chatgpt-42.p.rapidapi.com",
            'Content-Type': "application/json"
        }

        conn.request("POST", "/chatgpt", payload, headers)
        res = conn.getresponse()
        data = res.read()

        
        print(f"Resposta bruta da API: {data.decode('utf-8')}")

        try:
            response_json = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar o JSON: {e}")
            return "Erro ao decodificar a resposta da IA."

        if isinstance(response_json, dict) and 'result' in response_json:
            return response_json.get('result', 'Sem resposta disponível')
        else:
            print(f"Formato inesperado da resposta da API: {response_json}")
            return "Formato de resposta inesperado da API."

    except Exception as e:
        print(f"Erro ao conectar com a API: {e}")
        return "Erro ao obter resposta da IA."

def salvar_historico(usuario, pergunta, resposta, origem_resposta, acertou):
    registro = {
        'usuario': usuario,
        'pergunta': pergunta,
        'resposta': resposta,
        'origem_resposta': origem_resposta,
        'acertou': acertou
    }
    HISTORICO.append(registro)
    with open('historico_respostas.txt', 'a', encoding='utf-8') as file:
        file.write("{}\n".format(registro))

if __name__ == "__main__":
    iniciar_servidor()