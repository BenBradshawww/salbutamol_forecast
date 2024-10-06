from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import r2_score
import numpy as np
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

def arima_training_loop(df, p_val=None, d_val=None, q_val=None):
	p_values = range(0, 5)  # Autoregressive part (AR)
	d_values = range(0, 3)  # Differencing part (I)
	q_values = range(0, 5)  # Moving average part (MA)

	best_aic = np.inf
	best_order = None
	best_model = None

	for p in p_values:
		if p_val is not None:
			p=p_val
			
		for d in d_values:
			if d_val is not None:
				d=d_val

			for q in q_values:
				if q_val is not None:
					q=q_val

				model = ARIMA(df['TOTAL_QUANTITY'], order=(p,d,q))
				model_fit = model.fit()
				
				aic = model_fit.aic
				
				if aic < best_aic:
					best_aic = aic
					best_order = (p, d, q)
					best_model = model_fit

	print(f"Best ARIMA order: {best_order}")
	print(f"Best AIC: {best_aic}")
	return best_model


def model_metrics(true_values, forecast, verbose:int=1):

    true_values = np.array(true_values)
    forecast = np.array(forecast)

    r2 = round(r2_score(true_values, forecast), 3)

    mae = round(np.mean(np.abs(true_values - forecast)), 0).item()

    smape = round(100 * np.mean(2 * np.abs(true_values - forecast) / (np.abs(true_values) + np.abs(forecast))), 3).item()

    if verbose:
        print('R2:', r2)
        print('Mean Absolute Error:', mae)
        print('Symmetric Mean Absolute Percentage Error:', smape)


    return r2, mae, smape

def custom_seasonal_decompose(data, months):
	decomposed = seasonal_decompose(data, model='additive', period=12)

	trend = decomposed.trend
	seasonal = decomposed.seasonal
	observed = decomposed.observed
	
	fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1,
				subplot_titles=('Observed', 'Trend', 'Seasonal', 'Residual'))

	fig.add_trace(go.Scatter(x=months, y=observed, mode='lines', name='Observed'),
			row=1, col=1)

	fig.add_trace(go.Scatter(x=months, y=trend, mode='lines', name='Trend'),
			row=2, col=1)

	fig.add_trace(go.Scatter(x=months, y=seasonal, mode='lines', name='Seasonal'),
			row=3, col=1)


	fig.update_layout(height=800, width=900, title_text="Seasonal Decomposition of Total Quantity of Prescriptions",
				showlegend=False)

	fig.show()


def plot_residuals_acf_and_pacf(residuals):

	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

	plot_acf(residuals, lags=10, ax=ax1)
	ax1.set_title('Autocorrelation Function (ACF) of the Residuals')
	ax1.set_xlabel('Lags')
	ax1.set_ylabel('ACF')

	plot_pacf(residuals, lags=10, method='ywm', ax=ax2)
	ax2.set_title('Partial Autocorrelation Function (PACF) of the Residuals')
	ax2.set_xlabel('Lags')
	ax2.set_ylabel('PACF')

	plt.tight_layout()
	plt.show()