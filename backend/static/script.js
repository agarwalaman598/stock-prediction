let chartInstance = null;

// Handle suggestions as user types
const tickerInput = document.getElementById("tickerInput");
const suggestionsBox = document.getElementById("suggestions");

tickerInput.addEventListener("input", async function() {
    const query = this.value.trim();
    if (query.length < 2) {
        suggestionsBox.style.display = "none";
        return;
    }

    try {
        const res = await fetch(`/search?q=${query}`);
        const data = await res.json();

        suggestionsBox.innerHTML = "";
        if (data.length > 0) {
            suggestionsBox.style.display = "block";
            data.forEach(item => {
                const div = document.createElement("div");
                div.className = "suggestion-item";
                div.innerText = `${item.symbol} - ${item.name}`;
                div.onclick = () => {
                    tickerInput.value = item.symbol;
                    suggestionsBox.style.display = "none";
                    getPrediction();
                };
                suggestionsBox.appendChild(div);
            });
        } else {
            suggestionsBox.style.display = "none";
        }
    } catch (err) {
        console.error("Search error:", err);
    }
});

// Hide suggestions if clicking outside
document.addEventListener("click", function(e) {
    if (!tickerInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
        suggestionsBox.style.display = "none";
    }
});

async function getPrediction() {
    const symbol = tickerInput.value.toUpperCase();
    if (!symbol) return;

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("result").classList.add("hidden");
    document.getElementById("error").classList.add("hidden");

    try {
        const response = await fetch(`/predict/${symbol}`);
        const data = await response.json();

        if (data.error) {
            document.getElementById("error").innerText = data.error;
            document.getElementById("error").classList.remove("hidden");
        } else {
            // Update Text
            document.getElementById("stockTitle").innerText = `${data.symbol} Prediction`;
            document.getElementById("lrValue").innerText = `${data.currency} ${data.linear_prediction}`;
            document.getElementById("lstmValue").innerText = `${data.currency} ${data.lstm_prediction}`;
            
            // Render Chart
            renderChart(data.dates, data.history, data.linear_prediction, data.lstm_prediction);
            
            document.getElementById("result").classList.remove("hidden");
        }
    } catch (err) {
        document.getElementById("error").innerText = "Failed to fetch prediction.";
        document.getElementById("error").classList.remove("hidden");
    } finally {
        document.getElementById("loading").classList.add("hidden");
    }
}

function renderChart(dates, history, lrPred, lstmPred) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    
    if (chartInstance) {
        chartInstance.destroy();
    }

    // Add future date for prediction
    const futureDate = "Tomorrow";
    const extendedLabels = [...dates, futureDate];

    // Create dataset with nulls for history so prediction stands out
    const historyData = [...history, null];
    
    // Prediction points (connect last history point to prediction)
    const lastPrice = history[history.length - 1];
    const lrData = new Array(history.length).fill(null);
    lrData[history.length - 1] = lastPrice;
    lrData.push(lrPred);

    const lstmData = new Array(history.length).fill(null);
    lstmData[history.length - 1] = lastPrice;
    lstmData.push(lstmPred);

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: extendedLabels,
            datasets: [
                {
                    label: 'History',
                    data: historyData,
                    borderColor: '#6c757d',
                    tension: 0.1
                },
                {
                    label: 'Linear Regression',
                    data: lrData,
                    borderColor: '#007bff',
                    borderDash: [5, 5],
                    pointRadius: 5
                },
                {
                    label: 'LSTM',
                    data: lstmData,
                    borderColor: '#28a745',
                    borderDash: [5, 5],
                    pointRadius: 5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // <--- Key fix for mobile
            interaction: {
                intersect: false,
                mode: 'index',
            },
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}