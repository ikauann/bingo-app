# streamlit_app.py

import random
import os
import re
import io
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

st.set_page_config(page_title="Bingo Generator", page_icon="🎯")
st.title("🎯 Gerador de Cartela de Bingo")

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

# Desenha a cartela principal e instruções
def desenhar_cartela(c, cartela, id_jogador, nome, email):
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 800, f"Jogador / jugador {id_jogador}: {nome}")
    c.setFont("Helvetica", 12)
    c.drawString(100, 780, f"E-mail: {email}")

    letras = "BINGO"
    tamanho_celula = 60
    x_inicial = (595 - tamanho_celula * 5) // 2
    y_inicial = 700

    c.setFont("Helvetica-Bold", 20)
    for i, letra in enumerate(letras):
        x = x_inicial + i * tamanho_celula
        y = y_inicial
        c.rect(x, y, tamanho_celula, tamanho_celula)
        c.drawCentredString(x + tamanho_celula / 2, y + 20, letra)

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
                    tamanho_img = 40
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

    y_instrucao_pt = 270
    y_instrucao_es = 130

    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_instrucao_pt + 110, "🎯 COMO GANHAR NO BINGO / CÓMO GANAR EN EL BINGO:")

    x_texto = 70
    x_base = 130
    espaco_bingo = 60 + 40

    c.setFont("Helvetica", 11)
    c.drawString(x_texto, y_instrucao_pt + 25, "PT-BR:")

    preenchidos_coluna = [(i, 0) for i in range(5)]
    preenchidos_L = [(i, 0) for i in range(5)] + [(4, j) for j in range(1, 5)]
    preenchidos_total = [(i, j) for i in range(5) for j in range(5)]

    desenhar_mini_bingo(c, x_base, y_instrucao_pt, preenchidos_coluna, "Coluna ou linha\ncompleta", (0.0, 0.6, 0.0))
    desenhar_mini_bingo(c, x_base + espaco_bingo, y_instrucao_pt, preenchidos_L, "Formato em L\nL invertido também", (1.0, 0.5, 0.0))
    desenhar_mini_bingo(c, x_base + espaco_bingo * 2, y_instrucao_pt, preenchidos_total, "Cartela completa", (0.0, 0.4, 0.8))

    c.setFont("Helvetica", 11)
    c.drawString(x_texto, y_instrucao_es + 25, "ES:")

    desenhar_mini_bingo(c, x_base, y_instrucao_es, preenchidos_coluna, "Columna o línea\ncompleta", (0.0, 0.6, 0.0))
    desenhar_mini_bingo(c, x_base + espaco_bingo, y_instrucao_es, preenchidos_L, "Forma de L\nTambién en espejo", (1.0, 0.5, 0.0))
    desenhar_mini_bingo(c, x_base + espaco_bingo * 2, y_instrucao_es, preenchidos_total, "Cartón completo", (0.0, 0.4, 0.8))

    c.setFont("Helvetica-Oblique", 10)
    c.drawRightString(550, 820, "Developed by Kauan Souza HR S&S")

# Streamlit interface
nome = st.text_input("Seu nome")
email = st.text_input("Seu email")

if st.button("🎫 Gerar Cartela de Bingo"):
    if nome and email:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        cartela = gerar_cartela()
        desenhar_cartela(c, cartela, 1, nome, email)
        c.showPage()
        c.save()

        buffer.seek(0)
        st.success("✅ Cartela gerada com sucesso!")
        st.download_button(
            label="📥 Baixar Cartela PDF",
            data=buffer,
            file_name=f"bingo_{nome.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Por favor, preencha nome e email.")
