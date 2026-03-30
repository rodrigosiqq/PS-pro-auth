from app import create_app

# Instancia o app de autenticação
app = create_app()

if __name__ == "__main__":
    print("Iniciando Auth Service na porta 5001...")
    # Rodamos em porta diferente para não conflitar com o Plantão Service
    app.run(debug=True, port=5001)