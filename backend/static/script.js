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

            document.getElementById("lr").innerText =
                "Linear Regression Prediction: ₹ " + data.linear_prediction;

            document.getElementById("lstm").innerText =
                "LSTM Prediction: ₹ " + data.lstm_prediction;
        })
        .catch(err => {
            alert("Error fetching prediction");
            console.log(err);
        });
}
