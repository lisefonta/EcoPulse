
# 🌱 EcoPulse — Monitoramento Ambiental Inteligente

Sistema web de monitoramento ambiental desenvolvido como projeto acadêmico do curso de Ciência da Computação da Universidade Paulista (UNIP).

O EcoPulse permite acompanhar indicadores meteorológicos de São Paulo, incluindo temperatura, umidade relativa do ar e qualidade do ar, por meio de um dashboard interativo.

## 🎯 Objetivo

Desenvolver uma aplicação que integre programação Python, APIs públicas, banco de dados e tecnologias web para facilitar a consulta e o acompanhamento de informações ambientais.

O projeto explora conceitos de cidades inteligentes, sustentabilidade e monitoramento ambiental.

## ✨ Funcionalidades

- Consulta de temperatura e umidade atualizadas.
- Monitoramento da qualidade do ar pelo índice europeu EAQI.
- Dashboard com indicadores ambientais.
- Gráficos interativos de temperatura, umidade e qualidade do ar.
- Armazenamento de medições no banco SQLite.
- Histórico de medições com data e horário.
- Coleta automática programada para ocorrer de hora em hora.
- Atualização dos indicadores no navegador a cada cinco minutos.
- API REST desenvolvida com Flask.

**Observação:** a coleta automática de hora em hora está em fase de validação.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.11 | Lógica e processamento dos dados |
| Flask | Servidor web e API REST |
| SQLite | Armazenamento das medições |
| HTML5 | Estrutura da interface |
| CSS3 | Estilização do dashboard |
| JavaScript | Interatividade e atualização dos dados |
| Chart.js | Visualização dos gráficos |
| Requests | Comunicação com APIs externas |
| Open-Meteo | Dados meteorológicos e qualidade do ar |
| Git e GitHub | Versionamento e publicação do código |

## 🏗️ Arquitetura

O sistema utiliza uma arquitetura cliente-servidor.

1. A Open-Meteo fornece informações meteorológicas.
2. O backend Python consulta e processa os dados.
3. O Flask disponibiliza os dados por meio de rotas HTTP.
4. O SQLite armazena o histórico das medições.
5. O dashboard apresenta as informações em gráficos e indicadores.

A coleta periódica é realizada por um processo Python enquanto o servidor estiver em execução.

## 📁 Estrutura do projeto

```text
EcoPulse/
├── app/
│   ├── __init__.py
│   ├── collector.py
│   ├── database.py
│   ├── routes.py
│   ├── weather_api.py
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   └── templates/
│       └── index.html
├── data/
├── tests/
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## ⚙️ Como executar

### 1. Pré-requisitos

- Python 3.11 ou compatível.
- Acesso à internet.
- Navegador atualizado.

### 2. Instalar as dependências

Na pasta principal do projeto, execute:

```bash
python -m pip install -r requirements.txt
```

### 3. Iniciar o servidor

```bash
python run.py
```

### 4. Acessar o dashboard

Abra o navegador:

http://127.0.0.1:5000

O banco de dados SQLite será inicializado automaticamente na primeira execução.

## 🔗 Rotas da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Dashboard |
| GET | `/weather` | Dados meteorológicos atuais |
| GET | `/air-quality` | Qualidade do ar atual |
| GET | `/weather/history` | Histórico armazenado |
| GET | `/measurements` | Medições cadastradas |
| POST | `/measurements` | Cadastro manual de medições |

## 🕒 Atualização automática

O EcoPulse utiliza dois mecanismos de atualização:

**Dashboard:** quando a página está aberta, o JavaScript consulta periodicamente os dados atuais.

**Coletor Python:** executa consultas periódicas para armazenar medições no SQLite, mesmo com o navegador fechado.

A coleta depende de o processo Python permanecer ativo. Se o computador estiver desligado ou suspenso, não haverá novas coletas.

## 🌎 Localização monitorada

São Paulo — SP, Brasil.

Coordenadas aproximadas:
- Latitude: -23.5505
- Longitude: -46.6333

## 🧪 Testes

Foram realizados testes manuais de:

- Inicialização do servidor Flask.
- Consulta aos endpoints HTTP.
- Exibição de temperatura, umidade e qualidade do ar.
- Funcionamento dos gráficos interativos.
- Consulta do histórico armazenado.
- Persistência de registros no SQLite.

A validação da coleta automática independente do navegador ainda está em andamento.

## ⚠️ Limitações

O EcoPulse é um protótipo acadêmico.

A versão atual utiliza APIs públicas como alternativa à utilização de sensores físicos e microcontroladores. Portanto, não realiza medições por hardware próprio.

A precisão e a disponibilidade dos dados dependem dos serviços externos consultados.

O servidor Flask utilizado é destinado ao desenvolvimento local, não à hospedagem pública em produção.

## 🚀 Melhorias futuras

- Integração com ESP32 e sensores físicos.
- Monitoramento de outras cidades.
- Alertas ambientais.
- Exportação de dados históricos.
- Hospedagem em servidor externo.
- Testes automatizados mais abrangentes.

## 📚 Referências

- Open-Meteo: https://open-meteo.com/
- Open-Meteo Air Quality API: https://open-meteo.com/en/docs/air-quality-api
- Flask: https://flask.palletsprojects.com/
- Python: https://www.python.org/
- SQLite: https://www.sqlite.org/
- Chart.js: https://www.chartjs.org/

## 🎓 Contexto acadêmico

**Instituição:** Universidade Paulista (UNIP)

**Curso:** Ciência da Computação

**Disciplina:** Projeto e Desenvolvimento II

**Ano:** 2026

**Projeto:** EcoPulse — Monitoramento Ambiental Inteligente

---

Desenvolvido para fins acadêmicos, com foco na integração entre tecnologia, sustentabilidade e acesso à informação ambiental.
