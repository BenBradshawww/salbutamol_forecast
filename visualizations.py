from plotly import graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def plot_histogram(values, title:str, x_axis_title:str):

	trace = go.Histogram(x=values, nbinsx=25, texttemplate="%{y}", textposition='outside') 

	fig = go.Figure(data=[trace])

	fig.update_layout(
		xaxis_title=x_axis_title,
		yaxis_title="Frequency",
		width=800,
		height=600,
		title={
			'text': title,
			'x': 0.5, 
			'y': 0.95,
			'xanchor': 'center',
			'yanchor': 'top',
		}
	)

	fig.show()



def plot_counts(df:pd.DataFrame, title:str, x_axis_title:str):

	df.sort_values(by=['TOTAL_QUANTITY'], inplace=True, ascending=False)

	x = df['BNF_DESCRIPTION'].tolist()
	y = df['TOTAL_QUANTITY'].tolist()

	bar_plot_trace = go.Bar(
			x=x,
			y=y,
			text=y,
			textposition='outside'
	)

	fig = go.Figure(data=[bar_plot_trace])

	fig.update_layout(
		width=1200,
		height=800, 
		xaxis_title=x_axis_title,
		xaxis_title_font=dict(size=15),
		yaxis_title="Counts",
		yaxis_title_font=dict(size=15),
		title={
		'text': title,
		'x': 0.5, 
		'y': 0.95,
		'xanchor': 'center',
		'yanchor': 'top',
	},
	)

	fig.show()



def plot_combined_regions(df, title:str, y_axis_title:str):

	fig = go.Figure()

	for region in df['REGIONAL_OFFICE_NAME'].unique().tolist():

		region_df = df[df['REGIONAL_OFFICE_NAME']==region]

		fig.add_trace(go.Scatter(
			x=region_df['YEAR_MONTH'],
			y=region_df['TOTAL_QUANTITY'],
			mode='lines+markers',
			name=region
		)
		)

	fig.update_layout(
	title=title,
	xaxis_title='Month',
	yaxis_title=y_axis_title
	)

	fig.show()



def plot_individual_regions(df, title):
	
	regions = df['REGIONAL_OFFICE_NAME'].unique().tolist()
	
	fig = make_subplots(rows=4, cols=2, subplot_titles=regions, shared_xaxes=True, shared_yaxes=False)


	for index, region in enumerate(regions):
		
		region_df = df[df['REGIONAL_OFFICE_NAME']==region]

		fig.add_trace(go.Scatter(
			x=region_df['YEAR_MONTH'],
			y=region_df['TOTAL_QUANTITY'],
			mode='lines+markers'
		), row=1+(index//2), col=1+(index%2))


	fig.update_layout(
		width=1200,
		height=600, 
		title=title,
		showlegend=False
	)

	fig.show()

def result_prediction(train_list, test_list, forecast_list, train_months, test_months, model_name:str):

	fig = go.Figure()

	total_baseline = train_list+test_list
	total_months = train_months+test_months


	fig.add_trace(go.Scatter(
		x=total_months,
		y=total_baseline,
		mode='lines+markers',
		name='true_values'
	)
	)

	fig.add_trace(go.Scatter(
		x=[train_months[-1]] + test_months,
		y=[train_list[-1]] + list(forecast_list), 
		mode='lines+markers',
		line=dict(color='black', width=2, dash='dash'),
		name='prediction'
	)
	)

	fig.update_layout(
	title=f'{model_name} Predictions for the Total Quantity of Prescriptions',
	xaxis_title='Month',
	yaxis_title='Total Quantity'
	)

	fig.show()

def plot_region(df, region):

	fig = go.Figure()

	region_df = df[df['REGIONAL_OFFICE_NAME']==region]

	fig.add_trace(go.Scatter(
		x=region_df['YEAR_MONTH'],
		y=region_df['TOTAL_QUANTITY'],
		mode='lines+markers',
		name=region
	)
	)

	fig.update_layout(
	title=region+' Total Quantity of Prescriptions',
	xaxis_title='Month',
	yaxis_title='Total Quantity'
	)

	fig.show()


def plot_all_regions(x_data, y_data, title):

	fig = go.Figure()

	fig.add_trace(go.Scatter(
		x=x_data,
		y=y_data,
		mode='lines+markers'
	)
	)

	fig.update_layout(
	title=title,
	xaxis_title='Month',
	yaxis_title='Total Quantity'
	)

	fig.show()


def plot_residuals(x_data, y_data, title):

	fig = go.Figure()

	fig.add_trace(go.Scatter(
		x=x_data,
		y=y_data,
		mode='lines+markers'
	)
	)

	fig.update_layout(
	title=title,
	xaxis_title='Month',
	yaxis_title='Total Quantity Residuals'
	)

	fig.show()


def plot_fitted_vs_residuals(fitted_values, residuals):

	fig = go.Figure()

	fig.add_trace(go.Scatter(
	x=fitted_values,
	y=residuals,
	mode='markers',
	name='Residuals',
	marker=dict(color='blue', size=6)
	))

	fig.add_shape(type='line',
			x0=min(fitted_values), x1=max(fitted_values),
			y0=0, y1=0,
			line=dict(color='red', dash='dash'),
			name='Zero Line')

	
	fig.update_layout(
	title='Residuals vs Fitted Values',
	xaxis_title='Fitted Values',
	yaxis_title='Residuals',
	showlegend=False
	)

	
	fig.show()