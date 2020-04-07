import React, { Component } from 'react';
import CanvasJSReact from './canvasjs.react';
const CanvasJS = CanvasJSReact.CanvasJS;
const CanvasJSChart = CanvasJSReact.CanvasJSChart;
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

export default TestChart