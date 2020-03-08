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

#### API setup:

1. Install dependencies:
```pip install -r requirements.txt```

2. Run server on local machine:
```python server.py``` (runs on localhost:3000)


### Python setup:

On a Mac, ensure that xcode is installed.

Install Python 3 from [here](https://www.anaconda.com/distribution/).