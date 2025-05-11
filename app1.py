import streamlit as st
import pickle
import pandas as pd

# Load the model
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Teams and cities
batting_team = ['Quetta Gladiators', 'Karachi Kings', 'Islamabad United',
                'Peshawar Zalmi', 'Lahore Qalandars', 'Multan Sultans']
city = ['Dubai International Cricket Stadium', 'Sharjah Cricket Stadium',
        'Gaddafi Stadium', 'National Stadium', 'Sheikh Zayed Stadium',
        'Multan Cricket Stadium', 'Rawalpindi Cricket Stadium', 'Karachi',
        'Abu Dhabi', 'Lahore']

# Set page config
st.set_page_config(
    page_title="PSL Win Predictor",
    page_icon="🏏",
    layout="wide"
)

# Custom CSS with enhanced styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                                            url('data:image/jpeg;base64,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');

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .title {
        color: white !important;
        text-align: center;
        font-size: 2.8rem !important;
        font-weight: bold;
        margin-bottom: 30px;
        text-shadow: 2px 2px 8px #000000;
    }

    .select-label {
        font-size: 1.4rem !important;
        color: white !important;
        font-weight: bold !important;
        margin-bottom: 10px !important;
    }

    .stSelectbox>div>div {
        font-size: 1.3rem !important;
        padding: 15px !important;
        height: auto !important;
        min-height: 60px !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #1E3D8F !important;
        border-radius: 10px !important;
    }

    .stNumberInput input {
        font-size: 1.2rem !important;
        padding: 12px !important;
    }

    .stButton>button {
        background-color: #1E3D8F !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 24px;
        margin: 20px 0;
        width: 100%;
        border: none;
        font-size: 1.2rem;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: #142B66 !important;
        transform: scale(1.02);
    }

   # Change the result-box CSS in your style section to this:
.result-box {
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 12px;
    padding: 25px;
    margin-top: 30px;
    color: white;
    /* Removed the border property */
}

    .team-name {
        color: #FFD700;
        text-align: center;
        font-size: 1.8rem;
        margin-bottom: 10px;
    }

    .percentage {
        color: white;
        text-align: center;
        font-size: 2.5rem;
        margin: 15px 0;
    }

    .footer {
        text-align: center;
        color: white;
        margin-top: 50px;
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .stProgress>div>div>div {
        background-color: #FFD700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="title">🏏 PSL WIN PREDICTOR</h1>', unsafe_allow_html=True)

# Main container
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="select-label">Select the batting team</div>', unsafe_allow_html=True)
        selected_batting_team = st.selectbox(
            "batting_team_select",
            sorted(batting_team),
            label_visibility="collapsed"
        )

    with col2:
        st.markdown('<div class="select-label">Select the bowling team</div>', unsafe_allow_html=True)
        selected_bowling_team = st.selectbox(
            "bowling_team_select",
            sorted(batting_team),
            label_visibility="collapsed"
        )

    st.markdown('<div class="select-label">Select host city</div>', unsafe_allow_html=True)
    selected_city = st.selectbox(
        "city_select",
        sorted(city),
        label_visibility="collapsed"
    )

    st.markdown('<div class="select-label">Target</div>', unsafe_allow_html=True)
    target = st.number_input(
        "target_input",
        min_value=0,
        step=1,
        label_visibility="collapsed"
    )

    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown('<div class="select-label">Score</div>', unsafe_allow_html=True)
        score = st.number_input(
            "score_input",
            min_value=0,
            step=1,
            label_visibility="collapsed"
        )
    with col4:
        st.markdown('<div class="select-label">Overs completed</div>', unsafe_allow_html=True)
        overs = st.number_input(
            "overs_input",
            min_value=0,
            max_value=20,
            step=1,
            label_visibility="collapsed"
        )
    with col5:
        st.markdown('<div class="select-label">Wickets out</div>', unsafe_allow_html=True)
        wickets = st.number_input(
            "wickets_input",
            min_value=0,
            max_value=9,
            step=1,
            label_visibility="collapsed"
        )

    if st.button('Predict Winning Probability', key="predict_button"):
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        input_df = pd.DataFrame({
            'batting_team': [selected_batting_team],
            'bowling_team': [selected_bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_left],
            'total_runs_x_y': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        result = pipe.predict_proba(input_df)
        win = result[0][0]
        loss = result[0][1]

        with st.container():
            st.markdown('<div class="result-box">', unsafe_allow_html=True)

            st.markdown(f'<div class="team-name">{selected_batting_team}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="percentage">{round(win * 100)}%</div>', unsafe_allow_html=True)
            st.progress(win)

            st.markdown(f'<div class="team-name" style="margin-top: 30px;">{selected_bowling_team}</div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div class="percentage">{round(loss * 100)}%</div>', unsafe_allow_html=True)
            st.progress(loss)

            st.markdown('</div>', unsafe_allow_html=True)

# Add footer
st.markdown("""
    <div class="footer">
        Pakistan Super League Win Predictor © 2023
    </div>
""", unsafe_allow_html=True)