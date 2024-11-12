import pandas as pd
import plotly.express as px

df = pd.read_csv('1/1.csv')

K = 0.5 * df['T'] + df['P_ext'] - 1.5 * df['P_con'] 

fig = px.line(df, x = 'timestep', y = K , title='energy per timestep')
fig.show()


