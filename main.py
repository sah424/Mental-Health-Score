import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field # Field = Validation 
# Importing CORS
from fastapi.middleware.cors import CORSMiddleware

# For custom datatype
from typing import Literal

model = joblib.load('Mental_Health_Prediction_Model.pkl')
top_countries = [
    'Other',
 'India',
 'USA',
 'Canada',
 'Australia',
 'UK',
 'Germany',
 'Mexico',
 'Turkey',
 'France'
 ]


app = FastAPI()


# Whenever we want to link FastApi w Html,css,js for that we need to add 'CROSS ORIGIN RESORCE SHARING'
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)
# CORS basicaly used to connect BACKEND & FORNTEND
# f.e Backend is running in port 2200 and Frontend is running on port 5000 now ther sever are different so to connect those 2/ to run both in same port we need CORS



# A first pydentic model
class StudentData(BaseModel):

    # Validation for all column
    # : Validation 
    # ... = Important/*
    # ge = greater than
    # le = less than
    # Literal = Custom data type
    # After running this what we are getting what we will get in /describe is called request body

    age                     : int = Field(..., ge=10, le=100)
    gender                  : Literal['Male', 'Female']
    country                 : str
    academic_level          : Literal['Undergraduate', 'Graduate', 'High School']
    most_used_platform      : Literal['Facebook', 'LinkedIn', 'Instagram', 'Snapchat','Twitter','YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp','WeChat']
    purpose_of_use          : Literal['Networking', 'Education', 'Entertainment', 'News']
    avg_daily_usage_hours   : float = Field(..., ge=0, le=24)
    daily_unlocks           : int   = Field(..., ge=0)
    study_hours             : float = Field(..., ge=0, le=24)
    physical_activity_hours : float = Field(..., ge=0, le=24)
    sleep_hours_per_night   : float = Field(..., ge=0, le=24)
    stress_level            : Literal['Medium', 'Low', 'Very High', 'High']


# Now we gonna create response body
# Describe what we send back
# Valodation for Target column

class PredictionResponse(BaseModel) : #b.6.777777
    predicted_mental_health_score : float
    # is 6.777777 folat ?



# Have to create a /predict endpoint
@app.get('/')
def greet():
    return {'Hello World'}


# It will do what - whenever a user will write '/predict' & after that will give input of the data then when will press 'Enter' prediction will come threw this from class PredictionResponse
# response_model will diplay the prediction by validating from PredictionResponse
@app.post('/predict', response_model= PredictionResponse) #c.6.777777
def predict(data: StudentData):

    # dividing coutries in 2 format by using if/else
    country_group = data.country if data.country in top_countries else "Other"


    # We have multiple columns as input
    # Creating variable
    # We are converting user given data into a dataframe format

    input_row = pd.DataFrame([{
        'Age'                       : data.age,
        'Gender'                    : data.gender,
        'Country'                   : data.country,
        'Academic_Level'            : data.academic_level,
        'Most_Used_Platform'        : data.most_used_platform,
        'Purpose_Of_Use'            : data.purpose_of_use,
        'Avg_Daily_Usage_Hours'     : data.avg_daily_usage_hours,
        'Daily_Unlocks'             : data.daily_unlocks,
        'Study_Hours'               : data.study_hours,
        'Physical_Activity_Hours'   : data.physical_activity_hours,
        'Sleep_Hours_Per_Night'     : data.sleep_hours_per_night,
        'Stress_Level'              : data.stress_level,
        'Grouped_Country'           : country_group
    }])

    # After creating as dataframe format we will share this to our model
    # model will do '.predict' in 'input _row'
    # [0] =. from zeroth index of input data everything needs to get passon
 
    prediction = model.predict(input_row)[0] #a.6.777777


    # now to get the ans 
    # first go to PredictionResponse inside that will go to predicted_mental_health_score here we pass the prediction
    return PredictionResponse(predicted_mental_health_score = round(float(prediction),2))



"""
The code will start from '/predict' @app.post
What ever data came we store that in pd.DataFrame in there correct format

Now to prediction we will go to 'model' inside that we wrote '.predict'(function) in 'prediction' it will perform the all dataframe activity then it will give us
mental_helth_score

Now what ever score will come it will go to 'PredictionResponse' at @/post insde that class -> class PredictionResponse
then inside that class whatever score is comming from that, the class will check/validate that the score type is float or not 
"""
"""
{
  "age": 10,
  "gender": "Male",
  "country": "string",
  "academic_level": "Undergraduate",
  "most_used_platform": "Facebook",
  "purpose_of_use": "Networking",
  "avg_daily_usage_hours": 24,
  "daily_unlocks": 0,
  "study_hours": 24,
  "physical_activity_hours": 24,
  "sleep_hours_per_night": 24,
  "stress_level": "Medium"
}

this data will 1st go to class StudentData - pydantic model
StudentData will check is this values are in correctformat or not ?
if not will throw error 
if yes 

if will create a data frame from pd.DataFrame

After the values come we will share our .pkl our input rows form 'prediction'
now got the 'prediction'

Now will check the format of 'prediction' - is it in float or not ?
To check that will go to 'PredictionResponse' class
here we have validation named 'prediction_mental_helth_score' to check that is it in float format or not if yes
'response_model' will show the prediction

"""