# VEHICULES AVAILABILITY PREDICTION
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import pycaret
from pycaret.classification import *

# Loading the trained model
model = load_model(model_name='my_vehicule_model')

# Defining the function which will make the prediction using the data which the user inputs TRANSFORMATIONS & RUNNING MODEL
def prediction(dteday, season, yr, mnth, hr, holiday, weekday, workingday, weathersit, temp, atemp, hum, windspeed, tod, rush, wind, Hum, prev_count):

    if dteday.month == 1:
        mnth = 1
    elif dteday.month == 2:
        mnth = 2
    elif dteday.month == 3:
        mnth = 3
    elif dteday.month == 4:
        mnth = 4
    elif dteday.month == 5:
        mnth = 5
    elif dteday.month == 6:
        mnth = 6
    elif dteday.month == 7:
        mnth = 7
    elif dteday.month == 8:
        mnth = 8
    elif dteday.month == 9:
        mnth = 9
    elif dteday.month == 10:
        mnth = 10
    elif dteday.month == 11:
        mnth = 11
    else:
        mnth = 12

    if dteday.month in [3,4,5]:
        season = 1
    elif dteday.month in [6,7,8]:
        season = 2
    elif dteday.month in [9,10,11]:
        season = 3
    else:
        season = 4

    hr = hr.hour

    if holiday == "No":
        holiday = 0
    else:
        holiday = 1

    weekday = dteday.weekday

    if (dteday.weekday in [1,2,3,4,5]) and (holiday == 0):
        workingday = 1
    else:
        workingday = 0

    if weathersit == "Clear/Sunny":
        weathersit = 1
    elif weathersit == "Cloudy/Misty":
        weathersit = 2
    elif weathersit == "Light Snow/Rain":
        weathersit = 3
    else:
        weathersit = 4
    
    tod = hr
    if 6 <= tod < 12:
        tod = "Morning"
    elif 12 <= tod < 17:
        tod = "Afternoon"
    elif 17 <= tod < 21:
        tod = "Evening"
    else:
        tod = "Night"

    temp = temp / 41
    atemp = atemp / 50
    hum = hum / 100
    windspeed = windspeed / 100

    data = {
        'season': season,
        'yr': yr,  
        'mnth': mnth,  
        'hr': hr,  
        'holiday' : holiday,
        'weekday': weekday,
        'workingday' : workingday,
        'weathersit': weathersit,
        'temp': temp,
        'atemp' : atemp,
        'hum': hum,
        'windspeed': windspeed, 
        'TOD': tod,
        'Rush': rush,
        'Wind': wind,
        'Hum' : Hum,
        'prev_count': prev_count
    }

    # Convert data into dataframe
    df = pd.DataFrame.from_dict([data])

    predicted_value = predict_model(model, df)
    predicted_value = pd.DataFrame(predicted_value)
    prediction2 = predicted_value["prediction_label"][0]

    return prediction2
    

##############################

# This is the main function in which we define our webpage FRONT END 
def main_vehicle_prediction():       
    # Front-end elements of the web page 
    html_temp = """
    <div style="background-color:green;padding:10px">
    <h2 style="color:white;text-align:center;">Vehicule availability checker</h2>
    </div>"""

    st.markdown(html_temp, unsafe_allow_html=True)

    # Subtitle of our webapp
    st.subheader("Fill the following questions to see how many vehicules are needed at a specific point in time.")

    ################################
          
    # Following lines create input fields for prediction 
    dteday = st.date_input("What date would you like the vehicules?", format="YYYY-MM-DD", value="today")

    hr = st.time_input("What hour would you like the vehicules?", value="now", step=3600)

    holiday = st.selectbox("Is it a holiday?", ("Yes", "No"))

    rush = st.selectbox("Is it rush hour?", ("Rush", "Not Rush"))

    winds = ("Low", "Medium", "High")
    wind = st.selectbox("How windy is it?", winds)

    weathers = ("Clear/Sunny", "Cloudy/Misty", "Light Snow/Rain", "Heavy Rain/Snow")
    weathersit = st.selectbox("How is the weather?", weathers)

    temp = st.slider("What is the temperature in Celsius?", -30, 50, 1)
    
    Hums = ("Low", "Medium", "High")
    Hum = st.selectbox("How's the humidity?", Hums)

    # Variables that are ignored in PyCaret so we don't care about the value; only included to have the full DF
    yr = 0
    windspeed = 0
    atemp = 0
    hum = 0
    prev_count = 0

    # Variables that will be calculated afterwards
    weekday = 0
    workingday = 0
    season = 0
    tod = 0
    mnth = 0

    result = ""
    # When 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(dteday, season, yr, mnth, hr, holiday, weekday, workingday, weathersit, temp, atemp, hum, windspeed, tod, rush, wind, Hum, prev_count)

        st.success(f"The optimal amount of vehicules to deploy for the selected date and time is {1000 - result}")

      
if __name__ == '__main__':
    main_vehicle_prediction()
