## IKEA-Portfolio-Management

**Explanation**

Answering the question, how would a retail investor perform who invested in a randomly selected, equally-weighted portfolio of Australian companies and held the portfolio without rebalancing? Compared to investing through a retail fund, the strategy benefits from avoiding CG tax drag and management fees.

The results below are generated using Python with data sets webscraped from Yahoo Finance (security prices) and Trading Economics (market capitalisations). The market capitalisations are used to restrict the investable universe to securities larger than 700m at the beginning of the analysed period. This reduces backfill bias in the Yahoo Finance dataset as well as the tendency for equal weight portfolios to have a tilt toward the size risk factor. 

**Results from portfolio_sd.py**

Retail investors are limited in the number of individual securities they can directly hold because as portfolio holdings increase, so does the cost of brokerage as a proportion of their total investment. One of the benefits of investing through a fund is that it makes holding hundreds or even thousands of securities relatively inexpensive. However, investors gain most of the diversification benefit with a relatively small number of portfolio holdings. 

![](image1.png)

**Results from portfolio_returns.py**

Investing through a retail fund comes with a cost that potentially outweigh the benefits of increased diversification and 
convenience. Looking at historic fund statements, I calculate the annual average realised capital gains tax as a percent of investment value to be ~1.21%. Conservatively, assuming that all the capital gains distributed to fund holders are eligible for the 12 month holding period discount and a marginal tax rate of 32.5%, fund holders are subject to 20 bps of tax drag each year. Management fees subtract an additional 7 to 13 bps. The costs are not significant, but do begin to weigh on total return over an extended investment horizon. 

![](image2.png)
