import streamlit as st
import sqlite3
from datetime import datetime

# CONFIGURAÇÃO

st.set_page_config(
    page_title="Queridômetro da Rep",
    page_icon="🏠",
    layout="centered"
)

MORADORES = [
    "Leozinho",
    "John",
    "RG",
    "Liminha",
    "Radinho",
    "Oscar",
    "Breno",
    "Selico",
    "Phineas",
    "Hélice",
    "Herbs",
    "Hec",
    "Tigrão",
    "Shaki",
]

EMOJIS = {
    "❤️ Coração": "❤️",
    "🥰 Adoro": "🥰",
    "👀 Observando": "👀",
    "🤝 Aliado": "🤝",
    "🐍 Cobra": "🐍",
    "🎯 Alvo": "🎯",
    "🤡 Mala": "🤡",
    "💀 Ranço": "💀",
    "🍪 Biscoito": "🍪",
    "💣 Bomba": "💣"
}

SENHA_ADMIN = "rep2026"

#BANCO DE DADOS
def conectar():
    return sqlite3.connect("queridometro.db")


def criar_banco():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            votante TEXT,
            avaliado TEXT,
            emoji TEXT,
            data TEXT
        )
    """)

    conexao.commit()
    conexao.close()


criar_banco()

# SALVAR VOTO

def salvar_voto(votante, avaliado, emoji):

    conexao = conectar()
    cursor = conexao.cursor()

    # Remove voto anterior da pessoa
    cursor.execute("""
        DELETE FROM votos
        WHERE votante = ? AND avaliado = ?
    """, (votante, avaliado))

    # Salva novo voto
    cursor.execute("""
        INSERT INTO votos
        (votante, avaliado, emoji, data)
        VALUES (?, ?, ?, ?)
    """, (
        votante,
        avaliado,
        emoji,
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ))

    conexao.commit()
    conexao.close()



# INTERFACE

st.title("🏠 QUERIDÔMETRO DA OUR")

st.markdown(
    "### 💌 O que tá achando dos ours hoje?"
)

st.divider()



# IDENTIFICAÇÃO

votante = st.selectbox(
    "👤 Quem é você?",
    ["Selecione seu nome"] + MORADORES
)


if votante != "Selecione seu nome":

    st.success(
        f"Olá, {votante}! 💋"
    )

    st.write(
        "Escolha um emoji para cada morador."
    )

    st.divider()

    votos = {}

    for pessoa in MORADORES:

        if pessoa != votante:

            st.subheader(
                f"👤 {pessoa}"
            )

            escolha = st.radio(
                f"Como você está com {pessoa}?",
                ["Não votar"] + list(EMOJIS.keys()),
                horizontal=True,
                key=f"{votante}_{pessoa}"
            )

            if escolha != "Não votar":

                votos[pessoa] = EMOJIS[escolha]

            st.divider()


    # ENVIAR

    if st.button(
        "💌 ENVIAR QUERIDÔMETRO",
        use_container_width=True
    ):

        if len(votos) == 0:

            st.warning(
                "Você não escolheu nenhum emoji."
            )

        else:

            for pessoa, emoji in votos.items():

                salvar_voto(
                    votante,
                    pessoa,
                    emoji
                )

            st.success(
                "💌 Seus votos foram registrados!"
            )

            st.balloons()


# RESULTADOS


st.divider()

st.header("🔐 Área secreta")

senha = st.text_input(
    "Senha do administrador:",
    type="password"
)


if senha == SENHA_ADMIN:

    st.success("Acesso liberado!")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            avaliado,
            emoji,
            COUNT(*)
        FROM votos
        GROUP BY avaliado, emoji
        ORDER BY avaliado
    """)

    resultados = cursor.fetchall()

    conexao.close()


    # RESULTADOS


    st.header("🏆 RESULTADO DO QUERIDÔMETRO")

    for pessoa in MORADORES:

        votos_pessoa = [
            x for x in resultados
            if x[0] == pessoa
        ]

        st.subheader(
            f"👤 {pessoa}"
        )

        if len(votos_pessoa) == 0:

            st.caption(
                "Nenhum voto ainda."
            )

        else:

            for _, emoji, quantidade in votos_pessoa:

                st.write(
                    f"{emoji} × {quantidade}"
                )

        st.divider()

    # TODOS OS VOTOS

    st.header("🕵️ Todos os votos")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            votante,
            avaliado,
            emoji,
            data
        FROM votos
        ORDER BY id DESC
    """)

    todos = cursor.fetchall()

    conexao.close()


    for votante, avaliado, emoji, data in todos:

        st.write(
            f"**{votante}** → {emoji} → **{avaliado}**"
        )

        st.caption(data)
