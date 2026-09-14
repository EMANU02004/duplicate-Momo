const API = "http://127.0.0.1:8000";

async function loadDashboard() {
  const [analyticsRes, txRes] = await Promise.all([
    fetch(`${API}/analytics`),
    fetch(`${API}/transactions?limit=100`)
  ]);
  const analytics = await analyticsRes.json();
  const transactions = await txRes.json();

  renderSummary(analytics);
  renderChart(analytics.by_category);
  renderTable(transactions);
}

function renderSummary(data) {
  const summary = document.getElementById("summary");
  summary.innerHTML = `
    <div class="card"><h3>Total Transactions</h3><p>${data.total}</p></div>
    <div class="card"><h3>Total Amount (RWF)</h3><p>${data.total_amount.toLocaleString()}</p></div>
    ${Object.entries(data.by_category).map(([cat, count]) =>
      `<div class="card"><h3>${cat.replace(/_/g, " ")}</h3><p>${count}</p></div>`
    ).join("")}
  `;
}

function renderChart(byCategory) {
  const ctx = document.getElementById("chart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: Object.keys(byCategory).map(k => k.replace(/_/g, " ")),
      datasets: [{
        label: "Transactions",
        data: Object.values(byCategory),
        backgroundColor: "#4e73df"
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
    }
  });
}

function renderTable(transactions) {
  const container = document.getElementById("table-container");
  container.innerHTML = `
    <table>
      <thead>
        <tr><th>Date</th><th>Category</th><th>Amount (RWF)</th><th>Address</th></tr>
      </thead>
      <tbody>
        ${transactions.map(t => `
          <tr>
            <td>${t.date}</td>
            <td>${t.category.replace(/_/g, " ")}</td>
            <td>${t.amount != null ? t.amount.toLocaleString() : "—"}</td>
            <td>${t.address}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}

loadDashboard();
