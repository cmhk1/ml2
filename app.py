# VEHICLES AVAILABILITY PREDICTION
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the trained raw model (e.g., XGBRegressor) using pickle
with open('my_vehicule_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Defining the function to preprocess and make predictions
def preprocess_and_predict(dteday, hr, holiday, weathersit, temp, rush, wind, Hum):
    # Preprocessing user inputs
    mnth = dteday.month

    # Season calculation based on the month
    if mnth in [3, 4, 5]:
        season = 1  # Spring
    elif mnth in [6, 7, 8]:
        season = 2  # Summer
    elif mnth in [9, 10, 11]:
        season = 3  # Fall
    else:
        season = 4  # Winter

    # Extract hour from time input
    hr = hr.hour

    # Convert holiday input into numeric
    holiday = 0 if holiday == "No" else 1

    # Calculate weekday from the input date
    weekday = dteday.weekday()

    # Convert weather situation input into numeric
    weathersit_mapping = {
        "Clear/Sunny": 1,
        "Cloudy/Misty": 2,
        "Light Snow/Rain": 3,
        "Heavy Rain/Snow": 4,
    }
    weathersit = weathersit_mapping[weathersit]

    # Normalize numerical inputs
    temp = temp / 41  # Normalize temperature (assuming max temp = 41°C)
    rush = 1 if rush == "Rush" else 0
    wind_mapping = {"Low": "Wind_Low", "Medium": "Wind_Medium", "High": "Wind_High"}
    wind = wind_mapping[wind]
    hum_mapping = {"Low": "Hum_Low", "Medium": "Hum_Medium", "High": "Hum_High"}
    Hum = hum_mapping[Hum]

    # Create a DataFrame for input features
    input_data = {
        'season': season,
        'mnth': mnth,
        'hr': hr,
        'holiday': holiday,
        'weekday': weekday,
        'weathersit': weathersit,
        'temp': temp,
        'Rush': rush,
        wind: 1,  # Set one-hot encoded value for wind
        Hum: 1,   # Set one-hot encoded value for humidity
    }

    # One-hot encode remaining categorical variables
    for col in ['season', 'mnth', 'hr', 'weekday']:
        for value in range(1, 13 if col == 'mnth' else (24 if col == 'hr' else 7)):
            input_data[f"{col}_{value}.0"] = 1 if input_data.get(col) == value else 0

    # Drop original non-encoded columns
    input_data = {key: val for key, val in input_data.items() if '_' in key or isinstance(val, (int, float))}

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Fill missing columns with 0 (to match training data)
    for col in model.feature_names_in_:
        if col not in input_df:
            input_df[col] = 0

    # Reorder columns to match training data
    input_df = input_df[model.feature_names_in_]

    # Make prediction using the raw model
    predicted_value = model.predict(input_df)[0]
    return predicted_value

# Define the main function for the Streamlit app
def main_vehicle_prediction():
    # Front-end elements of the web page
    html_temp = """
    <div style="background-color:green;padding:10px">
    <h2 style="color:white;text-align:center;">Vehicle Availability Checker</h2>
    </div>"""

    st.markdown(html_temp, unsafe_allow_html=True)
    st.subheader("Fill in the fields to predict the number of vehicles required.")

    # Input fields for user data
    dteday = st.date_input("Select a date for vehicle availability", value=pd.Timestamp.now().date())
    hr = st.time_input("Select an hour", value=pd.Timestamp.now().time())
    holiday = st.selectbox("Is it a holiday?", ("No", "Yes"))
    rush = st.selectbox("Is it rush hour?", ("Not Rush", "Rush"))
    wind = st.selectbox("How windy is it?", ("Low", "Medium", "High"))
    weathersit = st.selectbox("How is the weather?", ("Clear/Sunny", "Cloudy/Misty", "Light Snow/Rain", "Heavy Rain/Snow"))
    temp = st.slider("Temperature (°C)", min_value=-30, max_value=50, value=20)
    Hum = st.selectbox("Humidity level", ("Low", "Medium", "High"))

    # Prediction result
    if st.button("Predict"):
        result = preprocess_and_predict(dteday, hr, holiday, weathersit, temp, rush, wind, Hum)
        rounded_result = round(1000 - result)  # Round the result to a whole number
        st.success(f"The optimal number of vehicles to deploy is: {rounded_result}")

if __name__ == '__main__':
    main_vehicle_prediction()
