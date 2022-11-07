import pandas as pd

import numpy as np

import random

import math

import matplotlib.pyplot as plt

# Number of portfolios with random and equal-weighted holdings

PORTFOLIO_NO = 300

# Portfolio holdings

SECURITIES_NO = 30

# Number of monthly returns

TIME_PERIOD = 120

# Comparison portfolio - index fund return post tax-drag 

INDEX_RETURN = 1.4439706992183

INDEX_SD = 0.135882829652592

# Specify market cap required for company inclusion 

MKTCAP_REQ = 700000000

MKTCAP_REQ_DATE = '2012-H1'

# _______________________________________________________________________________

# Dataframe for storing weights of portfolio holdings 

rescaled_weights_df = pd.DataFrame([])

results_df = pd.DataFrame([])

# Import monthly returns for companies

returns = pd.read_csv('INPUT_returns.csv')

# Exclude first column

returns = returns.iloc[:,1: ]

# Exclude all companies with market capitalisations below specified threshold

mktcap_df = pd.read_csv('INPUT_company_mktcaps.csv')

mktcap_df = mktcap_df[mktcap_df[MKTCAP_REQ_DATE] > MKTCAP_REQ]

returns = returns[returns.columns.intersection(mktcap_df['Period'])]

# Reverse order of returns (to most r
# ecent first) 

returns = returns.iloc[::-1] + 1

# Exclude returns outside specified time period

returns = returns.iloc[0:TIME_PERIOD, :]

# Exclude companies with insufficient return data

returns = returns.dropna(axis = 1,thresh=TIME_PERIOD)

# List of all company tickers from which to draw random samples

company_list = returns.columns[1:].to_list()

# Create dataframe of covariances

cov_df = returns.cov()


# Create portfolios with random equal-weighted holdings and calculate total portfolio return

for t in range(0, PORTFOLIO_NO):

    # Draw sample 

    sample = random.sample(company_list, SECURITIES_NO)

    # Isolate return series and covariance matrix of sampled companies

    temp_returns_df = returns[returns.columns.intersection(sample)]

    temp_cov_df = cov_df[cov_df.index.isin(sample)]

    temp_cov_df = temp_cov_df[temp_cov_df.columns.intersection(sample)]

    # Calculate initial equal-weights

    initial_weights = np.full(shape= SECURITIES_NO, fill_value = (1/SECURITIES_NO))

    # Convert equal-weights to dataframe and include in scaled weights dataframe

    initial_weights_df = pd.DataFrame(initial_weights).T

    # Use company names as column titles for weights data frame

    initial_weights_df.columns = temp_returns_df.columns

    # The rescaled weights dataframe supports weights that change through time (rebalancing, entrants and exits).
    # This is redundant for the case of an equal-weighted portfolio without rebalancing and could instead be achieved by 
    # simply multiplying each company's total return by the start of period weight. 

    rescaled_weights_df = pd.concat([rescaled_weights_df, initial_weights_df])

    return_series_length = len(temp_returns_df) - 1

    temp_returns_df = temp_returns_df.reset_index(drop=True)

    # Covariance - Need to test this

    covariance = np.dot(initial_weights_df, temp_cov_df)

    covariance = np.dot(covariance, initial_weights_df.T) 

    results_df.loc[t, 'Standard Deviation'] = math.sqrt(covariance * 12)

    # Each weight calculated as: Weight_t = Return_t x Weight_t-1

    for i in range(return_series_length, 0, -1):

        weights = initial_weights * temp_returns_df.iloc[i, :]

        rescale_total = weights.sum()

        rescaled_weights = weights / rescale_total

        rescaled_weights_df = pd.concat([rescaled_weights_df, rescaled_weights.to_frame().T])

        initial_weights = rescaled_weights

    rescaled_weights_df = rescaled_weights_df.iloc[::-1]

    rescaled_weights_df = rescaled_weights_df.reset_index(drop=True)

    temp_returns_df = temp_returns_df - 1 

    # Returns x Weights

    temp_returns_df = rescaled_weights_df * temp_returns_df

    # Calculate portfolio monthly returns 

    temp_returns_df['Return'] = temp_returns_df.sum(axis = 1) + 1

    # Calculate portfolio total return

    total_return = (temp_returns_df['Return'].product()) - 1

    # Save portfolio total return to results dataframe 

    results_df.loc[t, 'Return'] = total_return

    results_df.loc[t, 'Portfolio Holdings'] = ', '.join(temp_returns_df.columns[:-1])

    # Clear data frames after each iteration, otherwise columns indexes remain and result in incrementally larger 
    # dataframe dimensions. 

    del initial_weights_df

    del rescaled_weights_df

    del temp_returns_df

    rescaled_weights_df = pd.DataFrame([])

results_df.to_csv('OUTPUT_' + str(TIME_PERIOD/12) + 'years-' + str(SECURITIES_NO) + 'securities-' + str(PORTFOLIO_NO) +'portfolios.csv')

results_df['Outperformed'] = results_df['Return'] > INDEX_RETURN

print(len(results_df[results_df['Outperformed'] == True].index))

ax=plt.subplot()

ax.scatter(results_df['Standard Deviation'], results_df['Return'], label = 'Equal-weight portfolios', c ="deepskyblue")

ax.scatter(INDEX_SD,INDEX_RETURN, label = 'Index fund post-tax drag', c ="darkred")

ax.set_title('Australian Equity Portfolio Returns \n with ' + str(PORTFOLIO_NO) + ' Simulations of 30 Randomly Selected, Equal-Weight Holdings \n Monthly Returns (11-2012 to 11-2022)')

ax.set_xlabel("Standard Deviation")
ax.set_ylabel("Total Return - 10 Years")

ax.legend()

plt.xlim(0.12, 0.22)
plt.ylim(0, 4)

plt.show()

