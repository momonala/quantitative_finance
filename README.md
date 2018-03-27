# Probabilistic Stock Analysis 

"Man is a deterministic device in a probabilistic universe" - Amos Tversky & Danny Kahneman 

This experiment is based on an idea which the two aforementioned Israeli psychologists researched: that though the human mind can solve incredibly complex problems, like vision, it is systematically erred when forced to make simpler probabilistic judgements. Like investing! 

Our minds are particularly susceptible to warping current decisions based on the availability of recent events. For example, if a company puts out a good earnings report for their previous quarter, everyone rushes to invest. But most of those same people will tell you that the past behavior of a stock tells you nothing about its future.  With an investment strategy, we want to make money regardless of changes to tax codes or whether there is a coup in Turkey. If a stock can be treated more like a random variable, we can root out the probabilistic nature of its behavior, and resist the fallacies in our thinking. 

## Z-Score Trading Thresholds 

The basic idea here is to assume that a stock is a random distribution and use z-scores to set trade execution thresholds. The z-score is a useful statistic which indicates how many standard deviations an element is from the mean.  It can be calculated from the following formula:

Z = (X - μ)/σ

Where z is the z-score, X is the value of the element, μ is the population mean, and σ is the standard deviation. The z-score allows us to calulate the probability of the value X occuring in an normal distribution. If we have a Z-score of 2, that means we constrain the normal distribution by 2 standard deviations, and 95.4% of the data falls within those constraints. There is only a 4.6% chance that data will fall outside of those bounds.

<img src='https://i0.wp.com/i887.photobucket.com/albums/ac73/archaeopteryx1/bell-curve.jpg' height="300" >

By setting upper and lower z-score bounds over the rolling mean of a stock, I can build signals that a stock is over or undervalued. Combining this with intuition about the status of the company would give a solid quantitative and informed trading decision. Below you can see an example with Ford stock. A buy signal would be when the true price (dark blue) crosses under the red (lower z-bound), signalling undervaluation. The stock will revert to the mean, or get overvalued when it passes the upper blue bound, and be a sell signal. 

<img src='https://raw.githubusercontent.com/momonala/quantitative_finance/master/files/z_example.png' height="300">

## Current Progress 

I have performed an [exploratory analysis of stock data and tested the z-score idea.](bollingerbar_analysis.ipynb) The results look promising enough to continue developing the idea. There are a few factors to consider, outlined below. Additionally I did some k-means clustering analysis on the thresholds, and built a script to scrape quandl. 

I also played around with building a random stock price generator to create a large, realistic dataset for validation and testing. The advantage here is that we have labels for the volatility and mean drift of the stock, which will allow supervised learning later on. This also creates an unlimited amount of testing data. 

#### ensure you **pip install requirements.txt** before running the code! 

## Future Direction

I plan to continue work in a few different directions: 

1) A simple visualization web tool built in Flask with a Pandas data structure backend. 

2) Work with Quantopian's open-sourced tools [Zipline](https://github.com/quantopian/zipline) and [Alphalens](https://github.com/quantopian/alphalens) to validate and quantitatively analyze model perfomance. 

### References and Further Reading 

[Quantopian Lectures](https://www.quantopian.com/lectures)