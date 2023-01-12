



function build_chart(data,element_id) {
    let labels = [];
    let y_data = [];

    for (var i in data) {
        labels.push(i);
        y_data.push(data[i]);
    }

    var element = document.getElementById(element_id);
    element.innerHTML = "";

    window.ApexCharts && (new ApexCharts(document.getElementById(element_id), {
        chart: {
            type: "line",
            fontFamily: 'inherit',
            height: 240,
            parentHeightOffset: 0,
            toolbar: {
                show: false,
            },
            animations: {
                enabled: false
            },
        },
        fill: {
            opacity: 1,
        },
        stroke: {
            width: 2,
            lineCap: "round",
            curve: "straight",
        },
        series: [{
            name: "page requests",
            data: y_data,
        }
        ],
        grid: {
            padding: {
                top: -20,
                right: 0,
                left: -4,
                bottom: -4
            },
            strokeDashArray: 4,
        },
        xaxis: {
            labels: {
                padding: 0,
            },
            tooltip: {
                enabled: false
            }
        },
        yaxis: {
            labels: {
                padding: 4
            },
        },
        labels: labels,
        colors: ["#fab005", "#5eba00", "#206bc4"],
        legend: {
            show: true,
            position: 'bottom',
            offsetY: 12,
            markers: {
                width: 10,
                height: 10,
                radius: 100,
            },
            itemMargin: {
                horizontal: 8,
                vertical: 8
            },
        },
    })).render();
}

