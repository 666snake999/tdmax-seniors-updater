import pandas as pd
from playwright.sync_api import sync_playwright, Route
from datetime import datetime, timedelta
import time
import os

# === CONFIGURAÇÕES ===
USUARIO = "higor.grande"
SENHA = "h1g0r1312@Foztrans"
ARQUIVO_EXCEL = "Relatorio (3).xlsx"
ARQUIVO_LOG = "cadastros_atualizados.txt"
INTERVALO_ENTRE_CADASTROS = 1.5  # segundos

# === BLOQUEAR RECURSOS DESNECESSÁRIOS (CSS, imagens etc.) ===
def bloquear_recursos(route: Route):
    if route.request.resource_type in ["stylesheet", "image", "font"]:
        route.abort()
    else:
        route.continue_()

# === LER PLANILHA COM OS CÓDIGOS ===
df = pd.read_excel(ARQUIVO_EXCEL)
codigos = df.iloc[:, 3].dropna().apply(lambda x: str(int(float(x))))

# === LER LOG EXISTENTE PARA PULAR CÓDIGOS JÁ FEITOS ===
if os.path.exists(ARQUIVO_LOG):
    with open(ARQUIVO_LOG, "r") as f:
        codigos_feitos = set(l.strip() for l in f.readlines() if l.strip().isdigit())
else:
    codigos_feitos = set()

# === ABRIR O LOG PARA CONTINUAR ESCREVENDO ===
log = open(ARQUIVO_LOG, "a")

# === FUNÇÃO DE ATUALIZAÇÃO COM VERIFICAÇÃO DE USO RECENTE ===
def atualizar_vencimento(pagina, codigo):
    try:
        print(f"\n🔍 Verificando uso recente do código: {codigo}")

        # Acessa o menu "REEMBOLSO DE CRÉDITOS"
        pagina.click("#ctl00_menuSite_gvFavoritos_ctl06_HyperLink1")
        pagina.wait_for_selector("#ctl00_cphconteudo_UcBuscaCadastro1_txtBusca", timeout=10000)

        # Busca pelo código
        campo_busca = "#ctl00_cphconteudo_UcBuscaCadastro1_txtBusca"
        pagina.fill(campo_busca, codigo)
        pagina.once("dialog", lambda d: d.accept())
        pagina.press(campo_busca, "Enter")

        # Lê a data do último uso
        pagina.wait_for_selector("#ctl00_cphconteudo_gvMovimentos_ctl02_Label1", timeout=10000)
        data_uso_str = pagina.query_selector("#ctl00_cphconteudo_gvMovimentos_ctl02_Label1").inner_text().strip()
        data_uso = datetime.strptime(data_uso_str.split()[0], "%d/%m/%Y")

        # Verifica se o uso foi recente (menos de 60 dias)
        if data_uso < datetime.today() - timedelta(days=60):
            print(f"⏳ Código {codigo}: uso antigo. Último uso em {data_uso_str}. Pulando atualização.")
            return

        print(f"✅ Código {codigo}: uso recente (último uso em {data_uso_str}). Atualizando.")

        # Vai para a tela de edição
        pagina.click("#ctl00_menuSite_gvFavoritos_ctl05_HyperLink1")
        pagina.wait_for_selector("#ctl00_cphconteudo_txtCadastroID", timeout=10000)

        pagina.fill("#ctl00_cphconteudo_txtCadastroID", codigo)
        pagina.once("dialog", lambda d: d.accept())
        pagina.click("#ctl00_cphconteudo_btnBuscar")

        # Atualiza o campo de vencimento do cartão
        venc_selector = "#ctl00_cphconteudo_fvCadastro_UcCadastros1_txtVencimentoCartao"
        pagina.wait_for_selector(venc_selector, timeout=15000)
        pagina.click(venc_selector)
        pagina.press(venc_selector, "Control+A")
        pagina.type(venc_selector, "31052026")
        pagina.click("#ctl00_cphconteudo_btnSalvar")

        # Registra no log
        log.write(f"{codigo}\n")
        log.flush()

        print(f"✅ Código {codigo} atualizado com sucesso.")
        time.sleep(INTERVALO_ENTRE_CADASTROS)

    except Exception as e:
        print(f"⚠️ Erro ao processar código {codigo}: {e}")

# === EXECUÇÃO PRINCIPAL ===
def main():
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)
        pagina = navegador.new_page()
        pagina.route("**/*", bloquear_recursos)

        pagina.goto("https://max00087.itstransdata.com/TDMax/Default.aspx?ReturnUrl=%2fTDMax%2fLocalizarCadastro.aspx")
        pagina.fill("#ctl00_cphconteudo_login_UserName", USUARIO)
        pagina.fill("#ctl00_cphconteudo_login_Password", SENHA)
        pagina.click("#ctl00_cphconteudo_login_LoginButton")

        pagina.wait_for_selector("#ctl00_menuSite_gvFavoritos_ctl05_HyperLink1")

        for codigo in codigos:
            if codigo in codigos_feitos:
                print(f"⏭️ Código {codigo} já estava processado. Pulando.")
                continue
            atualizar_vencimento(pagina, codigo)

        navegador.close()
        log.close()
        print("\n🏁 Processo finalizado. Veja o log em 'cadastros_atualizados.txt'.")

if __name__ == "__main__":
    main()
