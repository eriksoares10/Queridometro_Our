import streamlit as st
import time
from collections import Counter
from supabase import create_client

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Queridômetro da OUR",
    page_icon="🏠",
    layout="wide"
)

# ============================================================
# SUPABASE
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
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #101412;
}

.block-container {
    max-width: 1400px;
    padding-top: 25px;
}

/* TÍTULO */

.titulo {
    text-align: center;
    color: #F47B20;
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 3px;
    margin-bottom: 5px;
}

.subtitulo {
    text-align: center;
    color: #A8C99A;
    font-size: 18px;
    margin-bottom: 35px;
}

/* NOME */

.nome {
    text-align: center;
    color: white;
    font-size: 60px;
    font-weight: 900;
    letter-spacing: 3px;
    margin-top: 15px;
    margin-bottom: 35px;
}

/* PAINEL */

.painel {
    background: #1D241F;
    border: 2px solid #F47B20;
    border-radius: 30px;
    padding: 45px;
    margin: auto;
    max-width: 1100px;
    box-shadow: 0px 0px 30px rgba(244,123,32,0.12);
}

/* EMOJIS */

.linha-emojis {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 55px;
    flex-wrap: wrap;
}

.emoji-item {
    text-align: center;
    min-width: 90px;
}

.emoji {
    font-size: 65px;
    line-height: 1;
}

.quantidade {
    color: white;
    font-size: 28px;
    font-weight: 900;
    margin-top: 12px;
}

.rotulo {
    color: #A8C99A;
    font-size: 13px;
    margin-top: 4px;
}

/* SEM VOTOS */

.sem-votos {
    text-align: center;
    color: #777;
    font-size: 25px;
    padding: 50px;
}

/* RODAPÉ */

.rodape {
    text-align: center;
    color: #666;
    font-size: 14px;
    margin-top: 30px;
    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# TÍTULO
# ============================================================

st.markdown(
    '<div class="titulo">🏠 QUERIDÔMETRO DA OUR</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">💌 AO VIVO</div>',
    unsafe_allow_html=True
)

# ============================================================
# ÁREA QUE SERÁ ATUALIZADA
# ============================================================

tela = st.empty()

# ============================================================
# BUSCAR VOTOS
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
# LOOP DA TV
# ============================================================

while True:

    resultados = buscar_votos()

    for pessoa in MORADORES:

        votos_pessoa = [
            voto
            for voto in resultados
            if voto["avaliado"] == pessoa
        ]

        contagem = Counter(
            voto["emoji"]
            for voto in votos_pessoa
        )

        # ----------------------------------------------------
        # MONTA OS EMOJIS AGRUPADOS
        # ----------------------------------------------------

        emojis_html = ""

        for emoji, quantidade in contagem.items():

            emojis_html += f"""
            <div class="emoji-item">
                <div class="emoji">{emoji}</div>
                <div class="quantidade">{quantidade}</div>
            </div>
            """

        # ----------------------------------------------------
        # CASO NÃO TENHA VOTOS
        # ----------------------------------------------------

        if not emojis_html:

            emojis_html = """
            <div class="sem-votos">
                Nenhum voto ainda...
            </div>
            """

        # ----------------------------------------------------
        # MOSTRA O PARTICIPANTE
        # ----------------------------------------------------

        tela.markdown(
            f"""
            <div class="painel">
                <div class="nome">{pessoa}</div>
                <div class="linha-emojis">
                    {emojis_html}
                </div>
                <div class="rodape">
                    QUERIDÔMETRO DA OUR
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Tempo de exibição de cada participante
        time.sleep(5)
