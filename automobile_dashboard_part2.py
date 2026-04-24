import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load dataset
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"

df = pd.read_csv(url)


app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}
    ),

    html.Div([

        # REPORT DROPDOWN
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type'
        ),

        # YEAR DROPDOWN
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in range(1980, 2024)],
            placeholder='Select year'
        ),

        html.Div(
            id='output-container',
            className='chart-grid',
            style={'display': 'flex'}
        )

    ])

])


@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

def update_output_container(selected_statistics, input_year):
    
    if selected_statistics == 'Recession Period Statistics':
        
        # Filter recession data
        recession_data = df[df['Recession'] == 1]

        return html.Div([
            html.H3("Recession Period Statistics Displayed Here")
        ])
    
    elif selected_statistics == 'Yearly Statistics' and input_year is not None:
        
        # Filter yearly data
        yearly_data = df[df['Year'] == input_year]

        return html.Div([
            html.H3(f"Yearly Statistics for {input_year}")
        ])
    
    else:
        return html.Div([
            html.H3("Please select a report type")
        ])

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'),
        Input(component_id='select-year', component_property='value')
    ]
)

def update_output_container(selected_statistics, input_year):

    # ===== RECESSION =====
    if selected_statistics == 'Recession Period Statistics':

        recession_data = df[df['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()

        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                           title="Automobile Sales during Recession"),
                           style={'width': '100%', 'height': '400px'}
        )

        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()

        R_chart2 = dcc.Graph(
            figure=px.bar(avg_sales, x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Sales by Vehicle Type during Recession"),
                          style={'width': '100%', 'height': '400px'}
        )

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title="Ad Expenditure Share during Recession"),
            style={'width': '100%', 'height': '400px'}
        )

        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                          x='unemployment_rate',
                          y='Automobile_Sales',
                          color='Vehicle_Type',
                          title="Unemployment vs Sales"),
            style={'width': '100%', 'height': '400px'}
        )

        return [
            html.Div([R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div([R_chart3, R_chart4], style={'display': 'flex'})
        ]

    # ===== YEARLY =====
    elif selected_statistics == 'Yearly Statistics' and input_year is not None:

        yearly_data = df[df['Year'] == input_year]

        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()

        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales',
                           title="Yearly Automobile Sales Trend")
        )

        mas = df.groupby('Month')['Automobile_Sales'].sum().reset_index()

        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales',
                           title="Monthly Sales")
        )

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()

        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                          title=f"Average Sales in {input_year}")
        )

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title="Ad Expenditure Share")
        )

        return [
            html.Div([Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div([Y_chart3, Y_chart4], style={'display': 'flex'})
        ]

    # ===== DEFAULT =====
    else:
        return html.Div([
            html.H3("Please select a report type")
        ])



if __name__ == '__main__':
    app.run(debug=True)