import streamlit as st
from supabase import create_client
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

# CONEXÃO COM SUPABASE

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
SENHA_ADMIN = st.secrets["SENHA_ADMIN"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# SALVAR VOTO

def salvar_voto(votante, avaliado, emoji):

    # Remove voto anterior da pessoa
    supabase.table("votos") \
        .delete() \
        .eq("votante", votante) \
        .eq("avaliado", avaliado) \
        .execute()

    # Salva novo voto
    supabase.table("votos").insert({
        "votante": votante,
        "avaliado": avaliado,
        "emoji": emoji,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }).execute()


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

    resposta = (
        supabase
        .table("votos")
        .select("avaliado, emoji")
        .execute()
    )

    resultados = resposta.data


    # RESULTADOS

    st.header("🏆 RESULTADO DO QUERIDÔMETRO")

    for pessoa in MORADORES:

        votos_pessoa = [
            x for x in resultados
            if x["avaliado"] == pessoa
        ]

        st.subheader(
            f"👤 {pessoa}"
        )

        if len(votos_pessoa) == 0:

            st.caption(
                "Nenhum voto ainda."
            )

        else:

            contagem = {}

            for voto in votos_pessoa:

                emoji = voto["emoji"]

                if emoji not in contagem:
                    contagem[emoji] = 0

                contagem[emoji] += 1

            for emoji, quantidade in contagem.items():

                st.write(
                    f"{emoji} × {quantidade}"
                )

        st.divider()


    # TODOS OS VOTOS

    st.header("🕵️ Todos os votos")

    resposta = (
        supabase
        .table("votos")
        .select("votante, avaliado, emoji, data, id")
        .order("id", desc=True)
        .execute()
    )

    todos = resposta.data


    for voto in todos:

        st.write(
            f"**{voto['votante']}** → "
            f"{voto['emoji']} → "
            f"**{voto['avaliado']}**"
        )

        st.caption(
            voto["data"]
        )
