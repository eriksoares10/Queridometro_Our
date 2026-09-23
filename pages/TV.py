import streamlit as st
import time
from collections import Counter
from supabase import create_client

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Queridômetro da OUR - TV",
    page_icon="🏠",
    layout="wide"
)

# ============================================================
# CONEXÃO COM SUPABASE
# ============================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ============================================================
# MORADORES
# ============================================================

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

# ============================================================
# CORES / VISUAL
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #101412;
}

.block-container {
    max-width: 1400px;
    padding-top: 30px;
    padding-bottom: 30px;
}

.titulo {
    text-align: center;
    color: #F47B20;
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 2px;
}

.subtitulo {
    text-align: center;
    color: #E8E8E8;
    font-size: 20px;
    margin-bottom: 35px;
}

.nome {
    text-align: center;
    color: white;
    font-size: 58px;
    font-weight: 900;
    margin-top: 15px;
    margin-bottom: 30px;
}

.emoji-area {
    background-color: #1D241F;
    border: 3px solid #F47B20;
    border-radius: 25px;
    padding: 35px;
    text-align: center;
    min-height: 220px;
}

.emoji {
    font-size: 70px;
    margin: 12px;
}

.contador {
    text-align: center;
    color: #A8C99A;
    font-size: 20px;
    margin-top: 25px;
}

.rodape {
    text-align: center;
    color: #777777;
    font-size: 15px;
    margin-top: 35px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="titulo">🏠 QUERIDÔMETRO DA OUR</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">💌 Como os OURs estão sendo vistos hoje?</div>',
    unsafe_allow_html=True
)

# ============================================================
# ESPAÇO DA TELA
# ============================================================

tela = st.empty()

# ============================================================
# FUNÇÃO PARA BUSCAR VOTOS
# ============================================================

def buscar_votos():

    resposta = (
        supabase
        .table("votos")
        .select("avaliado, emoji")
        .execute()
    )

    return resposta.data


# ============================================================
# EXIBIÇÃO
# ============================================================

while True:

    resultados = buscar_votos()

    for pessoa in MORADORES:

        votos_pessoa = [
            voto
            for voto in resultados
            if voto["avaliado"] == pessoa
        ]

        emojis = [
            voto["emoji"]
            for voto in votos_pessoa
        ]

        # Conta quantos recebeu de cada emoji
        contagem = Counter(emojis)

        # Cria lista organizada
        emojis_exibicao = []

        for emoji, quantidade in contagem.items():

            for _ in range(quantidade):
                emojis_exibicao.append(emoji)

        # ----------------------------------------------------
        # MONTA OS EMOJIS
        # ----------------------------------------------------

        if len(emojis_exibicao) == 0:

            emojis_html = """
            <div style="
                color:#777;
                font-size:28px;
                padding:50px;
            ">
                Nenhum voto ainda...
            </div>
            """

        else:

            emojis_html = ""

            for emoji in emojis_exibicao:

                emojis_html += f"""
                <span class="emoji">
                    {emoji}
                </span>
                """

        # ----------------------------------------------------
        # MOSTRA NA TV
        # ----------------------------------------------------

        tela.markdown(
            f"""
            <div class="nome">
                {pessoa}
            </div>

            <div class="emoji-area">
                {emojis_html}
            </div>

            <div class="contador">
                💌 {len(emojis_exibicao)} voto(s) recebido(s)
            </div>

            <div class="rodape">
                QUERIDÔMETRO DA OUR • AO VIVO
            </div>
            """,
            unsafe_allow_html=True
        )

        # Tempo que cada morador fica na tela
        time.sleep(5)

    # Depois de passar por todos,
    # busca os votos novamente.
