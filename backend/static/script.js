let chart = null;

function getPrediction() {
    const symbol = document.getElementById("symbol").value.trim();

    if (!symbol) {
        alert("Enter a stock symbol");
        return;
    }

    fetch(`http://127.0.0.1:5000/predict/${symbol}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            document.getElementById("lr").innerText = "₹ " + data.linear_prediction;

            document.getElementById("lstm").innerText = "₹ " + data.lstm_prediction;

            drawChart(data.history, data.dates, data.linear_prediction, data.symbol);
        })
        .catch(err => {
            alert("Error fetching prediction");
            console.log(err);
        });
}

function drawChart(history, dates, prediction, symbol) {
    const labels = [...dates, "Predicted"];
    const prices = [...history, prediction];

    const ctx = document.getElementById("priceChart").getContext("2d");

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: symbol + " Closing Price Trend",
                data: prices,
                borderWidth: 2,
                fill: false,
                tension: 0.3,
                pointRadius: function(ctx) {
                    return ctx.dataIndex === prices.length - 1 ? 6 : 3;
                }
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Date"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Price"
                    }
                }
            }
        }
    });
}
