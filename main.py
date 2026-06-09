import os
import shutil
import platform
import subprocess

ACERVO_DIR = "acervo"

def inicializar():
    """Cria o diretório principal caso não exista."""
    if not os.path.exists(ACERVO_DIR):
        os.makedirs(ACERVO_DIR)

def listar_documentos():
    """Lista todos os documentos digitais, organizados por ano e tipo."""
    print("\n--- Documentos no Acervo ---")
    if not os.path.exists(ACERVO_DIR) or not os.listdir(ACERVO_DIR):
        print("O acervo está vazio.")
        return

    for ano in sorted(os.listdir(ACERVO_DIR)):
        caminho_ano = os.path.join(ACERVO_DIR, ano)
        if os.path.isdir(caminho_ano):
            print(f"\nAno de Publicação: {ano}")
            for tipo in sorted(os.listdir(caminho_ano)):
                caminho_tipo = os.path.join(caminho_ano, tipo)
                if os.path.isdir(caminho_tipo):
                    print(f"  Tipo de Arquivo: {tipo.upper()}")
                    for arquivo in sorted(os.listdir(caminho_tipo)):
                        print(f"    - {arquivo}")

def adicionar_documento():
    """Permite aos bibliotecários adicionarem documentos."""
    caminho_origem = input("Caminho completo do arquivo a ser adicionado: ")
    if not os.path.exists(caminho_origem):
        print("Erro: Arquivo não encontrado.")
        return

    ano = input("Digite o ano de publicação do documento: ")
    nome_arquivo = os.path.basename(caminho_origem)
    extensao = nome_arquivo.split('.')[-1].lower() if '.' in nome_arquivo else 'outros'

    dir_destino = os.path.join(ACERVO_DIR, ano, extensao)
    os.makedirs(dir_destino, exist_ok=True)
    caminho_destino = os.path.join(dir_destino, nome_arquivo)
    
    try:
        shutil.copy(caminho_origem, caminho_destino)
        print(f"Sucesso: Documento adicionado em {caminho_destino}")
    except Exception as e:
        print(f"Erro ao adicionar arquivo: {e}")

def renomear_documento():
    """Permite aos bibliotecários renomearem documentos."""
    listar_documentos()
    caminho_atual = input("\nCaminho atual do arquivo no acervo (ex: acervo/2023/pdf/livro.pdf): ")
    if not os.path.exists(caminho_atual):
        print("Erro: Arquivo não encontrado.")
        return
    
    novo_nome = input("Novo nome do arquivo (com a extensão): ")
    caminho_novo = os.path.join(os.path.dirname(caminho_atual), novo_nome)

    try:
        os.rename(caminho_atual, caminho_novo)
        print(f"Sucesso: Arquivo renomeado para {novo_nome}")
    except Exception as e:
        print(f"Erro ao renomear: {e}")

def remover_documento():
    """Permite aos bibliotecários removerem documentos."""
    listar_documentos()
    caminho = input("\nCaminho do arquivo que deseja remover: ")
    if not os.path.exists(caminho):
        print("Erro: Arquivo não encontrado.")
        return
    
    confirmar = input(f"Tem certeza que deseja apagar {caminho}? (s/n): ")
    if confirmar.lower() == 's':
        try:
            os.remove(caminho)
            print("Sucesso: Arquivo removido.")
        except Exception as e:
            print(f"Erro ao remover: {e}")

def abrir_documento():
    """Permite abrir e ler o arquivo digital no sistema operacional."""
    listar_documentos()
    caminho = input("\nCaminho do arquivo que deseja abrir: ")
    if not os.path.exists(caminho):
        print("Erro: Arquivo não encontrado.")
        return
    
    try:
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', caminho))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(caminho)
        else:                                   # Linux
            subprocess.call(('xdg-open', caminho))
        print("Arquivo aberto com sucesso.")
    except Exception as e:
        print(f"Erro ao abrir arquivo: {e}")

def menu():
    inicializar()
    while True:
        print("\n=== Sistema de Biblioteca Digital ===")
        print("1. Listar Documentos")
        print("2. Adicionar Documento")
        print("3. Renomear Documento")
        print("4. Remover Documento")
        print("5. Abrir/Ler Documento")
        print("6. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1': listar_documentos()
        elif opcao == '2': adicionar_documento()
        elif opcao == '3': renomear_documento()
        elif opcao == '4': remover_documento()
        elif opcao == '5': abrir_documento()
        elif opcao == '6': break
        else: print("Opção inválida.")

if __name__ == "__main__":
    menu()
