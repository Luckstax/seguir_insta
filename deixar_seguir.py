from playwright.sync_api import sync_playwright
import json
import time
import os

# Solicitar dados do usuário
usuario_login = input("Digite seu usuário do Instagram: ")
senha = input("Digite sua senha do Instagram: ")
arquivo_json = input("Digite o caminho completo do arquivo JSON: ")

# Verificar se o arquivo existe
if not os.path.exists(arquivo_json):
    print("O arquivo fornecido não existe. Verifique o caminho e tente novamente.")
    exit()

# Carregar lista de usuários do JSON
with open(arquivo_json, "r", encoding="utf-8") as file:
    data = json.load(file)
    usuarios = [item["string_list_data"][0]["value"] for item in data["relationships_following"]]

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    pagina = navegador.new_page()

    # Acessar página de login
    pagina.goto("https://www.instagram.com/")
    pagina.fill('xpath=//*[@id="loginForm"]/div/div[1]/div/label/input', usuario_login)
    pagina.fill('xpath=//*[@id="loginForm"]/div/div[2]/div/label/input', senha)
    pagina.locator('xpath=//*[@id="loginForm"]/div/div[3]/button').click()
    time.sleep(10)
    print("Login realizado com sucesso!")

    for usuario in usuarios:
        try:
            print(f"Acessando o perfil de {usuario}...")
            pagina.goto(f"https://www.instagram.com/{usuario}/")

            # Espera a página carregar
            pagina.wait_for_selector("header", timeout=10000)

            # Localiza botão "Seguindo"
            botao_seguindo = pagina.locator("button:has-text('Seguindo')")

            if botao_seguindo.count() > 0 and botao_seguindo.first.is_visible():
                botao_seguindo.first.click()
                print(f"Abrindo menu para {usuario}...")

                # Espera o pop-up aparecer
                pagina.wait_for_selector("text=Deixar de seguir", timeout=5000)

                # Clica no botão "Deixar de seguir"
                botao_deixar_seguir = pagina.locator("text=Deixar de seguir")
                if botao_deixar_seguir.count() > 0:
                    botao_deixar_seguir.first.click()
                    print(f"Deixou de seguir {usuario}.")
                    time.sleep(3)  # Pequeno delay para evitar bloqueios
                else:
                    print(f"Botão 'Deixar de seguir' não encontrado para {usuario}.")
            else:
                print(f"Botão 'Seguindo' não encontrado para {usuario}, pulando...")

        except Exception as e:
            print(f"Erro ao processar {usuario}: {e}")

    navegador.close()
    print("Processo concluído.")
