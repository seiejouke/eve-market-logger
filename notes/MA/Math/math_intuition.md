# 📊 Time Series Analysis Cheat Sheet

---

## 1. Simple Moving Average (MA)

**Explanation:**  
The average of the last \( N \) values in a time series. Used to smooth data and identify trend direction.

$$
MA_t = \frac{1}{N} \sum_{i=0}^{N-1} x_{t-i}
$$

Where:  
- \( MA_t \) = moving average at time \( t \)  
- \( N \) = window size  
- \( x_{t-i} \) = value at time \( t-i \)

---

## 2. Exponential Moving Average (EMA)

**Explanation:**  
A moving average that gives more weight to recent data, making it more responsive to new information.

$$
EMA_t = \alpha \cdot x_t + (1 - \alpha) \cdot EMA_{t-1}
$$

Where:  
- \( \alpha = \frac{2}{N+1} \) (smoothing factor)  
- \( x_t \) = current value  
- \( EMA_{t-1} \) = previous EMA value

---

## 3. Weighted Moving Average (WMA)

**Explanation:**  
Like MA, but each data point has a different weight, usually increasing for more recent values.

$$
WMA_t = \frac{\sum_{i=1}^{N} w_i x_{t-N+i}}{\sum_{i=1}^{N} w_i}
$$

Where:  
- \( w_i \) = weight for each value (higher for recent values)  
- \( x_{t-N+i} \) = value at time \( t-N+i \)

---

## 4. Rolling Volatility (Standard Deviation)

**Explanation:**  
Measures how much values deviate from the mean in a rolling window—used as a proxy for risk or price variability.

$$
\sigma_t = \sqrt{ \frac{1}{N} \sum_{i=0}^{N-1} (x_{t-i} - \mu)^2 }
$$

Where:  
- \( \mu \) = mean of the values in the window  
- \( N \) = window size

---

## 5. Volume Weighted Average Price (VWAP)

**Explanation:**  
The average price of an asset, weighted by volume. Used to see the average entry/exit price for a period.

$$
VWAP = \frac{ \sum_{i=1}^{N} Price_i \times Volume_i }{ \sum_{i=1}^{N} Volume_i }
$$

---

## 6. Moving Average Convergence Divergence (MACD)

**Explanation:**  
Shows the difference between a fast EMA and a slow EMA, highlighting trend changes and momentum.

$$
MACD = EMA_{\text{fast}} - EMA_{\text{slow}}
$$

- Signal line: 9-period EMA of MACD.

---

## 7. Relative Strength Index (RSI)

**Explanation:**  
A momentum oscillator measuring the speed and change of price movements. Ranges from 0 to 100.

$$
RS = \frac{\text{Average Gain}}{\text{Average Loss}}
$$

$$
RSI = 100 - \left( \frac{100}{1 + RS} \right)
$$

Typically calculated over 14 periods.

---

## 8. Stochastic Oscillator

**Explanation:**  
Shows the position of the close price relative to the high-low range over \( N \) periods. Used for overbought/oversold signals.

$$
\text{Stoch}_t = 100 \times \frac{ \text{Close}_t - \min(\text{Low}_N) }{ \max(\text{High}_N) - \min(\text{Low}_N) }
$$

---

## 9. Rate of Change (ROC)

**Explanation:**  
The percentage change between the current value and the value \( n \) periods ago. Measures momentum.

$$
ROC_t = 100 \times \frac{ \text{Close}_t - \text{Close}_{t-n} }{ \text{Close}_{t-n} }
$$

---

## 10. Z-score

**Explanation:**  
How many standard deviations a value is from the mean. Used to find anomalies or normalize data.

$$
Z = \frac{x - \mu}{\sigma}
$$

Where:  
- \( x \) = current value  
- \( \mu \) = mean  
- \( \sigma \) = standard deviation

---

## 11. Bollinger Bands

**Explanation:**  
Shows volatility bands above and below a moving average. Widely used for identifying overbought/oversold conditions.

**Formulas:**

- Middle Band:

$$
\text{Middle Band} = MA_n
$$

- Upper Band:

$$
\text{Upper Band} = MA_n + K \cdot \sigma_n
$$

- Lower Band:

$$
\text{Lower Band} = MA_n - K \cdot \sigma_n
$$

Where:  
- \( n \) = window size (usually 20)  
- \( K \) = number of standard deviations (usually 2)

---

## 12. Percentile Ranking

**Explanation:**  
The percentage of values in the dataset that are less than a specific value.

$$
\text{Percentile} = \frac{ \text{Number of values less than } x }{ \text{Total number of values} } \times 100
$$

---

## 13. On-Balance Volume (OBV)

**Explanation:**  
Cumulative total of volume that adds or subtracts the volume based on price change direction.

**Logic:**

- If today's close > yesterday's close:  
  $$ OBV_t = OBV_{t-1} + \text{Volume}_t $$
- If today's close < yesterday's close:  
  $$ OBV_t = OBV_{t-1} - \text{Volume}_t $$
- If today's close = yesterday's close:  
  $$ OBV_t = OBV_{t-1} $$

---

## 14. Average True Range (ATR)

**Explanation:**  
Measures market volatility by decomposing the entire range of price for that period.

**Formulas:**

- True Range (TR):

$$
TR_t = \max
\begin{cases}
\text{High}_t - \text{Low}_t \\
|\text{High}_t - \text{Close}_{t-1}| \\
|\text{Low}_t - \text{Close}_{t-1}| \\
\end{cases}
$$

- ATR:

$$
ATR = \text{Average}(TR) \text{ over } N \text{ periods}
$$

---

## 15. Sharpe Ratio

**Explanation:**  
Measures risk-adjusted return of an investment.

$$
\text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}
$$

Where:  
- \( R_p \) = portfolio return  
- \( R_f \) = risk-free rate  
- \( \sigma_p \) = standard deviation of portfolio return

---

## 16. Autocorrelation

**Explanation:**  
Measures the correlation of a time series with a lagged version of itself.

$$
\text{Autocorr}_k = \text{corr}(x_t, x_{t-k})
$$

Where:  
- \( k \) = lag

---
