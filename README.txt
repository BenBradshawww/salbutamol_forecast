Chapters

	1.	Summary
    2.  Installation Instructions
	3.  Repo Breakdown
	4.	Data
	5.	Medication Details
	6.	Limitations
	7.	Methodology
	8.	Results
	9.  Next Steps
	10. Follow Up Questions

1. Summary

This analysis aims to forecast the total quantity of Salbutamol 2.5mg prescriptions for the year 2024, using historical data from the past three years. By leveraging the English Prescribing Dataset (EPD), we will model trends and predict future prescription volumes. The focus will be on national and regional patterns, aggregated at the county level due to data variability at a monthly scale.

2.  Installation Instructions

Prerequisites:
- Python 3.8 or higher
- pip (Python package manager)

To install the dependecies:

```bash
pip install -r requirements.txt
```

3. Repo Breakdown

│
├── forecast_salbutamol.py/         # Salbutamol jupyter notebook
├── README.md           			# Project documentation
├── requirements.txt    			# Python dependencies
├── misc.py 			   			# Python dependencies
├── training.py    			        # Python training and plotting scripts.
└── visualization.py            	# Python  file for the project

To reproduce the results, run the forecast_salbutamol jupyter notebook. This file will take 10 minutes to run given it has to get the data from the NHS website.

4. Data

We will be using an API to extact the NHS English Prescribing Dataset (EPD).

The EPD provides comprehensive data on prescriptions issued and dispensed across England, Wales, Scotland, and the Channel Islands (Guernsey, Alderney, Jersey, Isle of Man). 
Some of the fields from the EPD dataset include:

	•	Items: The total number of times a medicine, dressing, or appliance appeared on prescription forms, prescribed and dispensed.
	•	Quantity: The quantity of a prescribed medicine or item, representing an approximation of pack size, helping illustrate typical prescribed amounts.
	•	Total Quantity: Calculated as the product of Quantity and Items, representing the total prescribed quantity for each BNF (British National Formulary) presentation.
	•	Net Ingredient Cost (NIC): The price of prescribed items, typically based on the Drug Tariff or published wholesale prices.
	•	Actual Cost: The NIC adjusted for discounts and payments to dispensers.
	•	ADQ Usage: The Average Daily Quantity (ADQ), representing a typical daily dose prescribed for adult patients.
	•	Practice Details: Including the name and address of prescribing GP practices, where available.
	•	Unidentified: A flag for prescriptions where the issuing practice could not be identified.
	•	Year Month: The Year and Month as YYYYMM.

From these fields we will be using `Total Quantity` as the field to forecast in this investigation.

5. Medication Details

Since the EPD contains information on all the prescriptions in the UK, to isolate the perscriptions of Salbutamol I filtered for the `Chemical Substance BNF Description` of 'Salbutamol'.
To ensure the prescriptions only include perscriptions 2.5mg, we have filtered for `BNF Description`s including 2.5mg. 
Upon further inspection of the `BNF Description`s some other drugs appeared. These drugs included Ventolin, Combivent, Ipramol, Salamol, Combriprasal, and Brodilaten which were all classified as Salbutamol .
After consulting a pharmacists I found out that Salamil and Ventolin were purely Salbutamol. 
For the drugs Ipramol, Combivent, and Combriprasal, they consisted of the drugs Salbutamol and Ipratropium. 
Since these drugs still contained Salbutamol I decided to still include them in my dataset (if they appeared in the dataset).
Finally, Brodilaten was Salbutamol in a nebuliser solution. Which I also classified as Salbutamol.


6. Limitations

The most important limitation came from the use of using the `Total Quantity` of prescription to forecast future prescription rates. 
In the first half of 2024, there was an shortage of Salbutamol, as a result the prescriptions of Salbutamol were replaced with prescriptions of Ipatropium nebules.
Consequently, the forecast in 2024 may become problematic. A next step in this project would involve combining total prescriptions for Salbutamol and Ipatropium nebules. This would conteract the lower prescriptions in 2024.

The initial brief mentioned 3 months could be used for forecast. I extended this data to 3 years of data because I was worried 3 months of data would be insufficient to create accurately forecast given the model would not have even had 1 full caledar cycle and so it would be unable to learn the seasonal trends. 

7. Methodology
The data was gathering from the NHS Business Service Authority using the `requests` python package and was cleaned using the pandas package. 

This investigation will forecast the `TOTAL_QUANTITY` of prescriptions within the UK rather than forecasting at a regional or at a practice level due to time constraints. 
To model the `TOTAL_QUANTITY` of prescriptions in the UK, I will be using the 3 years of data from January 2021 to December 2023 to forecast the next 6 months worth of prescriptions (January 2024 - December 2024).

To perform the forecasts, I will apply 3 models to try to model the total quantity of prescriptions. 
	• ARIMA. The first model was an ARIMA model which focuses on trends and autocorrelations patterns perform its forecasts. ARIMA's limitation in this setting is that it does not use any seasonal information which will lead be a limitation.
	• SARIMA. This model is a seasonal variant of ARIMA and introduces 3 new hyper-parameters called the seasonal autoregressive (SAR) terms, seasonal differencing (D), and seasonal moving average (SMA) terms. As a result, SARIMA is able to capture both the seasonal and non-seasonal patterns. 
	• Prophet. The final model which was tested was the Prophet model by Facebook. Not only does this model capture the seasonality data but it can adapt to outliers, missing data, robust to large datasets, provides confidences intervals, and is simply easy to use.

For each of these models, no form of feature engineering was performed, ARIMA and SARIMA incorporate their own lag and moving average parameters. 
However, the model which would benefit from feature engineering is the Prophet model. This will be revisted for a later project.

To evaluate the performance of these models I will look at the R Squared, Mean Average Error, and the Symmetric Mean Absolute Percentage Error of the forecast predictions. In addition, I will look at distribution of the residuals and the forecasts to ensure the model has been correctly fitted.

8. Results
These results correspond to our 6 month forecasts.

	• ARIMA. R2: -10.424, MAE: 137946.0, SMAPE: 8.501
	• SARIMA. R2: -9.139, MAE: 128614.0, SMAPE: 7.91
	• Prophet. R2: -24.731, MAE: 187045.0, SMAPE: 11.161

On initial inspection of the results the SARIMA model has performed the best and the Prophet model has performed the worst.
On post model inspection, the model seemed to have fit well with the data with no further suggested changes in hyper-parameters.
The only areas of concerns were that each model would have 1 or 2 outlier predictions where total quantity of prescriptions were massively over-estimated or under-estimated by up to 2 million prescriptions.

ARIMA:
	• The ARIMA model achieved the second best results with a SMAPE of 8.501 (i.e. on average 8.501% off on its predictions).	
	• There was 1 major outlier when the model's training residuals were investigated. This residual suggested 2 million more total prescription would be created.
	• Another limitation of ARIMA was that it sturggled to incroporate seasonality information into the forecasts.

SARIMA:
	• SARIMA achieved the lowest SMAPE of 7.91 (i.e. on average 7.91% off on its predictions) and achieved the lowest absolute error. 
	• On inspection of the training data residuals, SARIMA performed well but had 2 outliers where total prescriptions were over and under predicted by 2 million. This massive under prediction is a major concern.
	• In general, SARIMA captured the seasonal information well by forecasting higher prescriptions in the christmas months and during pollen seasons.

Prophet:
	• Prophet achieved the lowest SMAPE of 11.161 (i.e. on average 11.16% off on its predictions).
	• In general, Prophet
	•



9. Next Steps
	• It would be interesting to apply these models to a more local scale such as by region code or even attempt this analysis at a practice level.
 	• As mentioned before, it would make sense to incorporate the prescriptions of Ipatropium nebules in the forecasts of Salbutamol prescriptions.
	• It would like to incroporate other features into the model, such as pollination count.
	• I would like to try out a variant of the GARCH model. This was initially built for forecasting volatility in the financial market. It could be applicable in this setting where there exists high volatility.

