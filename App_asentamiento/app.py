from dash import Dash, html,dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Base de datos
from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://cagomezj:1234@cluster0.lg8bsx8.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.sensores.sensor_1
result = 0

# Declarar data_dist fuera de la función para evitar el UnboundLocalError
data_dist = []

# Definir el diseño de la aplicación
app.layout = html.Div([
    # Contenedor principal con display:flex
    html.Div([
        # Primer contenedor (izquierda)
        html.Div([
            html.H1("Proyecto: Asentamiento Tuneladora", style={'text-align': 'center', 'color': 'white', 'margin-top': '20px'}),
            html.P("Una tuneladora, T.B.M. (del inglés Tunnel Boring Machine) o minador a sección completa es una máquina capaz de excavar túneles a sección completa, a la vez que colabora en la colocación de la entibación para la sustentación del túnel si ésta es necesaria, ya sea de forma provisional o definitiva.", style={'text-align': 'center', 'color': 'white'}),
            html.Img(src='https://i.ytimg.com/vi/4b4RDFwxgBI/maxresdefault.jpg', alt='Asentamiento Tuneladora', style={'width': '100%'}),
            html.H3("A continuación se muestra el sentamiento en tiempo real, medido por el sensor ultrasonico HC-SR04",style={'text-align': 'center', 'color': 'white','margin-top': '30px'}),
        ], style={'flex': '48%', 'padding': '2%'}),

        # Segundo contenedor (derecha)
        html.Div([
            html.H1("Asentamiento Tuneladora", style={'text-align': 'center', 'color': 'white', 'margin-top': '10px'}),
            html.Hr(style={'background-color': 'white'}),
            html.H4(id='distancia-actual', style={'text-align': 'center', 'color': 'white'}),
            dcc.Graph(id='asentamiento'),
            dcc.Interval(
                id='interval-component',
                interval=1 * 500,  # en milisegundos, actualiza cada 1 segundo
                n_intervals=0
            ),
            html.Div(id='alerta-texto', style={'text-align': 'center', 'margin-top': '10px'}),
        ], style={'flex': '48%', 'padding': '2%'}),
    ], style={'background-color': '#272727', 'padding': '40px'})
])

@app.callback(
    [Output('asentamiento', 'figure'),
     Output('distancia-actual', 'children'),
     Output('alerta-texto', 'children')],
    [Input('interval-component', 'n_intervals')]
)


def consultar(n):
    
    # Utilizar la variable global data_dist
    global data_dist , result , db
    result = db.find_one(sort=[('updated_at', -1)])
    distancia = int(result['distancia'])
    data_dist.append(distancia)
    
    # Crear el objeto de figura de Plotly
    fig = go.Figure(data=[go.Scatter(y=data_dist, mode='lines+markers')])
    
     # Agregar una línea horizontal en y=5
    fig.add_shape(
        type="line",
        x0=0,
        x1=len(data_dist),
        y0=1600,
        y1=1600,
        line=dict(color="red", width=2),
    )
    
    # Agregar un texto según la condición
    if distancia >= 1600:
        alerta_texto = html.Span("ALERTA", style={'color': 'red', 'font-size': '24px'})
    else:
        alerta_texto = html.Span("VAMOS BIEN", style={'color': 'green', 'font-size': '24px'})
    
    
    # Formatear la distancia para mostrarla en el H1
    distancia_texto = f"El asentamiento fue: {distancia} cm"
    
    return fig, distancia_texto,alerta_texto
# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
