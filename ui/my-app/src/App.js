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

console.log(SAMPLE_DATA.stocks);


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
    let stockCards = this.state.stocks.map((eachStock) => {
      console.log(eachStock);
      return <StockCard value={eachStock}/>;
    });
    return (
      <div>
        <div className="stock-cards">
          {stockCards}
        </div>
        
        {/*to start off put table here*/}        
      </div>
    );
    // return(
    //   <Tickers tickers = {['AAPL', 'MSFT']}/>
    // )
  }
}


class TestChart extends Component {
  render() {
    let coordinates = [];
    for(let index in this.props.value.price) {
      let point = {x: this.props.value.time[index], y: this.props.value.price[index]};
      coordinates.push(point);
    }
    console.log(coordinates);
    if(this.props.value !== undefined) {
      const options = {
        title: {text: this.props.value.ticker},
        theme: "light2",
        axisY: {
          title: "Price",
          includeZero: false,
          prefix: "$"
        },
        axisX: {
          title: "Time",
          interval: 5 //will need to implement conversion function
        },
        data: [
          {
            type: "line",
            dataPoints: coordinates
          }
        ],   
        animationEnabled: true,  
      };
      return(
        <div >
          <CanvasJSChart options={options} />
        </div>
      );
    } else {
      return null;
    }
    
  }
}

class StockCard extends Component {  
  render() {
    return (
      <div >
        
        <Card>
          <TestChart value={this.props.value} />
        
          <CardBody>
            <CardText>{this.props.value}</CardText>
            <Button>Button</Button>
          </CardBody>

        </Card>
      </div > 
    );
  }
}

export default App;
