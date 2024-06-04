from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })
df = pd.read_excel('Notebooks\\Case Navios Tanque\\BaseNTFinalDeles.xlsx')
id = list(df['ID'].unique())
id.append('Todos os casos')
fig = px.bar(df, x="ID", y="Início",color="Ocorrência", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Graficos Pm4py'),
    html.H2(children= 'Performance'),

    dcc.Dropdown(id, value='Todos os casos', id='selecID'),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server (debug=True)