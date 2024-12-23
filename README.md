Automação de Coleta e Organização de Dados com Python e Power BI
Descrição do Projeto:

Este projeto foi desenvolvido com o objetivo de automatizar a coleta de dados relevantes para a análise de desempenho da empresa, atendendo às necessidades dos gerentes. A automação utiliza Python para navegação em páginas web, extração e organização dos dados, que são posteriormente importados para o Power BI, permitindo a visualização interativa e a tomada de decisões informadas.
Estrutura do Código-Fonte:

Principais Arquivos e Diretórios:

    consulta_cpf.py:
    Arquivo principal que contém a lógica do robô, incluindo as etapas de:
        Configuração do Selenium para automação web.
        Extração de dados estruturados e não estruturados.
        Processamento inicial dos dados.

    janela.py.py:
    Contém funções que utilizam a biblioteca Pandas para organizar, tratar e limpar os dados extraídos, garantindo sua consistência antes da exportação.

    requirements.txt:
    Lista de dependências do projeto para fácil configuração do ambiente, incluindo:
        Selenium para automação de navegação.
        Pandas para manipulação de dados.
        Tkinter para exportação em formatos compatíveis.
