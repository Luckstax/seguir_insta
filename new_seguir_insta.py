from playwright.sync_api import sync_playwright
from time import sleep as espera
import os


#instruções
print("O programa foi feito para seguir uma lista de perfis que você tenha salvo em um arquivo .txt.")
print(r"É necessário informar o endereço completo do arquivo. Exemplo:C:\Users\stach\OneDrive\Documentos\@luckstax7.txt")



# Solicitar dados do usuário
usuario_login = input("Digite seu usuário do Instagram: ")
senha = input("Digite sua senha do Instagram: ")
endereco = input("Digite o endereço completo da lista de usuários: ")

# Verificar se o arquivo existe
if not os.path.exists(endereco):
    print("O arquivo fornecido não existe. Verifique o caminho e tente novamente.")
    exit()

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)  # Modo visível para depuração
    pagina = navegador.new_page()

    # Acessar a página de login
    pagina.goto("https://www.instagram.com/")
    pagina.fill('xpath=//*[@id="loginForm"]/div/div[1]/div/label/input', usuario_login)
    pagina.fill('xpath=//*[@id="loginForm"]/div/div[2]/div/label/input', senha)
    pagina.locator('xpath=//*[@id="loginForm"]/div/div[3]/button').click()

    # Aguarda o carregamento da página principal
    espera(15)
    print("Login realizado com sucesso!")

    # Ler a lista de usuários
    with open(endereco, "r", encoding="utf-8") as lista:
        usuarios = [linha.strip() for linha in lista]

        for usuario in usuarios:
            try:
                # Navega até o perfil do usuário
                print(f"Acessando o perfil de {usuario}...")
                pagina.goto(f"https://www.instagram.com/{usuario}/")

                # Aguarda o carregamento da página do perfil
                pagina.wait_for_selector("header", timeout=10000)

                # Localiza todos os botões com texto "Seguir"
                botoes = pagina.locator("button:has-text('Seguir')")

                # Itera sobre os botões encontrados
                for i in range(botoes.count()):
                    botao = botoes.nth(i)
                    if botao.is_visible():
                        botao.click()
                        print(f"Seguiu {usuario} clicando no botão {i}.")
                        break
                else:
                    print(f"Não foi possível encontrar um botão 'Seguir' para {usuario}.")

            except Exception as e:
                print(f"Erro ao processar {usuario}: {e}")

    # Fecha o navegador ao final
    navegador.close()
    #encerramento
    print("Processo concluído.")
    print("Siga no instagram: @luckstax7")
