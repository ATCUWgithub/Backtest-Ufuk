import React from 'react';
import {
  Card, CardImg, CardText, CardBody,
  CardTitle, CardSubtitle, Button
} from 'reactstrap';
import TestChart from './testchart';
import './stockCard.css';
import Chart from './chart';
import axios from 'axios';


const TickerData = ({ ticker, charting }) => {
//   const [loading, changeLoading] = React.useState(true);
//   const [data, changeData] = React.useState(null);


//   React.useEffect(() => {
//     async function getData() {
//       try {
//         const response = await fetch('http://localhost:5000/getCharting',
//           { method: 'POST', body: JSON.stringify({ 'ticker': ticker }), headers: { "Content-Type": "application/json"}}
//         ); 
//         const dat = await response.json();
//         changeData(dat);
//         changeLoading(false);
//       } catch(e) {
//         console.error(e);
//       }
//     }

//     getData();
//   }, []);

//   if (loading) {
//     return (
//       <Card>
//         <p>Loading...</p>
//       </Card>

//     )
//   } 
// console.log(pricing);
  return (
    <div className='card mx-4'>
      <Chart charting={charting} ticker={ticker.ticker}/>
      <p className = 'text-center'>Drawdown: {ticker.dd}   </p>
      <p className = 'text-center'>Open Price: {ticker.open}   </p>
    </div>
  );

}

//takes in array of tickers
const Tickers = () => {
  const [data, changeData] = React.useState(null);
  const [batch, changeBatch] = React.useState(null);
  const [loading, changeLoading] = React.useState(true);
  const [loading2, changeLoading2] = React.useState(true);

  React.useEffect(() => {
    async function getDDs(){
      try {
        const response = await fetch('http://localhost:5000/getAll',
          { method: 'GET', headers: { "Content-Type": "application/json" } }
        );
        const dat = await response.json();
        changeData(dat.disp);
        changeLoading(false);
      } catch (e) {
        console.error(e);
      }
    }
    async function getBatch() {
      try {
        const response = await fetch('http://localhost:5000/getBatch',
          { method: 'GET', headers: { "Content-Type": "application/json" } }
        );
        const dat = await response.json();
        changeBatch(dat.charts);
        changeLoading2(false);
        console.log(dat.charts)
      } catch (e) {
        console.error(e);
      }
    }
    getDDs();
    getBatch();

    // const interval = setInterval(() => {
    //   getDDs();
    // }, 30000);
    // return () => clearInterval(interval);
  }, []);
  // const ask = (care) => {
  //   // return true if care
  // }

  if (loading) {
    return (
      <Card>
        <p>Loading...</p>
      </Card>

    )
  } 
  if (loading2) {
    return (
      <Card>
        <p>Loading...</p>
      </Card>

    )
  } 


  return (
    <div className="d-flex flex-wrap">
      {data.map((ticker, i) => {
          const charting = batch[ticker.ticker]
          return (
            <TickerData ticker={ticker} charting={charting} />
          );
        // }
      })}
    </div>
  )
}

export default Tickers;