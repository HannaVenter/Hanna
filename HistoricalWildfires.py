from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import datetime as dt

app=Dash()
df=pd.read_csv('Historical_Wildfires.csv')

df['Month']=pd.to_datetime(df['Date']).dt.month_name()
df['Year']=pd.to_datetime(df['Date']).dt.year

app.layout = html.Div([
    html.H1('Australia Wildfire Dashboard',
            style={'textAlign':'center',
                   'color':'#503D36',
                   'font-size':26}),
    html.Div([
        html.Div([
            html.H2('Select Region:', style={'margin-right':'2em'}),
            dcc.RadioItems([{'label':'New South Wales','value':'NSW'},
                            {'label':'Victoria','value':'VI'},
                            {'label':'Tasmania','value':'TA'},
                            {'label':'Queensland','value':'QL'},
                            {'label':'Northern Territory','value':'NT'},
                            {'label':'South Australia','value':'SA'},
                            {'label':'Western Australia','value':'WA'}],
                           id='region-selected',
                           value='NSW',
                           inline=True)]),
        html.Div([
            html.H2('Select Year:', style={'margin right':'2em'}),
            dcc.Dropdown(df.Year.unique(), id='year-selected', value=2005)]),
        html.Div([
            html.Div([ ],id='pie-chart'),
            html.Div([ ],id='bar-graph')],
            style={'display':'flex'})
    ])
])


@app.callback(
    Output('pie-chart', 'children'),
    Output('bar-graph', 'children'),
    Input('region-selected', 'value'),
    Input('year-selected', 'value')
)
def update_graphs(input_region,input_year):
    region_data = df[df['Region'] == input_region]
    year_data = region_data[region_data['Year']==input_year]

    est_data = year_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()

    fig1 =px.pie(est_data, values='Estimated_fire_area', names='Month', title='{} : Monthly Average Estimated Fire Area in {}'.format(input_region,input_year))

    veg_data =year_data.groupby('Month')['Count'].mean().reset_index()

    fig2 = px.bar(veg_data,x='Month',y='Count', title='{} : Average Count of Pixels for Presumed Vegetation Fires in {}'.format(input_region,input_year))

    return [dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)]

if __name__ == '__main__':
    app.run(debug=True)