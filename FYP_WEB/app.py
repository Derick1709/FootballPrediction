import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Football Prediction",
                   page_icon=":soccer:", layout="wide")

# Load saved model
loaded_model = joblib.load('', 'rb')

options = ["Johor Darul Ta'zim", "Kedah Darul Aman", "Kelantan", "Kelantan United", "Kuala Lumpur City", "Kuching City",
           "Negeri Sembilan", "PDRM", "Penang", "Perak", "Sabah", "Selangor", "Sri Pahang", "Terengganu"]

csv_file_path = "./RollingMSL.csv"


def extract_team_data(home_sb, csv_file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        # Filter data for the selected team
        team_data = df[df['Team'] == home_sb]

        if team_data.empty:
            st.warning(
                f"No data found for {home_sb}. Please check your CSV file.")
            return None

        latest_data = team_data.iloc[-1]
        # Extract the required columns
        selected_columns = [
            'Goal Scored_rolling',
            'Goal Conceded_rolling',
            'ShotF_rolling',
            'ShotOnF_rolling',
            'CornerF_rolling',
            'CornerA_rolling',
            'OffF_rolling',
            'OffA_rolling',
            'FoulF_rolling',
            'FoulA_rolling'
        ]
        user_input_data = latest_data[selected_columns]
        # Create a DataFrame in the specified format
        user_input = pd.DataFrame({
            'Team_code': [home_team_code],
            'Venue_Code': [venue_code],
            'opp_code': [away_team_code],
            'hour': [hour_options[hour]],
            'day_code': [day_options[day_code]],
            'Goal Scored_rolling': [user_input_data['Goal Scored_rolling']],
            'Goal Conceded_rolling': [user_input_data['Goal Conceded_rolling']],
            'ShotF_rolling': [user_input_data['ShotF_rolling']],
            'ShotOnF_rolling': [user_input_data['ShotOnF_rolling']],
            'CornerF_rolling': [user_input_data['CornerF_rolling']],
            'CornerA_rolling': [user_input_data['CornerA_rolling']],
            'OffF_rolling': [user_input_data['OffF_rolling']],
            'OffA_rolling': [user_input_data['OffA_rolling']],
            'FoulF_rolling': [user_input_data['FoulF_rolling']],
            'FoulA_rolling': [user_input_data['FoulA_rolling']]
        })

        return user_input

    except Exception as e:
        st.error(f"An error occurred while extracting team data: {e}")
        return None


with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Home", "Predictor", "Help"],
        default_index=0,
    )

if selected == "Home":
    st.title("Malaysia Super League Prediction System :soccer:")
    banner_path = "MFL.JPG"
    st.image("MFL.JPG", use_column_width=True, output_format='auto')
    st.write("Football, the world's most popular sport, captivates billions of fans globally. Predicting match outcomes based on historical data is a challenge even for experts. Machine learning offers a solution, enabling more accurate predictions using team statistics, player metrics, and historical trends.")
    st.header("Upcoming Fixtures")
    fixtures_link = "[Click here to view upcoming fixtures](https://www.aiscore.com/tournament-malaysian-super-league/w34kgmi2y1h1ko9)"
    st.markdown(fixtures_link, unsafe_allow_html=True)


if selected == "Predictor":

    # Header
    with st.container():
        st.title("Choose Your Team to Predict")

    # Dropdown
    with st.container():
        home_sb = st.selectbox('Select Team', options)

        away_sb = st.selectbox('Select Opponent Team', options)

    # Check if the same team is selected for both home and away
    if home_sb == away_sb:
        st.warning("Please select different Team and Opponent.")
        st.stop()

    # Team code mapping
    team_mapping = {
        '': None,
        'Johor Darul Ta\'zim': 0,
        'Kedah Darul Aman': 1,
        'Kelantan': 2,
        'Kelantan United': 3,
        'Kuala Lumpur City': 4,
        'Kuching City': 5,
        'Negeri Sembilan': 6,
        'PDRM': 7,
        'Penang': 8,
        'Perak': 9,
        'Sabah': 10,
        'Selangor': 11,
        'Sri Pahang': 12,
        'Terengganu': 13
    }

    # Map selected team names to numeric codes
    home_team_code = team_mapping.get(home_sb, 0)
    away_team_code = team_mapping.get(away_sb, 0)

    # Dropdown for Venue
    venue_options = {'': None, 'Home': 1, 'Away': 0}
    venue_code = st.selectbox(
        'Select Venue (Home or Away)', list(venue_options.keys()))

    # Check if any of the required options is not selected
    if venue_code == '':
        st.warning("Please select Venue")
        st.stop()

    # Set venue code based on the selected venue
    venue_code = venue_options.get(venue_code, 0)

    # Image container
    col1, col2 = st.columns(2)

    with col1:
        st.header("Team")
        st.image("./Club Logo/" + home_sb + ".png", width=250)

    with col2:
        st.header("Opponent")
        st.image("./Club Logo/" + away_sb + ".png", width=250)

    # Dropdown for hour options
    hour_options = {'': None, '5pm': 17, '6pm': 18, '7pm': 19, '8pm': 20,
                    '9pm': 21, '10pm': 22, '11pm': 23, '12am': 0}
    hour = st.selectbox("Select Time", list(hour_options.keys()))

    # Check if any of the required options is not selected
    if hour == '':
        st.warning("Please select Time")
        st.stop()

    # Dropdown for day options
    day_options = {'': None, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
                   'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
    day_code = st.selectbox("Select Day of Week", list(day_options.keys()))

    # Check if any of the required options is not selected
    if day_code == '':
        st.warning("Please select Day")
        st.stop()

    # Predict function to call function and make prediction
    if st.button("Predict"):

        # Extract team data using the custom function
        user_input_data = extract_team_data(home_sb, csv_file_path)

        if user_input_data is not None:

            # Add the extracted data to the user input DataFrame
            user_input = pd.concat([user_input_data], axis=1)

            # Make predictions using the loaded model
            prediction = loaded_model.predict(user_input)

            # Display the prediction outcome
            outcome = "Win" if prediction[0] == 1 else "Lose"

            if outcome == "Win":
                st.success("Predicted Outcome: Win")
                st.image("./Club Logo/" + home_sb + ".png", width=250)
            else:
                st.error("Predicted Outcome: Lose")
                st.image("./Club Logo/" + away_sb + ".png", width=250)

if selected == "Help":
    st.title(f"You have selected {selected}")
