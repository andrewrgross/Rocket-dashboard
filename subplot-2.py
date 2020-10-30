### Rocket Dashboard version 0.1 -- Andrew R Gross -- 2020-10-29

from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()		# This declares the dash object and names it "app"

### Define toggle switches	- These are not used currently
toggle_one_status = 0
toggle_two_status = 0
toggle_three_status = 0
toggle_four_status = 0
slider = 75

# Initialize figure with subplots, starting with the collback function
@app.callback(Output(component_id='page', component_property='figure'), [Input('interval-component', 'n_intervals')])   # The callback decorator
def update_page(n):													# The function the callback wraps
	fig = make_subplots(											# Defining the figure object
	    rows=2, cols=5,											# The number of subfigures in the master figure
	    column_widths=[0.2, 0.2, 0.2, 0.2, 0.2],
	    row_heights=[1.4, 0.8],
	    specs=[[None, {"type": "scattergeo", "colspan": 2}, None, None, {"type": "bar", "rowspan":2}],	# Contents of the subfigures
	           [{"type": "scatter", "colspan": 4}, None, None, None, None]])
	# The next section defines the subfigures
	# This defines a scattergeo figure (the Earth)
	fig.add_trace(
	    go.Scattergeo(mode="markers",
	                  hoverinfo="text",
	                  showlegend=False,
	                  marker=dict(color="crimson", size=4, opacity=0.8)),
	    row=1, col=2 )
	# Figure definition: the four dots (as a scatter plot)
	fig.add_trace(
	    go.Scatter(x=[0,1,2,3.2], y=[1,1,1,1], mode='markers',
	    marker=dict(
        	color=pd.read_csv('test-data.csv').iloc[0].iloc[0:4], opacity = [1,1,1,1],
        	size=[55, 55, 55, 80],
        	showscale=False,
        	colorscale=[[0.0, "rgb(190,190,190)"],
                [1.0, "rgb(240,40,40)"]],
	    line=dict(width=6, color='DarkSlateGrey'))),
     	    row=2, col=1)
	# Figure definition: Throttle bar
	fig.add_trace(
	    go.Bar(y=pd.read_csv('test-data.csv').iloc[0][4:5], width = 0.5,
	    marker=dict(color=pd.read_csv('test-data.csv').iloc[0][4:5], colorscale= 'Peach', cmin = 0, cmax = 100, showscale = True  )),
	    row=1, col=5)
	# Subfigure Parameters - These modify the subfigures
	# Earth parameters
	fig.update_geos(
	    projection_type="orthographic",
	    landcolor="white",
	    oceancolor="MidnightBlue",
	    showocean=True,
	    lakecolor="LightBlue")
	# Paremeters for all plots
	fig.update_yaxes(title_text="Throttle %", range=[0, 100], row=1, col=5)
	fig.update_layout(
	    paper_bgcolor='rgba(0,0,0,0)',
	    plot_bgcolor='rgba(0,0,0,0)',
	    xaxis=dict(
	        autorange=True,
	        showgrid=False,
	        ticks='',
	        showticklabels=False,
		visible=False ),
	    yaxis=dict(
	        autorange=True,
	        showgrid=False,
	        ticks='',
	        showticklabels=False,
		visible=False ),
	    showlegend=False,
	    margin=dict(r=10, t=25, b=40, l=60),
	    annotations=[
	        dict(
	            text="Source: NOAA",
	            showarrow=False,
	            xref="paper",
	            yref="paper",
	            x=0,
	            y=0) ])
	return fig

### The Layout: this defines the page display settings
app.layout = html.Div([
    dcc.Graph(id='page', style={'height':700}),		# The page only has two components: the main figure, and a timer
    dcc.Interval(					# This timer triggers the callback function every 200 ms
            id='interval-component',
            interval=200, # in milliseconds
            n_intervals=0)
])

### The app run command creates and updates the server with the page
app.run_server(debug=False, use_reloader=False)  #
