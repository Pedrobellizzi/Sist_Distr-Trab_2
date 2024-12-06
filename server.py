# Código do Servidor


import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from datetime import datetime, timedelta
import threading, json, logging

class ServerChat:
    def __init__(self):                    # Estruturas de dados para gerenciar os usuários, as salas e inatividade
        self.usuarios = {}                            # {nomeUsuario: nomeSala}
        self.salas = {}                               # {nomeSala: {"usuarios": [], "mensagens": []}}
        self.salasInativas = {}                       # {nomeSala: timestampUltimaAtividade}
        self.arquivoUsuarios = "usuarios.json"        # Nome do arquivo JSON
        self.trava = threading.Lock()                 # Inicializa o travamento
        self.limpar_arquivo_usuarios()                # Limpa o arquivo de usuários ao iniciar

    def limpar_arquivo_usuarios(self):           # Limpar o arquivo JSON esvaziando-o ao iniciar o servidor
        with open(self.arquivoUsuarios, "w") as arquivo:
            json.dump([], arquivo)

    def carregar_usuarios(self):                 # Carregar usuários na lista contida no arquivo JSON
        try:
            with open(self.arquivoUsuarios, "r") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return []

    def salvar_usuario(self, nomeUsuario):          # Adicionar um usuário novo no arquivo JSON
        usuarios = self.carregar_usuarios()
        usuarios.append(nomeUsuario)
        with open(self.arquivoUsuarios, "w") as arquivo:
            json.dump(usuarios, arquivo)

                    # --- Funções destinadas ao Gerenciamento de Usuários ---
    def registrar_usuario(self, nomeUsuario):          # Registrar um usuário novo, verificando se ele já existe.
        if nomeUsuario in self.carregar_usuarios():
            logging.info(f"Tentativa de registro de nome duplicado: {nomeUsuario}")
            return False, "Nome de usuário já está em uso."
        self.salvar_usuario(nomeUsuario)
        self.usuarios[nomeUsuario] = None
        logging.info(f"Usuário registrado: {nomeUsuario}")
        return True, "Usuário '{nomeUsuario}' registrado com sucesso."

                    # --- Funções destinadas ao gerenciamento das Salas ---
    def criar_sala(self, nomeSala):                # Criar uma sala nova
        with self.trava:
            if nomeSala in self.salas:
                return False, "O nome da sala já existe."
            self.salas[nomeSala] = {"usuarios": [], "mensagens": []}
            return True, f"Sala '{nomeSala}' criada com sucesso."

    def entrar_na_sala(self, nomeUsuario, nomeSala):          # Fazer um usuário entrar em alguma sala
        with self.trava:
            if nomeUsuario not in self.usuarios:
                return False, "Usuário não registrado."
            if nomeSala not in self.salas:
                return False, "Sala não encontrada."
            
            if self.usuarios[nomeUsuario]:                     # Remover um usuário de outra sala, se necessário
                self.sair_da_sala(nomeUsuario)

            self.salas[nomeSala]["usuarios"].append(nomeUsuario)      # Adicionar um usuário à uma sala
            self.usuarios[nomeUsuario] = nomeSala
            self.salasInativas.pop(nomeSala, None)                    # Remove uma sala da lista de inatividade
            self.salas[nomeSala]["mensagens"].append({
                "tipo": "broadcast",
                "origem": "SERVER",
                "conteudo": f"{nomeUsuario} entrou na sala.",
                "timestamp": datetime.now()
            })

                            # Informar e retornar os dados e mensagens da sala
            usuariosNaSala = self.salas[nomeSala]["usuarios"]  
            mensagens = self.salas[nomeSala]["mensagens"][-50:]              # Últimas 50 mensagens
            return True, {"usuarios": usuariosNaSala, "mensagens": mensagens}

    def sair_da_sala(self, nomeUsuario):                     # Fazer um usuário sair da sala 
        with self.trava:
            if nomeUsuario not in self.usuarios or not self.usuarios[nomeUsuario]:
                return False, "Usuário não está em nenhuma sala."

            nomeSala = self.usuarios[nomeUsuario]
            self.salas[nomeSala]["usuarios"].remove(nomeUsuario)
            self.usuarios[nomeUsuario] = None

                          # Informar ou adicionar uma mensagem de saída
            self.salas[nomeSala]["mensagens"].append({
                "tipo": "broadcast",
                "origem": "SERVER",
                "conteudo": f"{nomeUsuario} saiu da sala.",
                "timestamp": datetime.now()
            })

                          # Marcar uma sala para remoção se estiver vazia
            if not self.salas[nomeSala]["usuarios"]:
                self.salasInativas[nomeSala] = datetime.now()

            return True, f"Usuário '{nomeUsuario}' saiu da sala '{nomeSala}'."


                    # --- Funções destinadas ao gerenciamento das Mensagens ---
                    # Enviar uma mensagem para todos da sala ou para um destinatário específico
    def enviar_mensagem(self, nomeUsuario, nomeSala, mensagem, destinatario=None):
        with self.trava:
            if nomeUsuario not in self.usuarios or self.usuarios[nomeUsuario] != nomeSala:
                return False, "Usuário não está na sala especificada."
            
            mensagemDados = {
                "tipo": "unicast" if destinatario else "broadcast",
                "origem": nomeUsuario,
                "conteudo": mensagem,
                "timestamp": datetime.now()
            }

            if destinatario:
                if destinatario not in self.salas[nomeSala]["usuarios"]:
                    return False, "Destinatário não está na mesma sala."
                mensagemDados["destino"] = destinatario
            else:
                mensagemDados["destino"] = "todos"

            self.salas[nomeSala]["mensagens"].append(mensagemDados)
            return True, "Mensagem enviada com sucesso."

    def receber_mensagens(self, nomeUsuario, nomeSala):
                   # Retornar mensagens da sala para o usuário
        with self.trava:
            if nomeUsuario not in self.usuarios or self.usuarios[nomeUsuario] != nomeSala:
                return False, "Usuário não está na sala especificada."

            mensagens = [
                msg for msg in self.salas[nomeSala]["mensagens"]
                if msg["tipo"] == "broadcast" or msg.get("destino") == nomeUsuario
            ]
            return True, mensagens

                  # --- Funções destinadas a gerenciar a listagem de Salas e Usuários ---
    def listar_salas(self):                   # Informar e retornar a lista de salas disponíveis
        with self.trava:
            return True, list(self.salas.keys())

    def listar_usuarios(self, nomeSala):               # Informar e retornar a lista de usuários de uma sala específica
        with self.trava:
            if nomeSala not in self.salas:
                return False, "Sala não encontrada."
            return True, self.salas[nomeSala]["usuarios"]

                      # --- Função para remover Salas Inativas ---
    def limpar_salas_inativas(self):                # Remover salas sem usuários após 5 minutos de inatividade
        while True:
            with self.trava:
                agora = datetime.now()
                for sala, ultimaAtividade in list(self.salasInativas.items()):
                    if agora - ultimaAtividade > timedelta(minutes=5):
                        del self.salas[sala]
                        del self.salasInativas[sala]
                        print(f"Sala '{sala}' removida por inatividade.")
            threading.Event().wait(60)                # Espera 60 segundos antes da próxima verificação


if __name__ == "__main__":
                        # Conectar ao Binder
    binder = xmlrpc.client.ServerProxy("http://localhost:5000/")
    procedure_name = "ChatService"
    address, port = "localhost", 8005

                     # Registrar no Binder
    sucesso, mensagem = binder.registrar_procedimento(procedure_name, address, port)
    print(mensagem)

    if sucesso:
                     # Iniciar o servidor RPC
        server = SimpleXMLRPCServer((address, port), requestHandler=SimpleXMLRPCRequestHandler, allow_none=True)
        server.register_instance(ServerChat())

                    # Iniciar a thread de limpeza de salas inativas
        threadLimpeza = threading.Thread(target=server.instance.limpar_salas_inativas, daemon=True)
        threadLimpeza.start()

        print(f"Servidor de chat rodando em {address}:{port}...")
        server.serve_forever()
