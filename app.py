import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly as plotly
import plotly.graph_objs as go
import os
import theoretical_funcs

app = dash.Dash(__name__)
server = app.server

colors = {
    'text': '#7FDBFF'
}

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# bring in the data

data_test_100 = np.flipud(np.load('test_E_100.npy'))
data_test_10 = np.flipud(np.load('test_E_10.npy'))
data_test_50 = np.flipud(np.load('test_E_50.npy'))

dataFrame = {'csf_1_mm':data_test_10,'csf_5_mm':data_test_50,'csf_10_mm':data_test_100}

app.layout = html.Div([
    #html.Div([
    html.H2('Visualization of Theoretical Dipole Stimulation'),
    html.Hr(),

    dcc.Dropdown(
                id='type_stim',
                options=[{'label': i, 'value': i} for i in dataFrame.keys()],
                value='csf_10_mm'
                ),
    html.Div(children='Dropdown menu to select CSF thickness of interest', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Input(
        id='x_cord',
        placeholder='Enter an X cord value...',
        type='number',
        value=500
    ),
        html.Div(children='Dropdown menu to select x coord', style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    dcc.Input(
        id='z_cord',
        placeholder='Enter a z cord value...',
        type='number',
        value=500
    ),
    html.Div(children='Dropdown menu to select z coord', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Hr(),
    html.Div([
    dcc.Graph(id='heatmap_efield') ], style={'width': '49%', 'display': 'inline-block', 'padding': '20 20 20 20'}),

    html.Div([
        dcc.Graph(id='x-graph'),
        dcc.Graph(id='z-graph'),
    ], style={'display': 'inline-block', 'width': '49%','padding': '20 20 20 20'}),

    html.Hr(),
    html.Div(children='Slider to control range of the plot', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div(dcc.RangeSlider(
        id='max_val',
        min=0,
        max=1100,
        value=[0,500],
        step=10,
        marks={i: '{}'.format(i) for i in range(0,1101,50)},),
        style={'width': '49%', 'padding': '0px 20px 20px 20px'}
    ),


    ])
    #],
    #style = {'display': 'inline-block', 'width': '48%'})

@app.callback(
    dash.dependencies.Output('heatmap_efield', 'figure'),
    [dash.dependencies.Input('type_stim','value'),
    dash.dependencies.Input('max_val', 'value')])
def update_figure(data_input,selected_range):
    maximum_val = int(selected_range[1])
    minimum_val = int(selected_range[0])
    data_input_select = dataFrame[data_input]
    return {
        'data': [
            #go.Contour([data])
            go.Heatmap(
                z=data_input_select,
             colorscale='Reds',
             zauto = 'false',
             zmin=minimum_val,
             zmax=maximum_val)
        ],
        'layout': go.Layout(
        xaxis={'title':'x dimension'},
        yaxis={'title': 'depth'},
        title='Plots of simulated field effects',
        margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
        height=450,
        )
    }

@app.callback(
    dash.dependencies.Output('x-graph', 'figure'),
    [dash.dependencies.Input('type_stim','value'),
    dash.dependencies.Input('x_cord','value')])
def update_x(data_input,x_cord_val):
    data_input_select = dataFrame[data_input]
    data_x = data_input_select[:,x_cord_val]
    indep_axis_x = len(data_x)
    return {
        'data': [
            #go.Contour([data])
            go.Scatter(
                x=indep_axis_x,
                y=data_x)
        ],
        'layout': go.Layout(
        xaxis={'title':'x dimension'},
        yaxis={'title': 'depth'},
        title='Plots of simulated field effects',
        height= 225,
        margin= {'l': 40, 'b': 40, 'r': 40, 't': 40},
        )
    }

@app.callback(
    dash.dependencies.Output('z-graph', 'figure'),
    [dash.dependencies.Input('type_stim','value'),
    dash.dependencies.Input('z_cord','value')])
def update_z(data_input,z_cord_val):
        data_input_select = dataFrame[data_input]
        data_z= data_input_select[z_cord_val,:]
        indep_axis_z = len(data_z)
        return {
        'data': [
            #go.Contour([data])
            go.Scatter(
                x = indep_axis_z,
                y= data_z)
        ],
        'layout': go.Layout(
        xaxis={'title':'x dimension'},
        yaxis={'title': 'depth'},
        title='Plots of simulated field effects',
        height = 225,
        margin = {'l': 40, 'b': 40, 'r': 40, 't': 40},
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
