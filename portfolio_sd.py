import yfinance as yf
import os
import getpass
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

results = pd.DataFrame([])


# Number of securities in largest portfolio size

NO_MAX_SECURITIES = 90

# Number of random samples included in each portfolio size

NO_SIMULATIONS = 50

# Included companies must have a market cap of 1 bn 

mktcap_df = pd.read_csv('INPUT_company_mktcaps.csv')

MKTCAP_REQ_DATE = '2012-H1'

MKTCAP_REQ = 700000000

mktcap_df = mktcap_df[mktcap_df[MKTCAP_REQ_DATE] > MKTCAP_REQ]

# Import company price data

prices_df = pd.read_csv('INPUT_yahoo_prices.csv')

# Reverse price order from most recent to least recent

prices_df = prices_df[::-1]

# Find difference between t and t-1 

returns_df = prices_df.iloc[:,1:].pct_change()

# Revert back to most recent order

returns_df = returns_df[::-1]

# Reduce data frame to 10 years of data, excluding companies without a complete return series

TIME_PERIOD = 120

returns_df = returns_df.loc[1:TIME_PERIOD, :]

returns_df = returns_df.dropna(axis=1, thresh=TIME_PERIOD)

# Exclude companys from return series without the specified market cap

returns_df = returns_df[returns_df.columns.intersection(mktcap_df['Period'])]

# Covariance dataframe

cov_df = returns_df.cov()

# Select column 

sample_column = cov_df.iloc[0]

list_sample = sample_column.index.to_list()

# Outer loop - number of securities in portfolio (portfolio size) - i
    
for i in range(NO_MAX_SECURITIES, 0, -1):

    # Inner loop - simulations number - t

    for t in range(0, NO_SIMULATIONS):

        print("Number of securities in portfolio: ", i," & Simulation number: ", t)

        # Randomaly select securities to be included in portfolio

        sample = sample_column.sample(n = i, replace=False)

        # Convert sample from type dataframe to list

        list_sample = sample.index.to_list()

        # Trim covaraiance matrix to only include companies in the sample

        temp_df = cov_df[cov_df.index.isin(list_sample)]

        temp_df = temp_df[temp_df.columns.intersection(list_sample)]

        # Equal weights for each portfolio holding

        weights = np.full(shape = i,  fill_value = (1/i))

        # Weights x Covariance Matrix x Weights.T

        cov_np = temp_df.to_numpy()

        variance = np.matmul(cov_np, weights)

        variance = np.matmul(variance, np.transpose(weights))

        # Annualised SD - x sqrt(12 months)

        results.loc[i, t] = math.sqrt(variance * 12)

# Average column

results['Average SD'] = results.mean(axis = 1)

# Percentile columns - first value in dictionary is shortening column range so that the average column or other percentile columns are not included
# in the calculation. 

percentiles = {'Q1 - 25th Percentile:': [1,0.25], 'High - 95th Percentile:': [2,0.95], 'Low - 5th Percentile': [3,0.05], 'Q3 Percentile - 75th Percentile': [4,0.75]}

for key, value in percentiles.items():

    results[key] = results.iloc[:,:-value[0]].quantile(value[1], axis=1)

results.to_csv('OUTPUT_portfolio_sd_securities-' + str(NO_MAX_SECURITIES) + '_simulations-' + str(NO_SIMULATIONS) + '.csv')
 
# Plot results

ax=plt.subplot()

ax.set_title('Australian Equity Portfolio Standard Deviation with \n ' + str(NO_SIMULATIONS) + ' Simulations of Randomly Selected, Equal-Weight Holdings \n Monthly Returns (11-2012 to 11-2022)')

ax.plot(results.index, results["Average SD"], label='Mean', color='deepskyblue')
ax.plot(results.index, results["High - 95th Percentile:"], label='95th Percentile', color='skyblue')
ax.plot(results.index, results["Low - 5th Percentile"], label='5th Percentile',color='skyblue')
ax.legend()
ax.set_xlabel('Number of Portfolio Holdings')
ax.set_ylabel('Standard Deviation')

plt.xlim(0, 90)
plt.ylim(0, 0.7)

plt.yticks(np.arange(0, 0.7, 0.05))

plt.show()