from prophet import Prophet
import pandas as pd
import numpy as np
import warnings
from IPython.display import display

warnings.filterwarnings("ignore")
df = pd.read_csv('train.csv', low_memory=False)
df_prophet = df[['date', 'target']].groupby(by='date', as_index=False).mean().rename(columns={'date':'ds', 'target':'y'})
m = Prophet(stan_backend='CMDSTANPY')
m.fit(df_prophet)
future = m.make_future_dataframe(periods=30)
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig1 = m.plot(forecast)
forecast[['ds', 'yhat']].rename(columns={'ds': 'date', 'yhat': 'prophet_prediction'}).to_csv('prophet_prediction.csv', index=False)