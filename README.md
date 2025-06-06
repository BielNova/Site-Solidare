# 🌐 Site Solidare

Este é um sistema web desenvolvido com **Python/Django** para o **Instituto Solidare**, uma organização social sediada em Recife, Brasil. O projeto visa apoiar as iniciativas sociais da instituição por meio da tecnologia.

---

## 📌 Visão Geral

O Site Solidare é uma plataforma digital projetada para facilitar a gestão de projetos sociais, otimizar os processos de inscrição para programas seletivos e aprimorar a comunicação com a comunidade atendida pelo Instituto Solidare.

---

## 🚀 Tecnologias Utilizadas

Este projeto utiliza um conjunto robusto de tecnologias para garantir escalabilidade, manutenibilidade e uma experiência de usuário fluida:

* **Backend:** Python 3 e Django
* **Frontend:** HTML5, CSS3, JavaScript
* **Banco de Dados:** SQLite
* **CI/CD:** GitLab CI (configurado via `.gitlab-ci.yml`)
* **Hospedagem:** Azure Web Apps

---

## 🛠️ Instalação e Execução Local

Para colocar o Site Solidare funcionando em sua máquina local, siga estes passos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/BielNova/Site-Solidare.git](https://github.com/BielNova/Site-Solidare.git)
    cd Site-Solidare
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate # Para Windows: venv\Scripts\activate
    ```
3.  **Instale as dependências do projeto:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure as variáveis de ambiente** conforme necessário para sua configuração local.
5.  **Aplique as migrações do banco de dados e inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

---

## 🔑 Gestão de Usuários e Professores

Implementamos controles de acesso específicos para manter a integridade e segurança dos dados:

* **Perfis de Professores:** Os perfis dos professores são criados exclusivamente através do painel administrativo do Django (`/admin`). Apenas administradores têm acesso a esta área, garantindo supervisão e segurança adequadas.
* **Validação de Alunos:** Os alunos são adicionados ao sistema somente após a validação pelo professor responsável, por meio de uma área restrita dentro do próprio sistema.

---

## 📁 Estrutura do Projeto

O projeto é organizado logicamente para promover clareza e facilidade de desenvolvimento:

* `core/`: Contém as aplicações Django principais e centrais.
* `processo_seletivo/`: Módulo dedicado à gestão de processos seletivos e registros de inscrições.
* `requirements.txt`: Uma lista abrangente de todas as dependências e bibliotecas necessárias.
* `manage.py`: O script utilitário padrão do Django para executar vários comandos.
* `.gitlab-ci.yml`: O arquivo de configuração para integração contínua com GitLab.

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT**. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🤝 Contribuições

Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir *issues* ou enviar *pull requests*.
