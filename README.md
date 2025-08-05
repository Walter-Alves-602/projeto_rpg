# Gerenciador de Personagens D&D (Flet GUI)

Este projeto é um gerenciador de personagens simplificado para Dungeons & Dragons 5ª Edição, construído com Python. Ele permite criar, visualizar e gerenciar personagens, bem como organizar mesas de jogo. A interface gráfica (GUI) é desenvolvida usando a biblioteca [Flet](https://flet.dev/), proporcionando uma experiência interativa e multiplataforma.

## Funcionalidades Atuais

*   **Autenticação de Usuários:**
    *   Registro de novos usuários.
    *   Login de usuários existentes.
    *   Dashboard personalizada após o login, exibindo mesas e personagens do usuário.
*   **Gerenciamento de Personagens:**
    *   Criação de novos personagens com nome, jogador, raça, classe e atributos.
    *   Listagem e visualização detalhada de personagens existentes.
    *   Exibição de atributos, modificadores, pontos de vida, habilidades raciais e magias da classe.
    *   Atualização dinâmica dos Pontos de Vida (PV) do personagem na interface.
*   **Gerenciamento de Mesas de Jogo:**
    *   Criação de mesas por mestres.
    *   Associação de jogadores e personagens a mesas.
    *   Lógica de permissões para mestres e jogadores.

## Arquitetura do Projeto

O projeto segue uma arquitetura em camadas, inspirada na Arquitetura Limpa (Clean Architecture) e Arquitetura Hexagonal (Ports and Adapters), garantindo modularidade, testabilidade e desacoplamento.

*   **Domain (`src/domain/`):** O núcleo da aplicação. Contém a lógica de negócio pura, modelos (entidades como `Usuario`, `Mesa`, `Personagem`) e interfaces (portas) para comunicação com o exterior (ex: `UsuarioRepositoryPort`, `MesaRepositoryPort`). É agnóstico a frameworks e bancos de dados.
*   **Application (`src/application/`):** Contém os casos de uso (use cases) que orquestram a lógica de negócio, utilizando as interfaces definidas no domínio. (ex: `GerenciarPersonagemUseCase`, `GerenciarMesaUseCase`).
*   **Infrastructure (`src/infrastructure/`):** Implementa as interfaces (portas) do domínio. Contém os adaptadores para tecnologias externas, como bancos de dados (SQLite) e arquivos de dados. (ex: `SQLiteUsuarioRepository`, `SQLiteMesaRepository`, `RacaFileAdapter`).
*   **Persistence (`src/persistence/`):** Gerencia a conexão e operações de baixo nível com o banco de dados (SQLite).
*   **UI (`src/ui/`):** A camada de apresentação, responsável pela interface gráfica do usuário utilizando a biblioteca Flet. Interage com a camada de aplicação para executar as funcionalidades.

## Estrutura de Diretórios

```
projeto_rpg/
├── src/
│   ├── application/          # Casos de Uso da Aplicação
│   │   └── use_cases/
│   │       ├── gerenciar_mesa_use_case.py
│   │       └── gerenciar_personagem_use_case.py
│   ├── domain/               # Modelos e Portas (Interfaces)
│   │   ├── models/
│   │   │   ├── armas.py
│   │   │   ├── mesa.py
│   │   │   ├── personagem.py
│   │   │   └── usuario.py
│   │   └── ports/
│   │       ├── arma_repository.py
│   │       ├── classe_repository.py
│   │       ├── habilidades_raciais_repository.py
│   │       ├── mesa_repository.py
│   │       ├── personagem_repository.py
│   │       ├── raca_repository.py
│   │       ├── spell_repository.py
│   │       └── usuario_repository.py
│   │   └── services/
│   │       └── autenticacao_service.py
│   ├── infrastructure/       # Implementações de Repositórios e Adaptadores
│   │   ├── adapters/
│   │   │   ├── data_files/   # Adaptadores para dados de arquivos (raças, classes, etc.)
│   │   │   └── database/     # Adaptadores para banco de dados (SQLite)
│   │   │       ├── sqlite_character_repository.py
│   │   │       ├── sqlite_mesa_repository.py
│   │   │       └── sqlite_usuario_repository.py
│   │   └── repositories/     # Repositórios legados (json_usuario_repository.py)
│   ├── persistence/          # Gerenciamento do Banco de Dados
│   │   └── database_manager.py
│   └── ui/                   # Interface do Usuário (Flet)
│       ├── pages/            # Páginas da aplicação (login, dashboard, etc.)
│       └── flet_app.py       # Ponto de entrada da UI
├── main.py                   # Ponto de entrada principal da aplicação
└── README.md                 # Este arquivo
└── requirements.txt          # Dependências do projeto
```

## Configuração e Execução

Siga os passos abaixo para configurar e rodar o projeto.

### 1. Clonar o Repositório (se aplicável)

```bash
git clone <URL_DO_SEU_REPOSITORIO> # Se for um repositório online
cd projeto_rpg
```

### 2. Criar e Ativar o Ambiente Virtual

É uma boa prática usar ambientes virtuais para isolar as dependências do projeto.

```bash
python3 -m venv .venv
source .venv/bin/activate # No Linux/macOS
# .venv\Scripts\activate # No Windows
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o Aplicativo Flet

Com o ambiente virtual ativado e as dependências instaladas, você pode iniciar a aplicação gráfica:

```bash
python main.py
```

Isso abrirá uma janela do aplicativo Flet, começando pela tela de login.

## Próximos Passos e Melhorias Potenciais

*   **Gerenciamento Completo de Mesas:**
    *   Páginas para criar e gerenciar mesas (adicionar/remover usuários, personagens).
    *   Visualização de detalhes da mesa.
*   **Gerenciamento de Personagens:**
    *   Edição de personagens existentes.
    *   Implementar testes de Habilidades/Perícias: Adicionar botões clicáveis para realizar testes de dados de acordo com os atributos e proficiências do personagem.
    *   Gerenciamento de Inventário: Uma seção para adicionar, remover e visualizar itens.
    *   Magias: Uma interface mais detalhada para gerenciar magias conhecidas, espaços de magia e conjuração.
    *   Progressão de Nível: Lógica para aumentar o nível do personagem e aplicar ganhos de HP, habilidades, etc.
*   **Combate:** Funcionalidades para iniciar combate, rastrear iniciativa, turnos, etc.
*   **Melhorias na UI/UX:** Refinamento visual e de usabilidade das páginas.
*   **Testes Unitários e de Integração:** Adicionar cobertura de testes para as novas funcionalidades.
