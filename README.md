# Servidor Chatbot com Desafio de Adivinhação: IA ou Humano?

Este projeto tem como objetivo a implementação de um servidor que integra um chatbot de inteligência artificial para responder a perguntas enviadas por um cliente via sockets TCP.
O cliente pode enviar perguntas e receber respostas tanto do chatbot quanto de um ser humano. O objetivo do cliente é adivinhar se a resposta retornada foi gerada por uma inteligência artificial ou por uma pessoa, desta forma, criando uma interação do servidor com o cliente.

## Como iniciar o projeto
Siga os passos abaixo para clonar o repositório e executar o servidor e o cliente:
1. ### Clonar o repositório:
   Abra o terminal e execute o seguinte comando para clonar o repositório em um diretório de sua escolha:
   ```sh
   git clone
   ```
2. ### Acessar o diretório do projeto:
   Após clonar o repositório, entre no diretório do projeto:
   ```sh
   cd nome-do-diretorio
   ```
3. ### Dividir o terminal para rodar o servidor e o cliente:
   Divida o terminal em múltiplas abas para rodar o servidor e o cliente simultaneamente. Abra duas abas ou divida o terminal em dois.
   
4. ### Executando o servidor:
   No primeiro terminal, execute primeiramente o seguinte comando: 
   ```sh
   python server.py
   ```
   Apos executar o comando, o servidor pedirá para você fornecer alguns dados, como escolha do modo de operação.
   
5. ### Executando o cliente:
   Depois que o servidor estiver em execução, vá para o segundo terminal e execute o seguinte comando para iniciar o cliente:
    ```sh
   python client.py
   ```
    Após executar o comando, o cliente pedirá para você fornecer alguns dados de identificação, como o nome de usuário, e depois permitirá que você envie perguntas ao servidor para receber as respostas.

6. ### Encerrando a conexão
   - No Cliente: Digite "sair" e feche o terminal
   - No servidor: Feche o terminal 
