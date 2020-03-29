# API Guidelines:

### API access:
Example POST body for /getData:
```
{
	"ticker": "AAPL"
}
```

Returns: 
```
{
  "Current Price": 289.0299987792969,
  "Display?": false,
  "Drawdown % ": -1,
  "Open Price": -1,
  "Previous Close Price": 287.61,
  "Symbol": "AAPL"
}
```

Example POST body for /getCharting:
```
{
  "ticker": "AAPL
}
```
Returns:
```
{
  "12:15:00-04:00": 276.56,
  "12:16:00-04:00": 276.66,
  "12:17:00-04:00": 276.41,
  "12:18:00-04:00": 275.65,
  "12:19:00-04:00": 275.32,
  "12:20:00-04:00": 275.05,
  "12:21:00-04:00": 275.77,
  "12:22:00-04:00": 276.13,
  "12:23:00-04:00": 275.7,
  "12:24:00-04:00": 274.81,
  "12:25:00-04:00": 274.76,
  "12:26:00-04:00": 274.03,
  "12:27:00-04:00": 274.25
}
```

GET call to /getOpens: {NOTE: NOT YET INTEGRATED INTO APP: SEE SECTION: Left to do.}
```
Creates a csv file containing all the open prices of each stock in stock_pool.csv in the form of

ticker	open
JCP	0.45
AAP	87.33
JNJ	118.91

Should be ran once in the morning at 9:30am EST [potentially by a chron job]
```
#### API setup:

1. Install dependencies:
```pip install -r requirements.txt```

2. Run server on local machine:
```python server.py``` (runs on localhost:3000)


### Python setup:

On a Mac, ensure that xcode is installed.

Install Python 3 from [here](https://www.anaconda.com/distribution/).




#### React App:
App.js renders 'Tickers'
'Tickers' maps all stocks in stock_pool.csv into a 'TickerData' component
'TickerData' uses POST /getCharting to get all needed data 
  'TickerData' renders 'Chart' 


#### Left to do:
1. Change app and getCharting to use the opens.csv file
2. Create an interval for 'Chart' to update every 5-10 seconds.
3. Recalculate drawdown for all every 40 - 60 seconds to determine which stocks to display
BONUS. At the next refresh (to do #3), keep all prior display = 'true' stocks and provide a button to delete stocks until the next refresh (to do #3).


WD

in app:
every min, call /getAll GET in App

remove no-chart tickers. 