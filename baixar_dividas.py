import asyncio
from playwright.async_api import async_playwright
import pyautogui
import time
import logging
import os

LOGIN_URL = "https://iris.sieg.com/DividaAtiva"
EMAIL = "contabil2@netocontabilidade.com.br"
PASSWORD = "Brasil*123"
CNPJ = "10608734000101"
DOWNLOAD_DIR = r"G:\\EMPRESAS\\GREEN AMBIENTAL LTDA\\Contabilidade\\Conferências\\Débitos Federais\\PGFN"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("baixar_dividas")

async def login(page):
    logger.info("Acessando %s", LOGIN_URL)
    await page.goto(LOGIN_URL)
    logger.info("Preenchendo e-mail e senha")
    await page.fill("#txtEmail", EMAIL)
    await page.fill("#txtPassword", PASSWORD)
    await page.click("#btnSubmit")
    logger.info("Enviado login, aguardando redirecionamento")
    try:
        await page.wait_for_load_state("networkidle", timeout=60000)
    except Exception as e:
        logger.error("Timeout ao aguardar carga inicial: %s", e)
        await page.screenshot(path="login_error.png")
        raise

    logger.info("URL atual apos login: %s", page.url)
    if "/home" in page.url:
        logger.info("Redirecionado para home, navegando para Divida Ativa")
        await page.goto(LOGIN_URL)
        await page.wait_for_load_state("networkidle")

async def selecionar_empresa(page):
    logger.info("Selecionando empresa %s", CNPJ)
    input_cnpj = page.locator("input.multiselect__input")
    await input_cnpj.fill(CNPJ)
    await input_cnpj.press("Enter")
    await page.wait_for_selector(f"span.hidden.xl\\:inline-block:text('({CNPJ})')", timeout=60000)
    logger.info("Empresa selecionada")

async def abrir_detalhes_dividas(page):
    logger.info("Abrindo lista de dívidas")
    await page.click("span.pill-alert.pill.cursor-pointer")
    await page.wait_for_selector("a[id^='btnDownload-']", timeout=60000)
    logger.info("Lista carregada")

async def salvar_pdf(inscricao):
    # Aguarda a janela "Salvar como" aparecer
    time.sleep(2)
    file_name = f"divida_{CNPJ}_{inscricao}.pdf"
    path = os.path.join(DOWNLOAD_DIR, file_name)
    logger.info("Salvando PDF: %s", path)
    pyautogui.write(path)
    pyautogui.press("enter")
    logger.info("Arquivo salvo")

async def baixar_detalhes(page):
    page_num = 1
    while True:
        logger.info("Processando página %s", page_num)
        links = page.locator("a[id^='btnDownload-']")
        count = await links.count()
        logger.info("Encontrados %s itens para download", count)
        for i in range(count):
            logger.info("Baixando item %s/%s", i + 1, count)
            await links.nth(i).click()
            await page.wait_for_selector("div[role='button']:has-text('Imprimir')", timeout=60000)
            await page.click("div[role='button']:has-text('Imprimir')")
            inscricao = await page.locator("h5:has-text('N° inscrição') span").inner_text()
            inscricao = inscricao.replace(' ', '').replace('-', '')
            try:
                await salvar_pdf(inscricao)
            except Exception as e:
                logger.error("Falha ao salvar %s: %s", inscricao, e)
            await page.keyboard.press('Escape')
            await page.wait_for_timeout(1000)
        next_btn = page.locator("ul.pagination a[data-dt-idx='next']:not(.disabled)")
        if await next_btn.count() == 0:
            logger.info("Não há mais páginas")
            break
        logger.info("Avançando para a próxima página")
        await next_btn.click()
        await page.wait_for_load_state("networkidle")
        page_num += 1

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await login(page)
            await selecionar_empresa(page)
            await abrir_detalhes_dividas(page)
            await baixar_detalhes(page)
        except Exception as e:
            logger.exception("Erro durante execução: %s", e)
            await page.screenshot(path="erro_execucao.png")
            raise
        finally:
            await context.close()
            await browser.close()

if __name__ == "__main__":
    logger.info("Iniciando automação")
    asyncio.run(main())
