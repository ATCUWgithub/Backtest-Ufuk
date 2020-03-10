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
import SAMPLE_DATA from './stocks.json';


const CanvasJS = CanvasJSReact.CanvasJS;
const CanvasJSChart = CanvasJSReact.CanvasJSChart;
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stocks:[],
      response: {}
    };
  }
  
  componentDidMount() {
    this.setState({stocks: SAMPLE_DATA.stocks, response: SAMPLE_DATA.response});
  }

  render() {
    let stockCards = this.state.stocks.map((eachStock) => {
      console.log(eachStock);
      return <StockCard value={eachStock} response={this.state.response}/>;
    });
    return (
      <div>
        <div className="stock-cards">
          {stockCards}
        </div>
        
        {/*to start off put table here*/}        
      </div>
    );
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
              <CardText>{this.props.response}</CardText>
              <Button>Button</Button>
            </CardBody>

        </Card>
      </div > 
    );
  }
}

export default App;
