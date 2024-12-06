# Código do Binder


from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class Binder:
              # Guardar e armazenar os procedimentos no formato {nome_do_procedimento: {"endereco": address, "porta": port}}
    def __init__(self):    
        self.procedures = {}

              # Fazer o registro de um procedimento remoto com o seu nome, endereço IP e porta.
    def registrar_procedimento(self, procedure_name, address, port): 
        if procedure_name in self.procedures:
            return False, f"Procedimento '{procedure_name}' já está registrado."
        self.procedures[procedure_name] = {"endereco": address, "porta": port}
        return True, f"Procedimento '{procedure_name}' registrado no endereço e porta {address}:{port}."

              # Fazer a busca e retornar o endereço e a porta de um procedimento remoto pelo seu nome.	
    def buscar_procedimento(self, procedure_name):
        if procedure_name not in self.procedures:
            return False, f"Procedimento '{procedure_name}' não encontrado."
        return True, self.procedures[procedure_name]

if __name__ == "__main__":              # Executar o Binder na porta fixa 5000
    portaBinder = 5000
    server = SimpleXMLRPCServer(("localhost", portaBinder), requestHandler=SimpleXMLRPCRequestHandler)
    binder = Binder()
    server.register_instance(binder)
    print(f"Binder está rodando na porta {portaBinder}...")
    server.serve_forever()
