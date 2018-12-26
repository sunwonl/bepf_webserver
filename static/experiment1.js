var layout = {
    height: 900,
    hovermode: 'closest',
    clickmode: "event+select",
    //clickselectmode: "single",
    dragmode: false,
    yaxis: {
        title: "X2",
        fixedrange: true,
        range: [0, 100]
    },
    xaxis: {
        title: "X1",
        fixedrange: true,
        range: [0, 100]
    }
};
var config = {
    displayModeBar: false,
    responsive: false
};


function getData() {
    let arrayX = [];
    let arrayY = [];
    let interceptX;
    let interceptY;
    //(interceptY * x) + (interceptX * y) = interceptX * interceptY
    //y = (interceptX * interceptY - (interceptY * x)) / interceptX

    if (Math.random() >= 0.5) {
        interceptX = Math.floor(Math.random() * (100 - 50 + 1)) + 50;
        interceptY = Math.floor(Math.random() * (100 - 10 + 1)) + 10;
    } else {
        interceptX = Math.floor(Math.random() * (100 - 10 + 1)) + 10;
        interceptY = Math.floor(Math.random() * (100 - 50 + 1)) + 50;
    }
    for (let x = 0; x <= interceptX; x += 0.1) {
        arrayX.push(x.toFixed(1));
        arrayY.push(((interceptX * interceptY - (interceptY * x)) / interceptX).toFixed(1));
    }


    let trace1 = {
        x: arrayX,
        y: arrayY,
        type: 'scatter'
    };

    let data = [trace1];
    return data;
}

const plotly = Plotly.newPlot('myDiv', getData(), layout, config);
var myPlot = document.getElementById('myDiv');
var x_value = document.getElementById("x_value");
var y_value = document.getElementById("y_value");

myPlot.on('plotly_click', function (data) {
    var pts = '';
    for (var i = 0; i < data.points.length; i++) {
        pts = 'x=' + data.points[i].x.toFixed(2) + '\ny=' +
            data.points[i].y.toFixed(2) + '\n\n';
        x_value.value = data.points[i].x.toFixed(2);
        y_value.value = data.points[i].y.toFixed(2);
    }
    //alert('Closest point clicked:\n\n' + pts);
    logEmit();
    console.log('plotly_click:\n\n' + pts);
});


// click log making

var email = document.getElementById('email').value;
var round = document.getElementById("round").value;

var clickLog = [{'email':email, 'round':round, 'ts':Date.now(), 'x':-1, 'y':-1}];

// myPlot.addEventListener('click', function(event) {
//
// });

function logEmit() {
    var curTS = Date.now();
    var x = x_value.value;
    var y = y_value.value;

    var log;
    log = {'email': email, 'round':round, 'ts':curTS, 'x': parseFloat(x), 'y': parseFloat(y)};

    clickLog.push(log);
    console.log(log)
}

console.log('start rount #'+round)

// submit current page

function submitResult() {
    if (clickLog.length == 1) {
        alert("선택하지 않았습니다. 그래프 위의 점을 선택해주세요.");
        return
    }
    var frm = document.getElementById("expResult");
    var result = document.getElementById("clicklogs");

    if (confirm("제출하시겠습니까?")) {
        clickLog.push({'email':email, 'round':round, 'ts':Date.now(), 'x':-2, 'y':-2})
        result.value = JSON.stringify(clickLog);
        frm.submit()
    } else {
        console.log('cancel');
    }

}