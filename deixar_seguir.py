from playwright.sync_api import sync_playwright
from time import sleep as espera
import os
import json
import random

# Instruções
print("Este programa irá parar de seguir perfis listados em um arquivo JSON exportado do Instagram.")
print(r"Informe o caminho completo do arquivo JSON. Exemplo: C:\Users\stach\OneDrive\Documentos\following_list.json")

# Solicitar dados do usuário
usuario_login = input("Digite seu usuário do Instagram: ")
senha = input("Digite sua senha do Instagram: ")
endereco = input("Digite o caminho completo do arquivo JSON: ")

# Verificar se o arquivo existe
if not os.path.exists(endereco):
    print("O arquivo fornecido não existe. Verifique o caminho e tente novamente.")
    exit()

# Ler o JSON
try:
    with open(endereco, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if "relationships_following" not in dados or not isinstance(dados["relationships_following"], list):
        print("O arquivo JSON deve conter uma chave 'relationships_following' com uma lista de usuários.")
        exit()

    usuarios = [item["string_list_data"][0]["value"] for item in dados["relationships_following"] if
                "string_list_data" in item and item["string_list_data"]]
except Exception as e:
    print(f"Erro ao ler o arquivo JSON: {e}")
    exit()

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=True)
    pagina = navegador.new_page()

    # Acessar a página de login
    pagina.goto("https://www.instagram.com/")
    pagina.fill('xpath=//*[@id="loginForm"]/div/div[1]/div/label/input', usuario_login)
    pagina.fill('xpath=//*[@id="loginForm"]/div/div[2]/div/label/input', senha)
    pagina.locator('xpath=//*[@id="loginForm"]/div/div[3]/button').click()

    # Aguarda carregamento
    espera(10)
    print("Login realizado com sucesso!")

    for usuario in usuarios:
        try:
            print(f"Acessando o perfil de {usuario}...")
            pagina.goto(f"https://www.instagram.com/{usuario}/")
            pagina.wait_for_selector("header", timeout=10000)

            # Verifica se já está seguindo
            botao_deixar_de_seguir = pagina.locator("button:has-text('Seguindo')")
            if botao_deixar_de_seguir.count() > 0 and botao_deixar_de_seguir.nth(0).is_visible():
                botao_deixar_de_seguir.nth(0).click()
                espera(random.uniform(2, 5))  # Aguardar antes de confirmar

                # Confirmar ação
                botao_confirmar = pagina.locator("button:has-text('Deixar de seguir')")
                if botao_confirmar.count() > 0:
                    botao_confirmar.nth(0).click()
                    print(f"Deixou de seguir {usuario}.")
                else:
                    print(f"Erro ao encontrar o botão de confirmação para {usuario}.")
            else:
                print(f"Já não segue {usuario} ou botão não encontrado.")

        except Exception as e:
            print(f"Erro ao processar {usuario}: {e}")

        espera(random.uniform(5, 10))  # Evitar bloqueios

    navegador.close()
    print("Processo concluído.")
