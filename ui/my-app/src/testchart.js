import React, { Component } from 'react';
import CanvasJSReact from './canvasjs.react';
const CanvasJS = CanvasJSReact.CanvasJS;
const CanvasJSChart = CanvasJSReact.CanvasJSChart;
class TestChart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null
    };
  }

  componentDidMount() {
    fetch('http://localhost:5000/getCharting',
          { method: 'POST', 
          body: JSON.stringify({ 'ticker': this.props.ticker }), 
          headers: { "Content-Type": "application/json"}
          })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        //console.log(data);
        this.setState({data: data});
      })
  }

  getDate = () => {
    let today = new Date();
    let dd = String(today.getDate()).padStart(2, '0');
    let mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    let yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    return today;
  }
  render() {
    if(this.state.data) {

      let coordinates = [];
      let times = Object.keys(this.state.data);
      let dateObjArray = times.map((time) => {
        let format = this.getDate() + 'T' + time.slice(0,8) +'.000' + time.slice(8);
        return new Date(format);
      });
      let prices = Object.values(this.state.data);
      console.log(prices);
      for(let index in dateObjArray) {
        console.log(index);
        console.log(prices[index]);
        let point = {x: dateObjArray[index], y: prices[index]};
        coordinates.push(point);
      }
      console.log(coordinates);
    
      const options = {
        title: {text: this.props.ticker},
        theme: "light2",
        axisY: {
          title: "Price",
          includeZero: false,
          prefix: "$"
        },
        axisX: {
          title: "Time",
          valueFormatString: 'h:mm:ss',
          //interval: 5, //will need to implement conversion function
          // labelFormatter: function (e) {
          //   return CanvasJS.formatDate( e.value, 'h:mm:ss');
          // },
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
    
    }
    return null;
    
  }
}

export default TestChart