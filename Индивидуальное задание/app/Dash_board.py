import os
import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import joblib


# Функция для чтения данных из файла
def read_SLAM_data(file_path):
    data = pd.read_csv(file_path, delim_whitespace=True, skiprows=40, usecols=[0, 1, 2, 3, 4, 5, 6, 7], header=None)
    data.columns = ['YYYY', 'MM', 'DD', 'HH', 'MJD', 'SLAM_x', 'SLAM_y', 'SLAM_z']
    return data

directory_path = './SLAM/'


def predict_values(values, component):
    filename = f'sarima_model_{component}.pkl'

    with open(filename, 'rb') as file:
        sarima_model = joblib.load(file)

    pred = sarima_model.predict(start=1, end=len(values))

    return pred

# Получение уникальных годов из файлов в директории и чтение данных
files = os.listdir(directory_path)
file_paths = [os.path.join(directory_path, file) for file in files if file.endswith('.asc') and 'SLAM' in file]

all_data = {}
for file_path in file_paths:
    year = int(file_path.split('_')[-1][:4])
    if year not in all_data:
        all_data[year] = read_SLAM_data(file_path)

# Создание списка годов для выбора
years = [{'label': str(year), 'value': year} for year in all_data.keys()]

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='year-dropdown',
        options=years,
        value=list(all_data.keys())[0]  # Устанавливаем значение по умолчанию на первый год
    ),
    html.Div([
        html.Div([
            dcc.Graph(id='SLAM-x-graph'),
        ], style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='SLAM-y-graph'),
        ], style={'width': '33%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='SLAM-z-graph'),
        ], style={'width': '33%', 'display': 'inline-block'})
    ]),
    html.Div(id='statistics-table')
])

@app.callback(
    [Output('SLAM-x-graph', 'figure'),
     Output('SLAM-y-graph', 'figure'),
     Output('SLAM-z-graph', 'figure'),
     Output('statistics-table', 'children')],
    [Input('year-dropdown', 'value')]
)




    
def update_graph(selected_year):
    data = all_data[selected_year]
    
    fig_x = go.Figure()
    fig_y = go.Figure()
    fig_z = go.Figure()
    
    fig_x.add_trace(go.Scatter(x=data['MJD'], y=data['SLAM_x'], mode='lines', name='SLAM_x', line=dict(color='blue')))
    fig_y.add_trace(go.Scatter(x=data['MJD'], y=data['SLAM_y'], mode='lines', name='SLAM_y', line=dict(color='red')))
    fig_z.add_trace(go.Scatter(x=data['MJD'], y=data['SLAM_z'], mode='lines', name='SLAM_z', line=dict(color='green')))

    pred_x = predict_values(values=data['SLAM_x'].values, component='x')
    pred_y = predict_values(values=data['SLAM_y'].values, component='y')
    pred_z = predict_values(values=data['SLAM_z'].values, component='z')

    # Добавление предсказанных значений на графики
    fig_x.add_trace(go.Scatter(x=data['MJD'], y=pred_x, mode='lines', name='Predicted SLAM_x', line=dict(color='orange')))
    fig_y.add_trace(go.Scatter(x=data['MJD'], y=pred_y, mode='lines', name='Predicted SLAM_x', line=dict(color='orange')))
    fig_z.add_trace(go.Scatter(x=data['MJD'], y=pred_z / 20, mode='lines', name='Predicted SLAM_x', line=dict(color='orange')))

    # Обновление макета графика
    fig_x.update_layout(title=f'Predicted SLAM_x Values for {selected_year}', showlegend=True)
    fig_x.update_layout(title=f'SLAM_x Values for {selected_year}', showlegend=True)
    fig_y.update_layout(title=f'SLAM_y Values for {selected_year}', showlegend=True)
    fig_z.update_layout(title=f'SLAM_z Values for {selected_year}', showlegend=True)



    # Вычисление статистики
    statistics = {
        'SLAM_x': data['SLAM_x'].describe(),
        'SLAM_y': data['SLAM_y'].describe(),
        'SLAM_z': data['SLAM_z'].describe()
    }

    statistics_table = html.Table([
        html.Tr([html.Th('Statistic'), html.Th('SLAM_x'), html.Th('SLAM_y'), html.Th('SLAM_z')]),
        *[html.Tr([html.Td(stat, style={'whiteSpace': 'pre-wrap'})] + [html.Td(statistics[component][stat]) for component in ['SLAM_x', 'SLAM_y', 'SLAM_z']]) for stat in statistics['SLAM_x'].index]
    ])

    return fig_x, fig_y, fig_z, statistics_table

import logging
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app.run_server(debug=True)
    logger.info("Dash server started")
    #webbrowser.open('http://127.0.0.1:8050/')