import random
import os
import zipfile
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
import win32com.client

# Gera os números da cartela
def gerar_cartela():
    cartela = {
        'B': random.sample(range(1, 16), 5),
        'I': random.sample(range(16, 31), 5),
        'N': random.sample(range(31, 46), 5),
        'G': random.sample(range(46, 61), 5),
        'O': random.sample(range(61, 76), 5)
    }
    cartela['N'][2] = 'X'
    return cartela

# Desenha mini cartelas visuais com cores
def desenhar_mini_bingo(c, x_inicial, y_inicial, preenchidos, titulo, cor_rgb):
    tamanho = 12
    linhas_titulo = titulo.split("\n")
    for i, linha in enumerate(linhas_titulo):
        c.setFont("Helvetica", 9)
        c.drawString(x_inicial, y_inicial + tamanho * 6 + 5 - (12 * i), linha)

    cor = Color(*cor_rgb)
    for linha in range(5):
        for coluna in range(5):
            x = x_inicial + coluna * tamanho
            y = y_inicial + (4 - linha) * tamanho
            c.rect(x, y, tamanho, tamanho)
            if (linha, coluna) in preenchidos:
                c.setFillColor(cor)
                c.rect(x, y, tamanho, tamanho, fill=1)
                c.setFillColorRGB(0, 0, 0)

# Desenha a cartela principal e as instruções
def desenhar_cartela(c, cartela, id_jogador, nome, email):
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 800, f"Jogador / jugador {id_jogador}: {nome}")
    c.setFont("Helvetica", 12)
    c.drawString(100, 780, f"E-mail: {email}")

    letras = "BINGO"
    tamanho_celula = 60
    x_inicial = (595 - tamanho_celula * 5) // 2  # Centralizado
    y_inicial = 700

    # Cabeçalho BINGO
    c.setFont("Helvetica-Bold", 20)
    for i, letra in enumerate(letras):
        x = x_inicial + i * tamanho_celula
        y = y_inicial
        c.rect(x, y, tamanho_celula, tamanho_celula)
        c.drawCentredString(x + tamanho_celula / 2, y + 20, letra)

    # Números com bordas
    c.setFont("Helvetica", 18)
    for linha in range(5):
        for coluna, letra in enumerate(letras):
            valor = cartela[letra][linha]
            x = x_inicial + coluna * tamanho_celula
            y = y_inicial - (linha + 1) * tamanho_celula
            c.rect(x, y, tamanho_celula, tamanho_celula)

            if valor == 'X':
                caminho_imagem = "syngenta_png.png"
                if os.path.exists(caminho_imagem):
                    tamanho_img = 40  # ajuste o tamanho da imagem conforme necessário
                    c.drawImage(
                        caminho_imagem,
                        x + (tamanho_celula - tamanho_img) / 2,
                        y + (tamanho_celula - tamanho_img) / 2,
                        width=tamanho_img,
                        height=tamanho_img,
                        preserveAspectRatio=True,
                        mask='auto'
                    )
                else:
                    c.drawCentredString(x + tamanho_celula / 2, y + 20, "X")
            else:
                texto = str(valor).rjust(2)
                c.drawCentredString(x + tamanho_celula / 2, y + 20, texto)

    # Instruções visuais
    # Instruções visuais multilíngue
    y_instrucao_pt = 270
    y_instrucao_es = 130

    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_instrucao_pt + 110, "🎯 COMO GANHAR NO BINGO / CÓMO GANAR EN EL BINGO:")

    x_texto = 70  # alinhamento do "PT-BR:" e "ES:"
    x_base = 130  # onde começam os mini bingos
    espaco_bingo = 60 + 40  # largura de um bingo + espaço

    # --- Linha PT-BR ---
    c.setFont("Helvetica", 11)
    c.drawString(x_texto, y_instrucao_pt + 25, "PT-BR:")

    preenchidos_coluna = [(i, 0) for i in range(5)]
    preenchidos_L = [(i, 0) for i in range(5)] + [(4, j) for j in range(1, 5)]
    preenchidos_total = [(i, j) for i in range(5) for j in range(5)]

    desenhar_mini_bingo(c, x_base, y_instrucao_pt, preenchidos_coluna, "Coluna ou linha\ncompleta", (0.0, 0.6, 0.0))
    desenhar_mini_bingo(c, x_base + espaco_bingo, y_instrucao_pt, preenchidos_L, "Formato em L\nL invertido também", (1.0, 0.5, 0.0))
    desenhar_mini_bingo(c, x_base + espaco_bingo * 2, y_instrucao_pt, preenchidos_total, "Cartela completa", (0.0, 0.4, 0.8))

    # --- Linha ES ---
    c.setFont("Helvetica", 11)
    c.drawString(x_texto, y_instrucao_es + 25, "ES:")

    desenhar_mini_bingo(c, x_base, y_instrucao_es, preenchidos_coluna, "Columna o línea\ncompleta", (0.0, 0.6, 0.0))
    desenhar_mini_bingo(c, x_base + espaco_bingo, y_instrucao_es, preenchidos_L, "Forma de L\nTambién en espejo", (1.0, 0.5, 0.0))
    desenhar_mini_bingo(c, x_base + espaco_bingo * 2, y_instrucao_es, preenchidos_total, "Cartón completo", (0.0, 0.4, 0.8))

    # Rodapé com autor
    c.setFont("Helvetica-Oblique", 10)
    c.drawRightString(550, 820, "Developed by Kauan Souza HR S&S")

# Gera PDF individual
def gerar_pdf_individual(jogador_id, nome, email):
    cartela = gerar_cartela()
    nome_limpo = re.sub(r'[^a-zA-Z0-9_]', '', nome.replace(" ", "_"))
    filename = f"{nome_limpo}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    desenhar_cartela(c, cartela, jogador_id, nome, email)
    c.showPage()
    c.save()
    return filename

# Compacta PDFs em zip
def compactar_pdfs(lista_arquivos, nome_arquivo_zip="cartelas_bingo.zip"):
    with zipfile.ZipFile(nome_arquivo_zip, 'w') as zipf:
        for arquivo in lista_arquivos:
            zipf.write(arquivo)
    print(f"✅ Arquivo ZIP gerado: {nome_arquivo_zip}")

# Remove PDFs depois de usar
def limpar_pdfs(lista_arquivos):
    for arquivo in lista_arquivos:
        os.remove(arquivo)

# Lê os jogadores do txt
def ler_jogadores_de_txt(nome_arquivo):
    jogadores = []
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha and "," in linha:
                nome, email = linha.split(",", 1)
                jogadores.append({"nome": nome.strip(), "email": email.strip()})
    return jogadores

# Envia email com Outlook
def enviar_email_outlook(nome, destinatario, caminho_anexo):
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = destinatario
        mail.Subject = "Sua Cartela de Bingo 🎉"
        mail.Body = f"Olá {nome},\n\nSegue em anexo sua cartela de bingo!\n\nBoa sorte! 🍀 \n\n🎯 Developed by Kauan Souza HR S&S\n"
        mail.Attachments.Add(os.path.abspath(caminho_anexo))
        mail.Send()
        print("Email enviado com sucesso!")
    except Exception as e:
        print("Erro:", e)

# Função principal
def main():
    print("\n🎯 Developed by Kauan Souza HR S&S\n")

    jogadores = ler_jogadores_de_txt("jogadores.txt")
    arquivos_pdfs = []

    for i, jogador in enumerate(jogadores, start=1):
        print(f"Gerando cartela para {jogador['nome']}...")
        pdf = gerar_pdf_individual(i, jogador['nome'], jogador['email'])
        arquivos_pdfs.append(pdf)
        print(f"Cartela gerada: {pdf}")
        print(f"Enviando e-mail para {jogador['email']}...")
        enviar_email_outlook(jogador['nome'], jogador['email'], pdf)
        print(f"Enviado! Apagando arquivo {pdf}")
    
    compactar_pdfs(arquivos_pdfs)
    limpar_pdfs(arquivos_pdfs)

if __name__ == "__main__":
    main()
