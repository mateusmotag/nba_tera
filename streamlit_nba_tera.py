import streamlit as st
import joblib
import numpy as np
import warnings

# Define o título com a cor branca usando CSS
# Defina a largura da página usando CSS
# Configurar a largura da página para 1500 pixels
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title="Probabilidade de sucesso do atleta da NCAA na NBA",
)
st.markdown(
    """
    <h1 style='text-align: center; color: white;margin-top: -4%'>Probabilidade de Sucesso de jogador da NCAA na NBA</h1>
    """,
    unsafe_allow_html=True
)

if 'avaliado' not in st.session_state:
    st.session_state['avaliado'] = False



# Define o layout em duas colunas
col1, col2,col3 = st.columns([5, 5,5])

# Adicione campos de input para os atributos do jogador na coluna 1 (à esquerda)
with col1:
    
    # Substitua o slider por um campo de entrada numérica
    gp = st.number_input("Partidas jogadas", min_value=1., key="gp")

    # Defina os estilos para o campo de entrada numérica na coluna 1
    input_styles_col1 = f'''
    <style>
        /* Adicione estilos específicos para o campo de entrada numérica aqui */
        /* Por exemplo, você pode definir a cor de fundo, a cor do texto, o tamanho da fonte, etc. */
        .stNumberInput {{
            /* Seus estilos para o campo de entrada numérica aqui */
        }}

        /* Estilize o rótulo do campo de entrada numérica */
        .stNumberInput label {{
            color: white;  /* Cor do rótulo do campo de entrada numérica */
            font-size: 20px;
            line-height: 0;
        }}

        .stNumberInput .step-up,
        .stNumberInput .step-down {{
            display: none;
        }}

        /* Adicionar borda de contorno na caixa de texto do input */
        .stNumberInput input {{
            border: 2px solid white;
            border-radius: 5px;
            padding: 5px;
            color: white;  /* Cor do texto */
            background-color: #78909C;  /* Cor de fundo da caixa de texto */
        }}
    </style>
    '''

    # Inclua os estilos do campo de entrada numérica na coluna 1
    st.markdown(input_styles_col1, unsafe_allow_html=True)

    # Continuação dos sliders e outros elementos na coluna 1
    minutes = st.number_input("Média de Minutos por jogo", 1., key="minutes")
    ptspergame = st.number_input("Média de pontos por Jogo:", 0., key="ptspergame")
    astpergame = st.number_input("Média de assitências por Jogo:", 0., key="astpergame")
    stl_totals = st.number_input("Total de roubos de bola:", 0., key="stl_totals")
    drb_totals = st.number_input("Total de rebotes defensivos:", 0., key="drb_totals")
    orb_totals = st.number_input("Total de rebotes ofensivos:", 0., key="orb_totals")
    
    
    
with col3:
    
    # Substitua o slider por um campo de entrada numérica
    blkpergame = st.number_input("Média de Tocos por Jogo:", 0., key="blkpergame")
    

    # Defina os estilos para o campo de entrada numérica na coluna 1
    input_styles_col1 = f'''
    <style>
        /* Adicione estilos específicos para o campo de entrada numérica aqui */
        /* Por exemplo, você pode definir a cor de fundo, a cor do texto, o tamanho da fonte, etc. */
        .stNumberInput {{
            /* Seus estilos para o campo de entrada numérica aqui */
        }}

        /* Estilize o rótulo do campo de entrada numérica */
        .stNumberInput label {{
            color: white;  /* Cor do rótulo do campo de entrada numérica */
            font-size: 20px;
            line-height: 0;
        }}

        .stNumberInput .step-up,
        .stNumberInput .step-down {{
            display: none;
        }}

        /* Adicionar borda de contorno na caixa de texto do input */
        .stNumberInput input {{
            border: 2px solid white;
            border-radius: 5px;
            padding: 5px;
            color: white;  /* Cor do texto */
            background-color: #78909C;  /* Cor de fundo da caixa de texto */
        }}
    </style>
    '''

    # Inclua os estilos do campo de entrada numérica na coluna 1
    st.markdown(input_styles_col1, unsafe_allow_html=True)

    # Continuação dos sliders e outros elementos na coluna 1
    usg = st.number_input("Usage Rate (%)", 0., key="usg")
    fg = st.number_input("Percentual de arremessos certos (%)", 0., key="fg")
    pm2 = st.number_input("Arremessos de 2 pontos certos", 0., key="2pm")
    pm3 = st.number_input("Arremessos de 3 pontos certos", 0., key="3pm")
    tovpergame = st.number_input("Média de perdas de bola por jogo", 0., key="tovpergame")
    drtg = st.number_input("Rating defensivo", 0., key="drtg")
    ortg = st.number_input("Rating ofensivo", 0., key="ortg")


# Dicionário de jogadores e suas imagens correspondentes
players = {
    "Jogador 1": "player1.png",
    "Jogador 2": "player2.png",
    "Jogador 3": "player3.png"
}

with col2:
    # Usando HTML para definir a cor do texto
    st.markdown("<h2 style='color: white;font-size: 24px;'>Escolha uma aparência:</h2>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
            st.session_state['avaliado'] = False
            st.experimental_rerun()
    selected_player = st.selectbox("", list(players.keys()))
    # Aplicar estilos CSS personalizados para a caixa de seleção na coluna 2
    custom_css_col2 = f"""
        <style>
            .st-c0 {{
                background-color: #78909C !important;  /* Cor de fundo (importante para sobrescrever estilos padrão) */
                color: white !important;  /* Cor do texto */
                font-size: 18px;  /* Tamanho da fonte */
            }}

            .st-c0:hover,
            .st-c0:focus {{
                background-color: rgb(255, 75, 75) !important;  /* Cor quando o mouse passa sobre a opção (vermelho) */
            }}
        </style>
    """

    st.markdown(custom_css_col2, unsafe_allow_html=True)

    if selected_player:
        player_image = players[selected_player]
        st.image(player_image, use_column_width=True)

# Avaliação
if col1.button("Avaliar"):
    st.session_state['avaliado'] = True
    modelo_adaboost = joblib.load("adaboost_otimizado.joblib")
    
    # Criar um dicionário com os valores inseridos pelo usuário
    jogador_data = {
        "gp": gp,
        "ptspergame": ptspergame,
        "stl_totals": stl_totals,
        "drb_totals": drb_totals,
        "blkpergame": blkpergame,
        "drtg": drtg,
        "ortg": ortg,
        "usg": usg/100,
        "fg": fg/100,
        "2pm": pm2,
        "3pm": pm3,
        "tovpergame": tovpergame,
        "astpermin": (astpergame)/(minutes),
        "tovpermin": (tovpergame)/(minutes),
        "blkpermin": (blkpergame)/(minutes),
        "stlpermin": (stl_totals)/(minutes*gp),
        "ptspermin": (ptspergame)/(minutes),
        "orbpermin": (orb_totals)/(minutes*gp)
    }

    # Converter o dicionário em um array numpy
    jogador_array = np.array(list(jogador_data.values())).reshape(1, -1)

    # Fazer a previsão usando o modelo
    previsao = modelo_adaboost.predict(jogador_array)
    probabilidade = modelo_adaboost.predict_proba(jogador_array)[:, 1]  # Extrai a probabilidade da classe positiva

    # Formatar a probabilidade para remover os colchetes e limitar o número de casas decimais
    probabilidade_formatada = f"{probabilidade[0]*100:.0f}"

    # Exibir a avaliação como um modal
    st.markdown(
        """
        <style>
            .custom-modal {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                padding: 20px;
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                z-index: 9999;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    if previsao[0] == 0:
        st.markdown(
            f"""
            <div class="custom-modal">
                <h2 style="color: red;">Probabilidade de sucesso na NBA: {probabilidade_formatada}%</h2>
                </script>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="custom-modal">
                <h2 style="color: green;">Probabilidade de sucesso na NBA: {probabilidade_formatada}%</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    


# Aplicar CSS personalizado para o fundo
st.markdown(
    """
    <style>
    .stApp {
        background-color: #78909C; 
    }
    </style>
    """,
    unsafe_allow_html=True
)
