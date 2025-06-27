from playwright.sync_api import sync_playwright
from openpyxl import Workbook

def verificar_linkedin_em_pagina(page):
    page.wait_for_timeout(2000)
    linkedin = None

    site_pessoal = page.locator("li[itemprop='url'] a")
    if site_pessoal.count() > 0:
        href = site_pessoal.first.get_attribute("href")
        if href and "linkedin.com" in href.lower():
            linkedin = href

    if not linkedin:
        todos_links = page.locator("a")
        for j in range(todos_links.count()):
            href = todos_links.nth(j).get_attribute("href")
            if href and "linkedin.com" in href.lower():
                linkedin = href
                break
    return linkedin

def buscar_perfis_xpath(start_page, end_page, headless=True):
    resultados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        for pagina in range(start_page, end_page + 1):
            url = f"https://github.com/search?q=location%3A%22S%C3%A3o+Paulo%22+++language%3AJava+is%3Apublic+sort%3Astars&type=users&p={pagina}"
            print(f"[+] Acessando página {pagina}...")
            page.goto(url)
            page.wait_for_timeout(3000)

            # Captura o número de spans clicáveis (nome dos perfis)
            qtd_perfis = len(page.locator("//span[@class='Box-sc-g0xbh4-0 hYFqef prc-Text-Text-0ima0']").all())
            print(f"    -> {qtd_perfis} perfis clicáveis encontrados")

            for i in range(qtd_perfis):
                try:
                    # Re-obtem o elemento no índice atual (evita stale element)
                    span = page.locator("//span[@class='Box-sc-g0xbh4-0 hYFqef prc-Text-Text-0ima0']").nth(i)
                    # O pai do span é o <a> que queremos clicar
                    link = span.locator("..")  # sobe para o pai <a>

                    href = link.get_attribute("href")
                    print(f"    ➜ Clicando no perfil: {href}")

                    link.click()
                    page.wait_for_timeout(3000)

                    linkedin = verificar_linkedin_em_pagina(page)

                    if linkedin:
                        github_url = page.url
                        print(f"        ✅ LinkedIn encontrado: {linkedin}")
                        resultados.append((github_url, linkedin))
                    else:
                        print("        🔍 Nenhum LinkedIn encontrado.")

                    page.go_back()
                    page.wait_for_timeout(3000)

                except Exception as e:
                    print(f"        ⚠️ Erro ao processar perfil na posição {i}: {e}")
                    page.go_back()
                    page.wait_for_timeout(3000)

        browser.close()
    return resultados

def salvar_em_excel(resultados):
    wb = Workbook()
    ws = wb.active
    ws.title = "Perfis com LinkedIn"
    ws.append(["GitHub", "LinkedIn"])
    for github_url, linkedin_url in resultados:
        ws.append([github_url, linkedin_url])
    wb.save("perfis_com_linkedin.xlsx")
    wb.save("perfis_com_linkedin.csv")
    print("\n[✓] Arquivo Excel gerado: perfis_com_linkedin.xlsx")
    print("\n[✓] Arquivo Excel gerado: perfis_com_linkedin.csv")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scraper GitHub por XPath dos perfis")
    parser.add_argument("--start", type=int, help="Página inicial")
    parser.add_argument("--end", type=int, help="Página final")
    parser.add_argument("--show", action="store_true", help="Mostrar navegador")

    args = parser.parse_args()
    if args.start is None or args.end is None:
        print("⚠️ Informe --start e --end")
        exit(1)

    resultados = buscar_perfis_xpath(args.start, args.end, headless=not args.show)

    if resultados:
        salvar_em_excel(resultados)
    else:
        print("⚠️ Nenhum perfil com LinkedIn encontrado.")
