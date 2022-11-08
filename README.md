## IKEA-Portfolio-Management

**Explanation**

Answering the question, how would a retail investor perform who invested in a randomly selected, equally-weighted portfolio of Australian companies and held the portfolio without rebalancing? Compared to investing through a retail fund, the strategy benefits from avoiding CG tax drag and management fees.

I generated the results using Python with data sets web scraped from Yahoo Finance (security prices) and Trading Economics (market capitalisations). I used the market capitalisations to restrict the investable universe to securities larger than 700m at the beginning of the analysed period. This filtering reduces backfill bias in the Yahoo Finance dataset and the tendency for equal-weight portfolios to tilt toward the size risk factor.

**Results from portfolio_sd.py**

Retail investors are limited in the number of individual securities they can directly hold because as portfolio holdings increase, so does the cost of brokerage as a proportion of their total investment. One of the benefits of investing through a fund is that it makes holding hundreds or even thousands of securities relatively inexpensive. However, investors gain most of the diversification benefit with a relatively small portfolio. 

I calculated the standard deviations for fifty random samples of each number of holdings in the portfolio. Increasing the portfolio size from one to thirty holdings markedly reduces standard deviation, but adding additional holdings thereafter has a diminishing marginal reduction.


![](image1.png)

**Results from portfolio_returns.py**

Investing through a retail fund comes with a cost that potentially outweighs the benefits of increased diversification and convenience. Looking at historic fund statements, I calculate the average annual realised capital gains tax as a percent of investment value to be ~1.21%. Assuming that all the capital gains distributed to fund holders are eligible for the 12-month holding period discount and a marginal tax rate of 32.5%, fund holders are subject to 20 bps of tax drag each year. Management fees subtract an additional 7 to 30 bps. For a comparison portfolio, I used an index fund with a combined tax and management fee drag of 30 bps. 

Given the results of the previous analysis, I used a portfolio size of thirty for each equal-weight portfolio as it captures most of the diversification benefit and is still manageable for a retail investor. I then calculated the total ten-year return for three hundred random samples. In the results pictured, 73% of the portfolios outperformed the Australian index fund but with significant active risk. 

![](image2.png)
