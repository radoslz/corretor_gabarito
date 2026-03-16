# Corretor de Gabarito

Sistema web em Django para uso pedagogico local, focado em cadastro de escolas, turmas, alunos e provas, com correcao manual, relatorios por prova e por turma, alem de exportacao em Excel.

## Visao geral

O projeto foi pensado desde o inicio para rodar localmente com simplicidade. Por isso, a configuracao padrao usa `SQLite`, o que reduz instalacao, manutencao e custo operacional para uso em escola, secretaria ou computador pessoal.

Mesmo assim, o projeto ja ficou preparado para uso com `PostgreSQL` por variaveis de ambiente, caso alguem queira evoluir para um cenario com mais usuarios, deploy em servidor ou banco dedicado.

## O que o sistema faz hoje

- autenticacao de usuarios
- dashboard inicial com indicadores gerais
- cadastro de escolas
- cadastro de turmas com serie, turno, ano letivo e professor responsavel
- cadastro de alunos individualmente
- importacao de alunos por CSV/TXT
- importacao de alunos diretamente a partir da tela da turma
- listagem de alunos com filtros por escola, ano letivo e turma
- cadastro de provas
- associacao de uma mesma prova a varias turmas
- correcao manual por aluno
- relatorio geral por prova
- relatorio filtrado por turma dentro da prova
- exportacao em Excel dos resultados detalhados
- exportacao em Excel do resumo por questao
- tema claro e escuro

## Stack atual

- Python 3.12+
- Django 5
- SQLite como banco padrao
- PostgreSQL opcional via `.env`
- OpenPyXL para exportacao Excel
- WhiteNoise para servir arquivos estaticos
- python-decouple para configuracao por ambiente

## Estrutura resumida

```text
apps/
  accounts/   # autenticacao
  schools/    # escolas, turmas e alunos
  exams/      # provas, aplicacoes, correcao e relatorios
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
- definicao do banco (`SQLite` ou `PostgreSQL`)

### Exemplo de configuracao local com SQLite

```env
SECRET_KEY=sua-chave
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
TIME_ZONE=America/Fortaleza
DB_ENGINE=sqlite
DB_SQLITE_NAME=db.sqlite3
```

### Exemplo de configuracao com PostgreSQL

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
2. Instale as dependencias com `pip install -r requirements.txt`.
3. Copie `.env.example` para `.env`.
4. Rode as migrations com `python manage.py migrate`.
5. Crie um usuario administrador com `python manage.py createsuperuser`.
6. Inicie o projeto com `python manage.py runserver`.

## Testes e verificacoes

- Validacao basica do Django: `python manage.py check`
- Testes automatizados: `python manage.py test`

## Decisoes de projeto

- `SQLite` foi mantido como padrao por coerencia com a proposta local do sistema.
- `PostgreSQL` ficou como opcao de crescimento, nao como obrigatoriedade.
- A exportacao implementada hoje e em Excel, que atende melhor o uso administrativo e pedagogico imediato.
- O foco atual esta em fluxo funcional e simplicidade operacional, nao em arquitetura de nuvem.

## Pontos que foram organizados nesta revisao

- configuracao do banco alinhada ao `.env`
- `ALLOWED_HOSTS` voltou a ser controlado por ambiente
- README atualizado para refletir o estado real do projeto
- dependencias sem uso direto removidas do `requirements.txt`
- testes basicos adicionados para filtros de alunos e relatorio por turma

## Ideias de implementacao futura

- destacar item ativo na barra de navegacao
- pagina de configuracoes do sistema pela interface
- painel com metricas por escola, serie e turma
- exportacao PDF de relatorios
- importacao de alunos com colunas adicionais como matricula e observacoes
- lancamento de gabarito oficial por questao
- comparativo entre aplicacoes da mesma prova ao longo do tempo
- trilha de auditoria de correcoes
- permissoes por perfil de usuario
- deploy com PostgreSQL em ambiente compartilhado

## Observacao importante

Este projeto foi construindo com foco claro em uso local. Se voce pretende publicar em producao para varios usuarios, vale configurar:

- `DEBUG=False`
- `ALLOWED_HOSTS` corretamente
- `PostgreSQL`
- backup automatico do banco
- politicas de acesso e seguranca
