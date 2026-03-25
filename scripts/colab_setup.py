import os
import sys

def setup_colab_sync():
    print("🚀 Inciando configuração do ViralVideoCutterHub para Colab...")
    
    try:
        from google.colab import drive
        print("📁 Montando Google Drive...")
        drive.mount('/content/drive')
        
        drive_path = "/content/drive/MyDrive/ViralVideoCutterHub_Results"
        if not os.path.exists(drive_path):
            os.makedirs(drive_path, exist_ok=True)
            print(f"✅ Pasta de resultados criada: {drive_path}")
        else:
            print(f"✅ Pasta de resultados já existe: {drive_path}")
            
        print("\n✨ TUDO PRONTO!")
        print("Agora, quando você rodar o Hub com '--colab', seus vídeos irão direto para o seu Google Drive.")
        print("💡 DICA: Instale o 'Google Drive para Desktop' no seu Windows para os vídeos aparecerem no seu PC na hora!")
        
    except ImportError:
        print("❌ Erro: Este script deve ser executado dentro de um ambiente Google Colab.")
    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")

if __name__ == "__main__":
    setup_colab_sync()
