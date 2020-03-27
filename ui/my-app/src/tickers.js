import React from 'react';
import {
  Card, CardImg, CardText, CardBody,
  CardTitle, CardSubtitle, Button
} from 'reactstrap';
import TestChart from './testchart';
import './stockCard.css';
import Chart from './chart';
import axios from 'axios';


const TickerData = ({ ticker }) => {
  const [loading, changeLoading] = React.useState(true);
  const [data, changeData] = React.useState(null);
  const [care, changeCare] = React.useState(true);


  React.useEffect(() => {
    async function getData() {
      try {
        const response = await fetch('http://localhost:5000/getCharting',
          { method: 'POST', body: JSON.stringify({ 'ticker': ticker }), headers: { "Content-Type": "application/json"}}
        ); 
        const dat = await response.json();
        changeData(dat);
        console.log(dat);
        changeLoading(false);
        if (String(dat.ending['Display?']) != 'true')  {
          changeCare(false);
        }
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
// console.log(pricing);
if  (care) {
  return (
    <div className='card mx-4'>
      <Chart charting={data} />
      <p className = 'text-center'>Open Price: {data.ending['open_price']}   </p>
      <p className='text-center'>Previous Close Price: {data.ending['prev_close']}</p>
    </div>
  );
}
return null;
}

//takes in array of tickers
const Tickers = ({ tickers }) => {
  // const ask = (care) => {
  //   // return true if care
  // }


  return (
    
    <div className="d-flex flex-wrap">
      {tickers.map((ticker, i) => {

          return (
            <TickerData ticker={ticker} />
          );
        // }
      })}
    </div>
  )
}

export default Tickers;