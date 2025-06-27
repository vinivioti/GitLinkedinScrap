# POC_ScrappingGit - Scraper GitHub de perfis com LinkedIn

Este projeto automatiza a busca de perfis públicos no GitHub localizados em **São Paulo**, filtrando por linguagem **Java**, e extrai os links do LinkedIn dos perfis encontrados. O resultado é salvo em uma planilha Excel para facilitar o contato do RH.

---

## ⚙️ Tecnologias usadas

- Python 3 (testado em 3.9+)
- Playwright para Python
- OpenPyXL para geração de Excel
- PowerShell para automação da execução e envio de e-mail (Windows)

---

## 🚀 Instruções de instalação

### 1. Instalar Python

- **Windows**: Baixe do site oficial https://www.python.org/downloads/windows/
- **MacOS**: Python 3 geralmente já vem instalado. Use `python3 --version` para verificar.

---

### 2. Clonar o repositório e criar ambiente virtual

```bash
git clone https://github.com/vinivioti/POC_ScrappingGit.git
cd POC_ScrappingGit

Criar e ativar virtualenv
Windows (PowerShell):

python -m venv venv
.\venv\Scripts\Activate.ps1

MacOS/Linux:
python3 -m venv venv
source venv/bin/activate

### 3. Instalar dependências

pip install -r requirements.txt

(Se não existir, crie o arquivo requirements.txt com as linhas abaixo)

playwright
openpyxl

### 4. Instalar navegadores do Playwright

python -m playwright install

📖 Como usar
Executar o script passando as páginas que deseja analisar.

python github_scrapper.py --start 1 --end 3 --show

--start: página inicial da busca no GitHub

--end: página final da busca

--show: (opcional) exibe o navegador para acompanhar cliques (remova para rodar headless)

Atenção:
Cada página tem até 10 perfis, e o script abre perfil por perfil para capturar o LinkedIn. Rodar muitas páginas pode levar tempo e consumir recursos, use com moderação.


📨 PowerShell para executar e enviar relatório por e-mail (Windows)
Temos um script PowerShell run_and_send.ps1 que:

Ativa o ambiente virtual

Executa o scraper Python

Envia o arquivo Excel gerado por e-mail via SMTP


Configurar o PowerShell
Edite o arquivo run_and_send.ps1 e configure as variáveis de e-mail:

$smtpServer = "smtp.seuprovedor.com"
$smtpPort = 587
$smtpUser = "seuemail@provedor.com"
$smtpPass = "suasenha"
$emailFrom = "seuemail@provedor.com"
$emailTo = "rh@empresa.com"
$emailSubject = "Relatório GitHub LinkedIn"
$emailBody = "Segue em anexo o relatório atualizado dos perfis GitHub com LinkedIn."

Rodar o PowerShell
Abra o PowerShell com permissão e rode:

.\run_and_send.ps1 -start 1 -end 3 -show
Parâmetros -start e -end controlam o intervalo de páginas buscadas.

📄 Arquivos importantes
github_scrapper.py: Script principal em Python

requirements.txt: Dependências Python

run_and_send.ps1: Script PowerShell para rodar scraper e enviar e-mail

perfis_com_linkedin.xlsx: Planilha gerada com os resultados

❓ Dúvidas / Problemas
Verifique se Python e Playwright estão instalados corretamente

Use o parâmetro --show para acompanhar a execução

Confira as permissões do PowerShell para rodar scripts (Set-ExecutionPolicy RemoteSigned)

🙌 Agradecimentos
Feito com 💻 + ☕️ por Vioti - automação para facilitar o trabalho do RH!
