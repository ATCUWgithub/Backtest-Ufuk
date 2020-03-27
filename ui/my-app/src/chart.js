import React, { Component } from 'react';
import CanvasJSReact from './canvasjs.react';
// import {
// 	Card, CardImg, CardText, CardBody,
// 	CardTitle, CardSubtitle, Button
// } from 'reactstrap';
// import { createChart } from 'lightweight-charts';


const CanvasJSChart = CanvasJSReact.CanvasJSChart;
export default ({charting}) => {

	let options = {
		animationEnabled: true,
		exportEnabled: true,
		theme: "light2", // "light1", "dark1", "dark2"
		title:{
			text: charting.ending.symbol
		},
		axisY: {
			title: "Price",
			includeZero: false,
			//suffix: "%"
		},
		axisX: {
			title: "Time",
			//prefix: "W",
			//interval: 2
		},
		data: [{
			type: "line",
			toolTipContent: "{x}: {y}",
			dataPoints: charting.total.map((val, i) => {
				return {'x': i, 'y': val}
			}),
		}]
	}

	// if (care) {
	return (
		<div >
			<CanvasJSChart options={options} />
			{/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
			<div>
				<p>Current Drawdown: {charting.ending.drawdown.toFixed(3)}</p>
				<p>Current Price: {charting.ending.current_price.toFixed(3)}</p>
			</div>
		</div>
	);

	// return null;

}
