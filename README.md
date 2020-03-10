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
#### API setup:

1. Install dependencies:
```pip install -r requirements.txt```

2. Run server on local machine:
```python server.py``` (runs on localhost:3000)


### Python setup:

On a Mac, ensure that xcode is installed.

Install Python 3 from [here](https://www.anaconda.com/distribution/).