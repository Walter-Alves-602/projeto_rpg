# Gerenciador de Personagens D&D (Flet GUI)

Este projeto é um gerenciador de personagens simplificado para Dungeons & Dragons 5ª Edição, construído com Python. Ele permite criar, visualizar e gerenciar personagens, incluindo raças, classes, atributos, habilidades raciais e magias. A interface gráfica (GUI) é desenvolvida usando a biblioteca [Flet](https://flet.dev/), proporcionando uma experiência interativa e multiplataforma.

## Funcionalidades Atuais

* Criação de novos personagens com nome, jogador, raça, classe e atributos.
* Listagem e visualização detalhada de personagens existentes.
* Exibição de atributos, modificadores, pontos de vida, habilidades raciais e magias da classe.
* Atualização dinâmica dos Pontos de Vida (PV) do personagem na interface.

## Estrutura do Projeto

projeto_rpg/  
├── src/  
│   ├── application/  
│   │   └── use_cases/  
│   │       └── gerenciar_personagem_use_case.py  
│   ├── domain/  
│   │   └── models/  
│   │       └── personagem.py  
│   ├── infrastructure/  
│   │   ├── adapters/  
│   │   │   ├── database/  
│   │   │   │   └── sqlite_character_repository.py  
│   │   │   └── data_files/  
│   │   │       ├── classes_adapter.py  
│   │   │       ├── classes_data.py  
│   │   │       ├── habilidades_raciais_file_adapter.  py
│   │   │       ├── racas_adapter.py  
│   │   │       ├── spells_data.py  
│   │   │       └── spells_file_adapter.py  
│   │   └── repositories/  
│   │       ├── classe_repository.py  
│   │       ├── habilidades_raciais_repository.py  
│   │       ├── personagem_repository.py  
│   │       ├── raca_repository.py  
│   │       └── spell_repository.py  
│   │   └── persistence/  
│   │       └── database_manager.py  
│   ├── ui/  
│   │   └── flet_app.py  (A interface gráfica) principal  
├── main.py  (Script original da   interface de) console (mantido)  
└── README.md  (Este arquivo)    
└── requirements.txt  (Dependências do projeto)    


## Configuração e Execução

Siga os passos abaixo para configurar e rodar o projeto.

### 1. Clonar o Repositório (se aplicável)

Se você estiver em um repositório Git, certifique-se de estar na branch correta ou clonar o projeto:

```bash
git clone <URL_DO_SEU_REPOSITORIO> # Se for um repositório online
cd projeto_rpg
git checkout feature/interface-flet # Se você já tem o projeto e está trabalhando em uma branch
```

2. Criar e Ativar o Ambiente Virtual

É uma boa prática usar ambientes virtuais para isolar as dependências do projeto.
Bash
```python
python3 -m venv .venv
source .venv/bin/activate # No Linux/macOS
# .venv\Scripts\activate # No Windows
```
3. Instalar Dependências

```python
pip install -r requirements.txt
```

4. Executar o Aplicativo Flet

Com o ambiente virtual ativado e as dependências instaladas, você pode iniciar a aplicação gráfica:
Bash
```bash
python src/ui/flet_app.py
```
Isso abrirá uma janela do aplicativo Flet.
Solução de Problemas Comuns (Linux: libmpv.so.1 Not Found)

Em sistemas Linux, ao executar o Flet, você pode encontrar o seguinte erro:
```bash
error while loading shared libraries: libmpv.so.1: cannot open shared object file: No such file or directory
```
Isso ocorre porque o executável interno do Flet (que é pré-compilado) espera uma versão específica da biblioteca libmpv (.so.1), mas seu sistema pode ter uma versão mais nova (.so.2 ou superior).

Para resolver isso, siga os passos abaixo:

    Atualize os pacotes e instale mpv e libmpv-dev:
    Bash
```bash
sudo apt-get update
sudo apt-get install mpv libmpv-dev
```
(No Linux Mint/Ubuntu, o pacote mpv geralmente fornece a biblioteca libmpv, e libmpv-dev pode incluir links simbólicos e arquivos de desenvolvimento úteis).

Crie um link simbólico (symlink) para libmpv.so.1:
Você precisa criar um link que "engane" o Flet, fazendo libmpv.so.1 apontar para a versão que você realmente tem (no seu caso, libmpv.so.2).

Execute os comandos abaixo na ordem:
```Bash

    cd /usr/lib/x86_64-linux-gnu/ # Navegue para o diretório onde a libmpv.so.2 está
    sudo ln -s libmpv.so.2 libmpv.so.1 # Crie o link simbólico
    sudo ldconfig # Atualize o cache de bibliotecas do sistema

    Após executar esses comandos, retorne à pasta raiz do seu projeto e tente rodar o aplicativo Flet novamente. Ele deve funcionar.
```
Próximos Passos e Melhorias Potenciais

    Implementar testes de Habilidades/Perícias: Adicionar botões clicáveis para realizar testes de dados de acordo com os atributos e proficiências do personagem.
    Gerenciamento de Inventário: Uma seção para adicionar, remover e visualizar itens.
    Combate: Funcionalidades para iniciar combate, rastrear iniciativa, turnos, etc.
    Magias: Uma interface mais detalhada para gerenciar magias conhecidas, espaços de magia e conjuração.
    Progressão de Nível: Lógica para aumentar o nível do personagem e aplicar ganhos de HP, habilidades, etc.
    Persistência de Dados: Melhorias no banco de dados para armazenar mais detalhes do personagem.