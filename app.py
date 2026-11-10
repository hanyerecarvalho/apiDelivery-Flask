from server import Server

def main():
    try:
        server = Server(porta=8080)

        server.init()

        server.run()

        print("✅ Servidor iniciado com sucesso")
    except Exception as error:
        print("❌ Erro ao iniciar o servidor:", error)

main()