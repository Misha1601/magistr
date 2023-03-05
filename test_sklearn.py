from sklearn.linear_model import LinearRegression

def predict_production_volumes(annual_volumes):
    # Create a list of years from 1 to 20
    years = [[i] for i in range(1995, 2021)]
    print(years)

    # Create a linear regression model
    model = LinearRegression().fit(years, annual_volumes)

    # Use the model to predict production volumes for the next 5 years
    predicted_volumes = model.predict([[2021], [2022], [2023], [2024], [2025]])

    return predicted_volumes.tolist()

production_volumes = [100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195]
generate = [8.26192344363636, 9.20460066059596, 12.0178164697778, 15.921260267805, 21.2161740066094, 31.420434564131, 38.3904519471421, 52.3307819867071, 62.9113953016839, 85.1161924282732, 104.083879757882, 132.859216030029, 170.682620580279, 220.600045153997, 276.020526299077, 346.465021938078, 440.385091980306, 530.55442135112, 635.49205101167, 705.805860788812, 831.42968828187, 962.227395409379, 1140.31094904253, 1269.52053571083, 1418.17004626655, 1591.2135122193]
predicted_volumes = predict_production_volumes(generate)
print(predicted_volumes)
