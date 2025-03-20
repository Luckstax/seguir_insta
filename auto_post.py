import os
from instagrapi import Client

def postar_imagens(folder_path, usuario, senha):
    client = Client()
    try:
        client.login(usuario, senha)
    except Exception as e:
        print(f"Erro no login: {e}")
        return

    for arquivo in os.listdir(folder_path):
        if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            caminho_imagem = os.path.join(folder_path, arquivo)
            legenda = os.path.splitext(arquivo)[0]  # nome sem extensão
            try:
                client.photo_upload(caminho_imagem, legenda)
                print(f"Imagem postada com sucesso: {arquivo}")

                # 🔥 Excluir a imagem após o upload bem-sucedido
                os.remove(caminho_imagem)

            except Exception as e:
                print(f"Erro ao postar {arquivo}: {e}")

if __name__ == '__main__':
    pasta_imagens = input("Digite o caminho completo do arquivo JSON: ")
    usuario = input("Digite seu usuário do Instagram: ")
    senha = input("Digite sua senha do Instagram: ")

    postar_imagens(pasta_imagens, usuario, senha)
