#Machine-Learning 2: University Project

## Project: Vehicules Availability Prediction

### Project Overview

This project aims to predict the optimal availability and deployment of vehicules based on various factors, including time of day, season, weather conditions, and more. The primary goal is to create an efficient model that forecasts vehicule demand, allowing for strategic deployment of vehicules to meet demand peaks and minimize idle time. Using data preprocessing, feature engineering, and predictive modeling, this project provides actionable insights to enhance vehicule availability and utilization.

### Dataset Description

The dataset used in this project includes key features relevant to vehicule usage patterns. Some of the essential columns in the dataset include:

- **hr**: The hour of the day (0-23) representing vehicule usage at specific times.
- **season**: The season during which the vehicule usage is recorded (spring, summer, fall, winter).
- **weathersit**: Weather conditions (e.g., Clear/Sunny, Cloudy/Misty, Light Snow/Rain, Heavy Rain/Snow).
- **temp**: Temperature in Celsius.
- **hum**: Humidity levels.
- **windspeed**: Wind speed level.
- **cnt**: Count of vehicules used, which is the target variable for prediction.

### Feature Engineering

To improve the accuracy and interpretability of the model, we performed several feature engineering steps:

1. **Rush Hour Classification**: 
   Based on an analysis of hourly vehicule usage patterns, we identified specific time periods with elevated vehicule demand:
   
   - **Morning Rush**: 7-9 AM
   - **Evening Rush**: 5-7 PM
   
   These hours were classified as "Rush," while all other hours were labeled "Not Rush." This classification enables the model to capture peak vehicule demand periods and make targeted predictions. The bar chart below illustrates the rush and non-rush hour demand, with rush hours highlighted in red:
   
<img width="856" alt="Screenshot 2024-11-15 at 20 56 39" src="https://github.com/user-attachments/assets/3e718477-233e-4ba0-92cf-3107cfed2ddf">

   
3. **Wind Speed Classification**:
   Wind speed values were categorized as:
   
   - **Low**: Below 0.1
   - **Medium**: Between 0.1 and 0.2
   - **High**: 0.2 and above
   
   This binning helps to represent wind conditions concisely for the model.

4. **Humidity Classification**:
   Humidity levels were classified as:
   
   - **Low**: Below 0.3
   - **Medium**: Between 0.31 and 0.6
   - **High**: 0.6 and above
   
   Similar to wind speed, this classification simplifies the humidity data for improved model performance.

### Model Development

The model was developed using PyCaret, a low-code machine learning library that simplifies model building and tuning. The following steps were taken to build the predictive model:

1. **Data Preprocessing**:
   - Dropped unnecessary columns such as simple counts and identifiers that do not contribute predictive value (e.g., `instant`).
   - Used binning and encoding on categorical and numerical features to improve model input quality.

2. **Model Setup and Training**:
   - Defined categorical and numeric features for the model.
   - Applied feature engineering techniques, such as removing multicollinearity and feature scaling, for optimal model performance.
   - Configured a time-series split to respect temporal order in data, essential for accurate predictions.

3. **Evaluation Metrics**:
   The model was evaluated on several metrics, including:
   
   - **MAE (Mean Absolute Error)**: Measures average absolute errors.
   - **MSE (Mean Squared Error)**: Squares errors to penalize larger errors.
   - **RMSE (Root Mean Squared Error)**: Square root of MSE, for easier interpretation.
   - **R² (Coefficient of Determination)**: Indicates proportion of variance explained.
   - **MAPE (Mean Absolute Percentage Error)**: Measures percentage-based error.

### Model Deployment

The model is designed to be deployed in a Streamlit app, where users can input various conditions such as date, time, weather, and temperature to predict vehicule availability. The app displays the optimal number of vehicules to deploy for the selected date and time, helping decision-makers manage resources efficiently.

### How to Use

1. **Launch the Streamlit app**.

streamlit run app.py

3. **Enter the required inputs** for prediction:
   - Date and time for which vehicule availability is desired.
   - Select the weather conditions and temperature.
4. **Run the prediction** to see the recommended vehicule deployment.

### Conclusion

This project provides a  model for predicting vehicule demand based on time and environmental factors. By classifying rush hours and binning other features, the model’s ability to make accurate predictions for effective vehicule deployment has been improved. The tool aids in managing vehicule resources efficiently, helping to meet demand surges and optimize utilization.

