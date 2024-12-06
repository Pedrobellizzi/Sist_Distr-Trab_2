# Chat System Distribuido
   ### Um sistema de chat distribuído desenvolvido em Python utilizando RPC (Remote Procedure Call). Este projeto simula um sistema multiusuário com salas de chat, mensagens públicas e privadas, integrando um binder central para gerenciamento dos serviços.

## Índice
  ### 1.	Visão Geral
  ### 2.	Características do Sistema
  ### 3.	Estrutura do Projeto
  ### 4.	Requisitos
  ### 5.	Execução
  ### 6.	Detalhamento das Funcionalidades
  ### 7.	Exemplo de Uso
 
## Visão Geral
### O Chat System Distribuido é composto por três partes principais:
   #### •	Binder: Responsável por registrar e descobrir os procedimentos remotos disponíveis no servidor.
   #### •	Servidor de Chat (Server): Gerencia as salas, mensagens e usuários conectados.
   #### •	Cliente: Permite que os usuários interajam com o sistema criando salas, enviando mensagens e listando informações.
#### Este sistema foi desenvolvido como parte de um exercício acadêmico para ilustrar conceitos de sistemas distribuídos e RPC.

## Características do Sistema
### Binder
   #### •	Registro de procedimentos remotos (RPC).
   #### •	Descoberta dinâmica de serviços por clientes e servidores.
### Servidor
   #### •	Gerenciamento de múltiplas salas de chat.
   #### •	Controle de usuários únicos.
   #### •	Histórico de mensagens com suporte para broadcast e unicast.
   #### •	Remoção automática de salas inativas.
### Cliente
   #### •	Registro de usuários com usernames únicos.
   #### •	Criação e entrada em salas.
   #### •	Envio de mensagens públicas e privadas.
   #### •	Busca periódica de mensagens.

## Estrutura do Projeto
#### chat_system/

├── binder/

│   ├── binder.py               # Binder RPC server

├── cliente/

│   ├── cliente.py              # Chat client

├── README.md                   # Documentação do projeto

├── server/

│   ├── server.py               # Chat server

├── utils/

│   ├── requisitos.gitignore    # Funções auxiliares e Dependências do Python

├── chat_start.bat              # Script para inicializar o sistema

└── usuarios.json               # Arquivo de usuários

## Requisitos
###   •	Python 3.8+
###   •	Instalar as dependências listadas em requisitos.gitignore:

## Execução
### Inicie o sistema:  
   ./chat_start.bat

### Isso executará o Binder e o Servidor. Eles estarão disponíveis nos seguintes endereços:
   o	Binder: http://localhost:5000
   o	Servidor: http://localhost:8005

### Abrirá também os novos terminais para executar os clientes:
   python cliente/cliente.py

## Detalhamento das Funcionalidades
### Binder
   #### •	Registrar Procedimento:
     ##### o	register_procedure(procedure_name, address, port)
     ##### o	Exemplo: Registra o método criar_sala disponível no servidor.
   #### •	Descobrir Procedimento:
      ##### o	lookup_procedure(procedure_name)
      ##### o	Exemplo: Retorna o endereço e a porta do método remoto enviar_messagem.
      
### Servidor
   #### •	Registrar Usuario:
        ##### o	registrar_usuario(nomeUsuario)
        ##### o	Exemplo: registra um novo usuario quando acessa o chat, verificando se existe nome igual.
   #### •	Criar Sala:
        ##### o	criarSala(nomeSala)
        ##### o	Exemplo: input("Digite o nome da sala: ") = Sala 2; cria uma nova sala com o nome e número digitado.
   #### •	Entrar em Sala:
        ##### o	entrar_sala(nomeUsuario, nomeSala)
        ##### o	Exemplo: entrar_sala("Pedro", "Sala 2") adiciona o usuário "Pedro" à Sala 2.
   #### •	Enviar Mensagem:
        ##### o	enviar_mensagem(nomeUsuario, salaAtual, messagem, destinatario)
        ##### o	Exemplo: Envia mensagens públicas (broadcast) ou privadas (unicast).
   #### •	Listar Salas:
        ##### o	listar_salas()
        ##### o	Exemplo: Retorna todas as salas ativas.
   #### •	Listar Usuarios:
        ##### o	listar_usuarios()
        ##### o	Exemplo: Retorna todos os usuarios conectados na sala atual.
   #### •	Sair da Sala:
        ##### o	sair_da_sala()
        ##### o	Exemplo: sair_da_sala(nomeUsuario) o usuario sai da sala atual e pode criar ou entrar em outra sala.
   #### •	Buscar Mensagens:
        ##### o	receber_mensagens(nomeUsuario, salaAtual)
        ##### o	Exemplo: Periodicamente busca e exibe para o usuario as 50 últimas mensagens da sala atual que ele estiver conectado.
   #### •	Formatar Mensagens:
        ##### o	formatar_mensagens(mensagem)
        ##### o	Exemplo: Todas as mensagens são formatadas de forma que exiba para o usuario a origem, destino e o conteudo da mensagem. O destino pode ser para todos (broadcast) ou privadas (unicast).
        
### Cliente
   #### •	Permite criar salas, entrar em salas, enviar mensagens e listar informações do servidor.
   #### •	Após registrar o usuario será iniciado um primeiro menu com as seguintes opçoes:
          ##### 1) Criar sala - self.criar_sala()
          ##### 2) Entrar em uma sala - self.entrar_na_sala()
          ##### 3) Listar salas - self.listar_salas()
          ##### 4) Encerrar - print( Encerrando...") - break
   #### •	Após o primeiro menu acima será iniciado o segundo menu com as seguintes opçoes:
          ##### 1) Enviar mensagem - self.enviar_mensagem()
          ##### 2) Sair da sala - self.sair_da_sala()
          ##### 3) Listar usuários - self.listar_usuarios()
          ##### 4) Encerrar - print( Encerrando...") - break
       
## Exemplo de Uso
### 1.	Inicie o sistema e execute o cliente:
      #### ./chat_start.bat
           ##### python binder/binder.py
           ##### python server/server.py
  	        ##### python cliente/cliente.py

### 2. Abra novos terminais para executar os clientes:
    #### ./chat_start.bat

### 3.	Registre um nome de usuário (nomeUsuario):
    #### Digite seu nome de usuario: Pedro

### 4.	Escolha uma das opções do primeiro menu, criando ou entrando em uma sala:
         #### 1) Criar sala 
         #### 2) Entrar em uma sala
         #### 3) Listar salas
         #### 4) Encerrar

### 6.	Escolha uma das opções do segundo menu e envie mensagens:
         #### 1) Enviar mensagem
         #### 2) Sair da sala
         #### 3) Listar usuários
         #### 4) Encerrar

### 7.	Receba mensagens automaticamente:
         #### [12:34:56] Pedro: Bom dia a todos!

