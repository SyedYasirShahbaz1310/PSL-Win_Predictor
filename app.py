import streamlit as st


import pickle
import pandas as pd

batting_team = ['Quetta Gladiators', 'Karachi Kings', 'Islamabad United',
       'Peshawar Zalmi', 'Lahore Qalandars', 'Multan Sultans']

city = ['Dubai International Cricket Stadium', 'Sharjah Cricket Stadium',
       'Gaddafi Stadium', 'National Stadium', 'Sheikh Zayed Stadium',
       'Multan Cricket Stadium', 'Rawalpindi Cricket Stadium', 'Karachi',
       'Abu Dhabi', 'Lahore']

pipe = pickle.load(open('pipe.pkl','rb'))
st.title('PSL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    selected_batting_team = st.selectbox('Select the batting team',sorted(batting_team))
with col2:
    selected_bowling_team = st.selectbox('Select the bowling team',sorted(batting_team))

selected_city = st.selectbox('Select host city',sorted(city))

target = st.number_input('Target')

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets = st.number_input('Wickets out')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'batting_team':[selected_batting_team],'bowling_team':[selected_bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x_y':[target],'crr':[crr],'rrr':[rrr]})

    result = pipe.predict_proba(input_df)
    win = result[0][0]
    loss = result[0][1]
    st.header(selected_batting_team + "- " + str(round(win*100)) + "%")
    st.header(selected_bowling_team + "- " + str(round(loss*100)) + "%")


