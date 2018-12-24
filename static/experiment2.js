var layout = {
    height: "800px",
    dragmode: false,
    hovermode: "closest",
    clickmode: "event+select",
    margin: {
        l: 0,
        r: 0,
        b: 0,
        t: 0
    },
    scene: {
        camera: {
            eye: {
                x: 1.5,
                y: 1.5,
                z: 1.5
            }
        },
        xaxis: {
            title: "X1",
            type:'linear',
            nticks: 10,
            range: [0, 100]
        },
        yaxis: {
            title: "X2",
            type:'linear',
            nticks: 10,
            range: [0, 100]
        },
        zaxis: {
            title: "X3",
            type:'linear',
            nticks: 10,
            range: [0, 100]
        }
    }
};
var config = {
    displayModeBar: false,
    responsive: false
};



function getData() {
    let arrayX = [];
    let arrayY = [];
    let arrayZ = [];
    let interceptX;
    let interceptY;
    let interceptZ;

    //(interceptY * x) + (interceptX * y) = interceptX * interceptY
    //y = (interceptX * interceptY - (interceptY * x)) / interceptX

    if (Math.random() >= 0.66) {
        interceptX = Math.floor(Math.random() * (100 - 50 + 1)) + 50;
        interceptY = Math.floor(Math.random() * (100 - 10 + 1)) + 10;
        interceptZ = Math.floor(Math.random() * (100 - 10 + 1)) + 10;
    } else if (Math.random() >= 0.33) {
        interceptX = Math.floor(Math.random() * (100 - 10 + 1)) + 10;
        interceptY = Math.floor(Math.random() * (100 - 50 + 1)) + 50;
        interceptZ = Math.floor(Math.random() * (100 - 10 + 1)) + 10;
    } else {
        interceptX = Math.floor(Math.random() * (100 - 10 + 1)) + 10;
        interceptY = Math.floor(Math.random() * (100 - 10 + 1)) + 10;
        interceptZ = Math.floor(Math.random() * (100 - 50 + 1)) + 50;
    }

    for (let x = 0; x < interceptX; x += 1) {
        for (let y = 0; y < interceptY; y += 1) {
            for (let z = 0; z < interceptZ; z += 1) {
                let result = Number((x / interceptX).toFixed(2)) + Number((y / interceptY).toFixed(2)) + Number((z / interceptZ).toFixed(2));
                if (result > 0.98 && result < 1.02) {
                    arrayX.push(x);
                    arrayY.push(y);
                    arrayZ.push(z);
                }

            }
        }
    }



    let trace1 = {
        x: arrayX,
        y: arrayY,
        z: arrayZ,
        mode: 'markers',
        marker: {
            color: '#1f77b4',
            size: 1,
            symbol: 'circle',
            line: {
                color: 'rgb(0,0,0)',
                width: 0
            }
        },
        line: {
            color: '#1f77b4',
            width: 5
        },
        type: 'scatter3d'
    };

    let data = [trace1];
    return data;
}

const plotly = Plotly.newPlot('myDiv', getData(), layout, config);

var myPlot = document.getElementById('myDiv');
var x_value = document.getElementById("x_value");
var y_value = document.getElementById("y_value");
var z_value = document.getElementById("z_value");

myPlot.on('plotly_click', function (data) {
    var pts = '';
    for (var i = 0; i < data.points.length; i++) {
        pts = 'x=' + data.points[i].x.toFixed(2) + '\ny=' +
            data.points[i].y.toFixed(2) + '\nz= ' + data.points[i].z.toFixed(2) + '\n\n';
        x_value.value = data.points[i].x.toFixed(2);
        y_value.value = data.points[i].y.toFixed(2);
        z_value.value = data.points[i].z.toFixed(2);
    }
    //alert('Closest point clicked:\n\n' + pts);
    console.log('plotly_click:\n\n' + pts);
});

let isTouched = false;
myPlot.on('plotly_hover', function (data) {
    // do something;
    if (isTouched) {
        isTouched = false;
        var pts = '';
        for (var i = 0; i < data.points.length; i++) {
            pts = 'x=' + data.points[i].x.toFixed(2) + '\ny=' +
                data.points[i].y.toFixed(2) + '\nz= ' + data.points[i].z.toFixed(2) + '\n\n';
            x_value.value = data.points[i].x.toFixed(2);
            y_value.value = data.points[i].y.toFixed(2);
            z_value.value = data.points[i].z.toFixed(2);
        }
        console.log('plotly_hover:\n\n' + pts);
    }
});

myPlot.addEventListener('touchenter', (event) => PlotlyPage.touchHandler(event));
myPlot.addEventListener('touchleave', (event) => PlotlyPage.touchHandler(event));
myPlot.addEventListener('touchstart', (event) => touchHandler(event));
myPlot.addEventListener('touchmove', (event) => touchHandler(event));
myPlot.addEventListener('touchend', (event) => touchHandler(event));

function touchHandler(event) {
    //console.log(`touchHandler triggered for event ${event.type}`);
    var touches = event.changedTouches,
        first = touches[0],
        type = "";
    switch (event.type) {
        case "touchenter":
            type = "mouseover";
            break;
        case "touchleave":
            type = "mouseout";
            break;
        case "touchstart":
            type = "mousedown";
            isTouched = true;
            break;
        case "touchmove":
            type = "mousemove";
            break;
        case "touchend":
            type = "mouseup";
            break;
        default:
            return;
    }

    var opts = {
        bubbles: true,
        screenX: first.screenX,
        screenY: first.screenY,
        clientX: first.clientX,
        clientY: first.clientY,
    };

    var simulatedEvent = new MouseEvent(type, opts);

    first.target.dispatchEvent(simulatedEvent);
    event.preventDefault();
}