import React, { Component } from 'react';
import {
  Card, CardImg, CardText, CardBody,
  CardTitle, CardSubtitle, Button
} from 'reactstrap';
//import { createChart } from 'lightweight-charts';
import CanvasJSReact from './canvasjs.react';
import {ExampleChart} from './chart';
import './stockCard.css';
//import Clock from 'react-clock';
import Tickers from './tickers';
import SAMPLE_DATA from './stocks.json';
import io from 'socket.io-client';
import { getRoles } from '@testing-library/react';


const CanvasJS = CanvasJSReact.CanvasJS;
const CanvasJSChart = CanvasJSReact.CanvasJSChart;
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stocks:[],
      loading: true
    };
  }


  
  // async componentDidMount() {
  //   this.setState({stocks: SAMPLE_DATA.stocks});

  //   const url = 'http://localhost:5000/updateCurPrices';
  //   const response = await fetch(url, {
  //     mode: 'no-cors'
  //   });
  //   const data = response.json;
  //   this.state.loading = false;
  //   console.log('yay');
  // }




  render() {

    return(
      <div >
          <Tickers tickers={SAMPLE_DATA.stocks} />
        {console.log(SAMPLE_DATA.stocks)}
        </div>
    )
  }
}


export default App;
