# Sistema de Correção de Gabarito

Sistema web desenvolvido com Django para cadastro de turmas, alunos, provas, gabaritos, correção manual, análises pedagógicas, comparação entre turmas, exportação para Excel e PDF.

## Tecnologias
- Django
- PostgreSQL
- HTML, CSS e JavaScript
- Chart.js

## Funcionalidades previstas
- autenticação de usuários
- cadastro de turmas e alunos
- importação de alunos por CSV
- cadastro de provas e gabaritos
- correção manual rápida
- relatórios automáticos
- comparação entre turmas
- tema escuro
- exportação CSV, Excel e PDF

## Como rodar localmente
1. Criar e ativar ambiente virtual
2. Instalar dependências com `pip install -r requirements.txt`
3. Criar banco PostgreSQL
4. Copiar `.env.example` para `.env`
5. Rodar migrations
6. Executar `python manage.py runserver`