# GitLinkedin.ps1

# # Configurações de e-mail
$smtpServer = "smtp.mail.yahoo.com"
$smtpPort = 587
$smtpUser = "SEUEMAIL@yahoo.com.br"
$smtpPass = "SEUTOKENYAHOO"
$emailFrom = "SEUEMAIL@yahoo.com.br"
$emailTo = "SEUEMAIL@yahoo.com.br"  # pode ser outro e-mail destino
$emailSubject = "Relatório GitHub LinkedIn"
$emailBody = "Segue em anexo o relatório atualizado dos perfis GitHub com LinkedIn."



$ehWindows = $env:OS -eq "Windows_NT"

if ($ehWindows) {
    $pythonExe = ".\venv\Scripts\python.exe"
} else {
    $pythonExe = "./venv/bin/python"
}


$scriptPy = Join-Path $PSScriptRoot "github_scrapper.py"

$arquivoExcel = Join-Path $PSScriptRoot "perfis_com_linkedin.xlsx"
$arquivoExcel1 = Join-Path $PSScriptRoot "perfis_com_linkedin.csv"


# Função para confirmação com o usuário
function Confirmacao($mensagem) {
    do {
        $resposta = (Read-Host "$mensagem (S/N)").Trim().ToUpper()
    } while ($resposta -notin @("S", "N"))
    return $resposta -eq "S"
}

# Loop até o usuário confirmar corretamente os parâmetros
do {
    $start = Read-Host "Digite a página INICIAL de validação" 
    $end = Read-Host "Digite a página FINAL de validação" 

    Write-Host ""
    Write-Host "Você vai verificar da página $start até a página $end" 
    $showNavegador = Confirmacao "Deseja visualizar o navegador durante a execução?" 

    Write-Host "`nConfirma os dados acima?" 
    $confirmado = Confirmacao "Confirmar"
    if (-not $confirmado) {
        Write-Host "`nReiniciando parâmetros..."
    }
} while (-not $confirmado)

# Montar comando de execução
$showFlag = ""
if ($showNavegador) {
    $showFlag = "--show"
}

Write-Host "`n🟢 Iniciando execução do scraper Python..." 
$arguments = @("--start", $start, "--end", $end)
if ($mostrarNavegador) {
    $arguments += "--show"
}
& $pythonExe $scriptPy @arguments


# Verifica se gerou o Excel
if (-Not (Test-Path $arquivoExcel)) {
    Write-Host "❌ Arquivo Excel não encontrado. Abortando envio de e-mail." -ForegroundColor Red
    exit 1
}

# Enviar e-mail
Write-Host "`n📨 Enviando relatório por e-mail..."
try {
    $smtp = New-Object Net.Mail.SmtpClient($smtpServer, $smtpPort)
    $smtp.EnableSsl = $true
    $smtp.Credentials = New-Object System.Net.NetworkCredential($smtpUser, $smtpPass)

    $msg = New-Object Net.Mail.MailMessage
    $msg.From = $emailFrom
    $msg.To.Add($emailTo)
    $msg.Subject = $emailSubject
    $msg.Body = $emailBody
    $msg.Attachments.Add($arquivoExcel)
    $msg.Attachments.Add($arquivoExcel1)

    $smtp.Send($msg)
    Write-Host "✅ E-mail enviado com sucesso!"
} catch {
    Write-Host "❌ Erro ao enviar o e-mail: $_"
}
