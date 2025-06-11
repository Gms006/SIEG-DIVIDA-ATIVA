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

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def login(page):
    await page.goto(LOGIN_URL)
    await page.fill("#txtEmail", EMAIL)
    await page.fill("#txtPassword", PASSWORD)
    await page.click("#btnSubmit")
    await page.wait_for_load_state("networkidle")

async def selecionar_empresa(page):
    input_cnpj = page.locator("input.multiselect__input")
    await input_cnpj.fill(CNPJ)
    await input_cnpj.press("Enter")
    await page.wait_for_selector(f"span.hidden.xl\\:inline-block:text('({CNPJ})')")

async def abrir_detalhes_dividas(page):
    await page.click("span.pill-alert.pill.cursor-pointer")
    await page.wait_for_selector("a[id^='btnDownload-']")

async def salvar_pdf(inscricao):
    # Aguarda a janela "Salvar como" aparecer
    time.sleep(2)
    file_name = f"divida_{CNPJ}_{inscricao}.pdf"
    path = os.path.join(DOWNLOAD_DIR, file_name)
    pyautogui.write(path)
    pyautogui.press('enter')
    logging.info(f"Salvo: {path}")

async def baixar_detalhes(page):
    while True:
        links = page.locator("a[id^='btnDownload-']")
        count = await links.count()
        for i in range(count):
            await links.nth(i).click()
            await page.wait_for_selector("div[role='button']:has-text('Imprimir')")
            await page.click("div[role='button']:has-text('Imprimir')")
            inscricao = await page.locator("h5:has-text('N° inscrição') span").inner_text()
            inscricao = inscricao.replace(' ', '').replace('-', '')
            try:
                await salvar_pdf(inscricao)
            except Exception as e:
                logging.error(f"Falha ao salvar {inscricao}: {e}")
            await page.keyboard.press('Escape')
            await page.wait_for_timeout(1000)
        next_btn = page.locator("ul.pagination a[data-dt-idx='next']:not(.disabled)")
        if await next_btn.count() == 0:
            break
        await next_btn.click()
        await page.wait_for_load_state('networkidle')

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
        finally:
            await context.close()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
