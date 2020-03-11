import React from 'react';
import {
  Card, CardImg, CardText, CardBody,
  CardTitle, CardSubtitle, Button
} from 'reactstrap';
import TestChart from './testchart';
import './stockCard.css';

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
      <Card>
        <p>Loading...</p>
      </Card>

    )
  } 
console.log(data)
const show = data['Display?']
if (show) {
  return (
    <div>
      <div >

        {/* <TestChart value={data['Symbol']} /> */}
        <div>
          <Card>
            <CardImg top width="100%" alt="Card image cap" />
            <TestChart ticker={ticker} />
            <CardBody>
              <CardTitle>{data['Symbol']}</CardTitle>
              <CardSubtitle> % change: {data['percent change']}</CardSubtitle>
              <CardText>
                <ul>
                  <li>Current Price: {data['Current Price']}</li>
                  <li>Current Price: {data['Open Price']}</li>
                  <li>Current Price: {data['Previous Close Price']}</li>
                </ul>
              </CardText>
              <Button>Button</Button>
            </CardBody>
          </Card>
        </div>
      </div >
    </div>
  );
}
return null;
}

//takes in array of tickers
const Tickers = ({ tickers }) => {
  return (
    <div>
      {tickers.map((ticker, i) => {
        //console.log(ticker)
        return <TickerData ticker={ticker} key={i} />
      })}
    </div>
  )
}

export default Tickers;