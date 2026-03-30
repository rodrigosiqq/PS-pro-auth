# PS Pro Auth - Sistema de Autenticação

Este é o microserviço de autenticação do ecossistema **Plantão Service Pro**. Desenvolvido com uma arquitetura de microserviços, este componente é responsável por gerenciar o ciclo de vida de acesso dos usuários de forma desacoplada do SaaS principal e do Frontend.

## 🚀 Sobre o *Projeto

O **PS Pro Auth** atua como o Identity Provider (IdP) centralizado. Ele permite que o sistema principal e outras ferramentas satélites validem credenciais e gerenciem permissões sem sobrecarregar a lógica de negócio do SaaS.

### Principais Características:
- **Login Desacoplado:** Autenticação independente do sistema principal.
- **Arquitetura de Microserviços:** Pronto para escalabilidade e fácil integração via APIs REST.
- **Segurança:** Implementação de tokens JWT para comunicação segura entre serviços.
- **Integração Frontend:** Compatível com aplicações SPA/Mobile que consomem o ecossistema Plantão Service Pro.
*
## 🛠 Tecnologias Utilizadas

- **Flask** (ou framework utilizado)
- **JWT (JSON Web Tokens)** para autenticação.
- **SQLAlchemy** (conforme sua implementação).
- **SQlite** (conforme sua implementação).

## 🔧 Configuração e Instalação

### Pré-requisitos
- Python.
- Flask
- PyJwt

### Passo a Passo1. **Instale o gerenciador de pacotes `uv` (caso não tenha):**
    ```bash
    pip install uv
    ```

2. **Instale as dependências:**
    ```bash
    uv sync
    ```

3. **Ative o ambiente virtual:**
    ```bash
    # Windows
    .venv\Scripts\activate
    # Linux/macOS
    source .venv/bin/activate
    ```

4. **Execute a aplicação:**
    ```bash
    python app.py
   

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/ps-pro-auth.git
    ```

2. **Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do projeto seguindo o modelo:
    ```env
    PORT=3333
    DATABASE_URL="sua_string_de_conexao"
    JWT_SECRET="seu_segredo_super_seguro"
    EXPIRES_IN="1d"
    ```

