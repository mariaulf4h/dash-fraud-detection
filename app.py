# Import some libraries

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from time import time
import plotly.express as px
import plotly.offline as pyo
import calendar

import warnings
warnings.filterwarnings('ignore')


# Import data_eda.csv
df = pd.read_csv("data/data_eda.csv", index_col = 0)

# Naming Days
df['days'] = df['weekday'].apply(lambda x: calendar.day_name[x]) 

# groupby fraudulence 
fr_group = df.groupby("FraudResult").agg({"CustomerId": "count", "Value": "sum" })
label = {"non-fraud": "non", "fraud": "fraud"}
fr_group["labels"] = label

# Plot "Volume of Fraudulence

# "by Percentage of Transactions"
colors = ['#4F6272', '#B7C3F3', '#DD7596', '#8EB897']

fig_transaction = px.pie(fr_group, values = "CustomerId", names = "labels", color_discrete_sequence=colors)

# "by values"
fig_values = px.pie(fr_group, values = "Value", names = "labels", color_discrete_sequence=colors)


#Selecting only Fraud
fraud = df[df["FraudResult"] == 1]

# Plot Fraud Product Category
fig_fraud_product = px.bar(fraud, x='ProductCategory', y='FraudResult',
             hover_data=['ProductId', 'ChannelId'], color='Value',
             height=400, labels = {'FraudResult' : "Count of fraud. Transactions", 
                                   'ProductCategory': "Product Category"}, )
#fig_fraud_product.update_layout(title_text="Numbers of Fraudulent Transactions by Product Categories")

# Plot Fraud by Days 
fig_fraud_days = px.bar(fraud.sort_values("weekday"), x='days', y='FraudResult',
             hover_data=['ProductId', 'ChannelId'], color='Value',
             height=400), labels = {'FraudResult' : "Count of fraud. Transactions",
                                   'days': "Weekday"})
#fig_fraud_days.update_layout(title_text="Numbers of Fraudulent Transactions by Days")

# Plot Fraud by Hour
fig_fraud_hour = px.bar(fraud.sort_values("hour"), x="hour", y='FraudResult',
             hover_data=['ProductId', 'ChannelId'], color='Value',
             height=400), labels = {'FraudResult' : "Count of fraud. Transactions",
                                   'hour': "Hour"})
#fig_fraud_hour.update_layout(title_text="Numbers of Fraudulent Transactions by Hour")

#import df_plot
df_plot = pd.read_csv("data/df_plot.csv", index_col = 0)

# Customer History
fig_customer_history = px.scatter(df_plot, x = "Value", y = "fraud_total",
                       animation_group= "CustomerId",
                       labels = {"fraud_total" : "Count of Fraudulence Transaction", "fraud_history": "Fraud History"},
                       size = "Value", color = "fraud_history", hover_data= ["ProductCategory", "ChannelId"])

fig_customer_history.update_layout(title_text="Values of Transactions by Customer History", transition = {'duration': 100})


# Import necessary libraries fo Dash

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import base64



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
notes=''

server = app.server


def getPlot(plotObject, title, notes="", static=False):
    if static == True:
        image_filename = f"assets/{plotObject}"
        encoded_image = base64.b64encode(open(image_filename, "rb").read())
        card = dbc.CardBody([
            dbc.Col([
                html.Img(src="data:image/png;base64,{}".format(encoded_image.decode()),
                className='img-thumbnail img-fluid p-1',
                style=dict(width='600px')
                ),
            ], width='100%'),
        ])
    else:
        card = dbc.CardBody([
            dcc.Graph(
                figure = plotObject.update_layout(
                    template='plotly',
                    plot_bgcolor= 'white',
                    paper_bgcolor= 'white',
                ),config={
                    'displayModeBar': True
                }
            )
        ])
    return html.Div([
        dbc.Card([
            dbc.CardHeader([
                html.H5(title)
            ]),
            card,
            dbc.CardFooter([
                html.P(notes)
            ])
        ])
    ])


encoded_image = base64.b64encode(open("assets/fraud.png", "rb").read())

# Author info
def getAuthor():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Img(src="data:image/png;base64,{}".format(encoded_image.decode())
                    , width="500px")], width='6'),
                    dbc.Col([
                        html.Div([
                            html.P('Welcome to the Fraudbusters.'),
                            html.P("xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx"),
                            html.P("xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx"),
                            html.P("This is our project, xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx"),
                            html.P("xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx"),
                            html.P("The Hypothesis:"),
                            html.P("xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx"),
                            html.P("xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx"),
                            html.P("xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx"),
                            html.P("Then, the objective of xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx:"),
                            html.P("1. xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx"),
                            html.P("2. xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx"), 
                            html.P("3. xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx"),
                            html.A("You can find full version of analysis on our Github.","href=xxxxxxxxxxxxxxxxx tbd xxxxxxxxxx"),
                        ])
                    ], width='8')
                ])
                
                
            ],
            )
        )
    ])


app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
               dbc.Row([
                dbc.Col([
                    getAuthor()
                ], width=12),
            ], align='center'), 
            html.Br(),
            dbc.Row([
              dbc.Col([
                    getPlot(fig_transaction, "Fraudulent vs. non-fraudulent transactuins - count", "Only ~0.2% of all transactions are fraud.")
                ], width=5),
                dbc.Col([
                    getPlot(fig_values, "Fraudulent vs. non-fraudulent transactuins - value", "Fraudulent transactions account for ~32% of the overall transaction value.")
                ], width=7),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    getPlot(fig_fraud_product, "Fraudulent transactions by product category", "Most fraudulent transactions refer to Financial Services.")
                ], width=6),
                dbc.Col([
                    getPlot(fig_fraud_days, "Fraudulent transactions by weekday (count)", "Weekday with highest number of fraudulent transactions: Thursday.")
                ], width=6),
            ], align='start'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    getPlot(fig_fraud_hour, "Fraudulent transactions by hour (count)", "Peak of fraudulent transactions: 12:00am.")
                ], width=6),
                dbc.Col([
                    getPlot(fig_customer_history, "xxxxxx tbd xxxxxxx", "xxxxxx tbd xxxxxxx")
                ], width=6),
            ], align='start'),
            dbc.Row([
                dbc.Col([
                    getPlot(fig_fraud_hour, "plot will be replaced", "plot will be replaced")
                ], width=6),
                dbc.Col([
                    getPlot(fig_fraud_hour, "plot will be replaced", "plot will be replaced")
                ], width=6)
            ], align='start'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    getPlot(fig_fraud_hour, "plot will be replaced", "plot will be replaced")
                ], width=4),
                dbc.Col([
                    getPlot(fig_fraud_hour, "plot will be replaced", "plot will be replaced")
                ], width=4),
                dbc.Col([
                    getPlot(fig_fraud_hour, "plot will be replaced", "plot will be replaced")
                ], width=4),
            ], align='start'), 
            html.Br(),    
        ]), color = 'white'
    )
])


if __name__ == '__main__':
    app.run_server()
