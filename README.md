# 🧓 Automação de Atualização de Cadastros SENIORS – TDMax

Este script em Python automatiza a **atualização mensal dos cadastros gratuitos do tipo Seniors e Senior60** no sistema **TDMax Gerencial**. Ele realiza login no sistema, verifica a data do último uso do cartão e atualiza o vencimento somente para usuários com movimentação recente (últimos 60 dias).

---

## ⚙️ Funcionalidades

- ✅ Acessa automaticamente o sistema TDMax Gerencial via navegador controlado (Playwright).
- 📅 Verifica a **data do último uso do cartão** para cada código.
- 🔄 Atualiza a **data de vencimento** do cartão para `30/06/2026`, **somente se o uso for recente**.
- 📥 Lê os códigos a partir de um arquivo Excel.
- 📝 Mantém um **log de cadastros atualizados** para evitar duplicações em execuções futuras.
- ⏱ Adiciona um intervalo entre as execuções para evitar sobrecarregar o sistema.

---

## 🗂 Estrutura dos Arquivos

| Arquivo                        | Descrição                                         |
|-------------------------------|---------------------------------------------------|
| `seniors.py`                  | Script principal de automação                     |
| `Relatorio (3).xlsx`          | Planilha com os códigos dos cadastros na coluna D |
| `cadastros_atualizados.txt`   | Log dos códigos já atualizados                    |

---

## 🛠 Requisitos

- Python 3.8+
- Bibliotecas Python:
  - `pandas`
  - `playwright`
- Navegadores instalados pelo Playwright:
  ```bash
  playwright install
