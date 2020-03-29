import React, { Component } from 'react';
import CanvasJSReact from './canvasjs.react';
import { Card } from 'reactstrap';
// import {
// 	Card, CardImg, CardText, CardBody,
// 	CardTitle, CardSubtitle, Button
// } from 'reactstrap';
// import { createChart } from 'lightweight-charts';


const CanvasJSChart = CanvasJSReact.CanvasJSChart;
export default ({charting, ticker}) => {
	const [data, changeData] = React.useState(null);
	const [loading, changeLoading] = React.useState(true);

	React.useEffect(() => {
		async function getSups() {
			try {
				const response = await fetch('http://localhost:5000/getSupport',
					{ method: 'POST', body: JSON.stringify({ 'ticker': ticker }), headers: { "Content-Type": "application/json" } }
				);
				const dat = await response.json();
				changeData(dat);
				changeLoading(false);
			} catch (e) {
				console.error(e);
			}
		}
		getSups()
	}, []);

	let options = {
		animationEnabled: true,
		exportEnabled: true,
		theme: "light2", // "light1", "dark1", "dark2"
		title:{
			text: ticker
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
			xValueType: "dateTime",
			dataPoints: charting.map((val, i) => {
				return {'x': val.time, 'y': val.value}
			}),
		}]
	}
	if (loading) {
		return(
			<div>
					<p>Loading...</p>
			</div>
		)
	}

	// if (care) {
	return (
		<div >
			<CanvasJSChart options={options} />
			{/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
			<p className='text-center'>Current Price: {data.current}   </p>
			<p className='text-center'>Previous Day Close: {data.lastClose}   </p>

		</div>
	);

	// return null;

}
