import React from 'react';

const TickerData = ({ ticker }) => {
  const [loading, changeLoading] = React.useState(true);
  const [data, changeData] = React.useState(null);

  React.useEffect(() => {
    async function getData() {
      try {
        const response = await fetch('http://localhost:5000/getData',
          { method: 'POST', body: JSON.stringify({ 'ticker': ticker }), headers: { "Content-Type": "application/json"}}
        ); 
        const data = await response.json();
        changeData(data);
        changeLoading(false);
      } catch(e) {
        console.error(e);
      }
    }
    getData();
  }, []);

  if (loading) {
    return (
      <div>
        <p>Loading...</p>
      </div>
    )
  } 
console.log(data)
  return (
    <div>
      <p>{data['Symbol']}</p>
      <ul>
        <li>
          {data['Current Price']}
        </li>
        <li>
          {data['Open Price']}
        </li>
        <li>
          {data['Previous Close Price']}
        </li>
        <li>
          {data['percent change']}
        </li>
      </ul>
    </div>
  );
}

//takes in array of tickers
const Tickers = ({ tickers }) => {
  return (
    <div>
      {tickers.map((ticker, i) => {
        return <TickerData ticker={ticker} key={i} />
      })}
    </div>
  )
}

export default Tickers;