from playwright.sync_api import sync_playwright
from time import sleep as espera


# Solicitar dados do usuário
usuario_login = input("Digite seu usuário do Instagram: ")
senha = input("Digite sua senha do Instagram: ")
endereco = input("Digite o endereço completo da lista de usuários: ")


with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)  # Modo visível para depuração
    pagina = navegador.new_page()

    # Acessar a página de login
    pagina.goto("https://www.instagram.com/")
    pagina.fill('xpath=//*[@id="loginForm"]/div/div[1]/div/label/input', usuario_login)
    pagina.fill('xpath=//*[@id="loginForm"]/div/div[2]/div/label/input', senha)
    pagina.locator('xpath=//*[@id="loginForm"]/div/div[3]/button').click()

    # Aguarda o carregamento da página principal
    espera(5)
    print("Login realizado com sucesso!")

    # Navega até o perfil do usuário

    pagina.goto(f"https://www.instagram.com/{endereco}/")
    espera(5)
    # Acessar a lista de "Seguindo"
    pagina.locator('xpath=//a[contains(@href, "/following/")]').click()
    espera(5)
    print("Acessou a lista de 'Seguindo'!")

    # Iterar pela lista e parar de seguir
    while True:
        # Localizar os botões "Seguindo"
        botoes_seguindo = pagina.locator("button:has-text('Seguindo')")

        # Contar quantos botões estão visíveis
        total_botoes = botoes_seguindo.count()
        if total_botoes == 0:
            print("Não há mais contas para parar de seguir.")
            break

        for i in range(total_botoes):
            try:
                # Clica no botão "Seguindo"
                botoes_seguindo.nth(i).click()
                espera(2)

                # Confirma o "Deixar de seguir"
                botao_confirmar = pagina.locator("button:has-text('Deixar de seguir')")
                if botao_confirmar.is_visible():
                    botao_confirmar.click()
                    espera(2)
                    print(f"Parou de seguir o {i + 1}º perfil.")
            except Exception as e:
                print(f"Erro ao parar de seguir: {e}")

        # Rola para baixo para carregar mais itens
        pagina.evaluate("window.scrollBy(0, 500)")
        espera(2)
