# Corretor de Gabarito

Sistema web em Django para uso **pedagógico local**, focado em cadastro de escolas, turmas, alunos e provas, com **correção manual**, **relatórios por prova e por turma**, além de **exportação em Excel**.

## Visão geral

O projeto foi pensado desde o início para rodar localmente com simplicidade. Por isso, a configuração padrão usa `SQLite`, o que reduz instalação, manutenção e custo operacional para uso em escola, secretaria ou computador pessoal.

Mesmo assim, o projeto já ficou preparado para uso com `PostgreSQL` por variáveis de ambiente, caso alguém queira evoluir para um cenário com mais usuários, deploy em servidor ou banco dedicado.

## O que o sistema faz hoje

- autenticação de usuários
- dashboard inicial com indicadores gerais
- cadastro de escolas
- cadastro de turmas com série, turno, ano letivo e professor responsável
- cadastro de alunos individualmente
- importação de alunos por CSV/TXT
- importação de alunos diretamente a partir da tela da turma
- listagem de alunos com filtros por escola, ano letivo e turma
- cadastro de provas
- associação de uma mesma prova a várias turmas
- correção manual por aluno
- relatório geral por prova
- relatório filtrado por turma dentro da prova
- exportação em Excel dos resultados detalhados
- exportação em Excel do resumo por questão
- tema claro e escuro

## Stack atual

- Python 3.12+
- Django 5
- SQLite como banco padrão
- PostgreSQL opcional via `.env`
- OpenPyXL para exportação Excel
- WhiteNoise para servir arquivos estáticos
- python-decouple para configuração por ambiente

## Estrutura resumida

```text
apps/
  accounts/   # autenticação
  schools/    # escolas, turmas e alunos
  exams/      # provas, aplicações, correção e relatórios
config/       # settings, urls e bootstrap do Django
templates/    # interfaces HTML
static/       # CSS e JavaScript
media/        # arquivos enviados em ambiente local
```

## Uso de `.env`

O projeto usa `.env` para:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `TIME_ZONE`
- definição do banco (`SQLite` ou `PostgreSQL`)

### Exemplo de configuração local com SQLite

```env
SECRET_KEY=sua-chave
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
TIME_ZONE=America/Fortaleza
DB_ENGINE=sqlite
DB_SQLITE_NAME=db.sqlite3
```

### Exemplo de configuração com PostgreSQL

```env
SECRET_KEY=sua-chave
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.com
TIME_ZONE=America/Fortaleza
DB_ENGINE=postgres
DB_NAME=corretor_gabarito
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

## Como rodar localmente

1. Crie e ative um ambiente virtual.
2. Instale as dependências com `pip install -r requirements.txt`.
3. Copie `.env.example` para `.env`.
4. Rode as migrations com `python manage.py migrate`.
5. Crie um usuário administrador com `python manage.py createsuperuser`.
6. Inicie o projeto com `python manage.py runserver`.

## Testes e verificações

- Validação básica do Django: `python manage.py check`
- Testes automatizados: `python manage.py test`

## Decisões de projeto

- `SQLite` foi mantido como padrão por coerência com a proposta local do sistema.
- `PostgreSQL` ficou como opção de crescimento, não como obrigatoriedade.
- A exportação implementada hoje é em Excel, que atende melhor o uso administrativo e pedagógico imediato.
- O foco atual está em fluxo funcional e simplicidade operacional, não em arquitetura de nuvem.

## Pontos que foram organizados nesta revisão

- configuração do banco alinhada ao `.env`
- `ALLOWED_HOSTS` voltou a ser controlado por ambiente
- README atualizado para refletir o estado real do projeto
- dependências sem uso direto removidas do `requirements.txt`
- testes básicos adicionados para filtros de alunos e relatório por turma

## Ideias de implementação futura

- destacar item ativo na barra de navegação
- página de configurações do sistema pela interface
- painel com métricas por escola, série e turma
- exportação PDF de relatórios
- importação de alunos com colunas adicionais como matrícula e observações
- lançamento de gabarito oficial por questão
- comparativo entre aplicações da mesma prova ao longo do tempo
- trilha de auditoria de correções
- permissões por perfil de usuário
- deploy com PostgreSQL em ambiente compartilhado

## Observação importante

Este projeto foi construído com foco claro em uso local. Se você pretende publicar em produção para vários usuários, vale configurar:

- `DEBUG=False`
- `ALLOWED_HOSTS` corretamente
- `PostgreSQL`
- backup automático do banco
- políticas de acesso e segurança
