# 🧓 tdmax-seniors-updater

Automação em Python para atualização mensal dos cadastros gratuitos do tipo **Seniors** e **Senior60** no sistema **TDMax Gerencial**.  
O script acessa automaticamente o sistema, verifica a data do último uso do cartão e **atualiza apenas os cadastros com uso recente (menos de 60 dias)**.

---

## ⚙️ Funcionalidades

- Acesso automático ao sistema web TDMax Gerencial com Playwright.
- Verificação da data do último uso do cartão.
- Atualização da data de vencimento do cartão para um valor definido (ex: `30/06/2026`).
- Log de cadastros já atualizados para evitar duplicações.
- Processamento em lote com intervalo automático para evitar sobrecarga.

---

## ⚠️ Pré-requisitos Antes da Execução

Antes de rodar o script, você precisa:

1. **Exportar o relatório no sistema TDMax:**
   - Acesse o menu de **Listagem de Cadastros** no TDMaxReports.
   - Gere e baixe o relatório de cadastros com vencimento previsto **no mês atual**.
   - Salve esse arquivo como `Relatorio (3).xlsx` (ou outro nome à sua escolha).

2. **Configurar o script se necessário:**
   - Se o nome do arquivo Excel ou do log **for diferente**, atualize as constantes no início do script:
     ```python
     ARQUIVO_EXCEL = "Relatorio (3).xlsx"
     ARQUIVO_LOG = "cadastros_atualizados.txt"
     ```
   - Se o script e os arquivos não estiverem na **mesma pasta**, forneça o **caminho completo** para os arquivos.
   - Se for atualizar para outra **data de vencimento**, altere diretamente no código:
     ```python
     pagina.type(venc_selector, "30062026")  # Altere para a nova data desejada
     ```

---

## 🗂 Estrutura dos Arquivos

| Arquivo                        | Descrição                                         |
|-------------------------------|---------------------------------------------------|
| `seniors.py`                  | Script principal de automação                     |
| `Relatorio (3).xlsx`          | Planilha com os códigos dos cadastros (coluna D)  |
| `cadastros_atualizados.txt`   | Log dos códigos já atualizados                    |

---

## 🛠 Requisitos

- Python 3.8+
- Bibliotecas Python:
  - `pandas`
  - `playwright`

Instalação:

```bash
pip install pandas playwright
playwright install
