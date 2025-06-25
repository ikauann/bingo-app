import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color
import random
import re
import os

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

def desenhar_cartela(c, cartela, id_jogador, nome, email):
    letras = "BINGO"
    tamanho_celula = 60
    x_inicial = (595 - tamanho_celula * 5) // 2
    y_inicial = 700

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 800, f"Jogador / jugador {id_jogador}: {nome}")
    c.setFont("Helvetica", 12)
    c.drawString(100, 780, f"E-mail: {email}")

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
                imagem = "syngenta_png.png"
                if os.path.exists(imagem):
                    c.drawImage(imagem, x, y, width=tamanho_celula, height=tamanho_celula, preserveAspectRatio=False, mask='auto')
                else:
                    c.drawCentredString(x + tamanho_celula / 2, y + 20, "X")
            else:
                texto = str(valor).rjust(2)
                c.drawCentredString(x + tamanho_celula / 2, y + 20, texto)

def gerar_pdf_individual(jogador_id, nome, email):
    cartela = gerar_cartela()
    nome_limpo = re.sub(r'[^a-zA-Z0-9_]', '', nome.replace(" ", "_"))
    filename = f"{nome_limpo}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    desenhar_cartela(c, cartela, jogador_id, nome, email)
    c.showPage()
    c.save()
    return filename

# --- INTERFACE WEB COM STREAMLIT ---

st.set_page_config(page_title="Gerador de Bingo", page_icon="🎯")

st.title("🎯 Gerador de Cartelas de Bingo")
st.markdown("Preencha seus dados e baixe sua cartela personalizada!")

nome = st.text_input("Nome do Jogador")
email = st.text_input("E-mail")

if st.button("Gerar Cartela"):
    if not nome or not email:
        st.error("Por favor, preencha nome e email.")
    else:
        st.success("Cartela gerada com sucesso!")
        pdf_arquivo = gerar_pdf_individual(1, nome, email)
        with open(pdf_arquivo, "rb") as f:
            st.download_button(
                label="📥 Baixar PDF da Cartela",
                data=f,
                file_name=pdf_arquivo,
                mime="application/pdf"
            )
        os.remove(pdf_arquivo)  # limpa arquivo gerado depois do download