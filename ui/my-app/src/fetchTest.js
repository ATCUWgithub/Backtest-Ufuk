let uri = 'http://127.0.0.1:5000/getData'
fetch("http://127.0.0.1:5000/getData", {
    method: "POST",
    mode: "cors",
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify({"ticker": "AAPL"})
}).then((res)=>res.json()).then((data) => console.log(data))
// let response = fetch(uri, {
//     method: 'POST', 
//     mode: 'no-cors',
//     headers: {
//         'Accept': 'application/json',
//         'Content-Type': 'application/json'
//     }, 
//     body: JSON.stringify({'ticker': 'AAPL'})
// }).then((data) => {
//     console.log(data);
// })
// .catch((err) => {
//     console.error(err);
// });