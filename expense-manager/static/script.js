let isLoggedIn = false;
let chart = null;


// 🔐 REGISTER
async function register() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    await fetch("/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password })
    });

    alert("Registered successfully!");
}


// 🔐 LOGIN
async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch("/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (data.message === "success") {
        alert("Login successful");
        isLoggedIn = true;
        loadExpenses();
    } else {
        alert("Invalid login");
    }
}


// ➕ ADD EXPENSE
async function addExpense() {

    if (!isLoggedIn) {
        alert("⚠️ Please login first!");
        return;
    }

    const amount = document.getElementById("amount").value;
    const category = document.getElementById("category").value;
    const date = document.getElementById("date").value;
    const note = document.getElementById("note").value;

    if (!amount || !category || !date) {
        alert("Fill all required fields");
        return;
    }

    const res = await fetch("/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ amount, category, date, note })
    });

    const data = await res.json();

    if (data.error) {
        alert("⚠️ You are not logged in!");
        return;
    }

    // clear inputs
    document.getElementById("amount").value = "";
    document.getElementById("category").value = "";
    document.getElementById("date").value = "";
    document.getElementById("note").value = "";

    loadExpenses();
}


// 📋 LOAD + TOTAL + BUDGET + CHART
async function loadExpenses() {

    const res = await fetch("/get");
    const data = await res.json();

    const list = document.getElementById("list");
    list.innerHTML = "";

    let total = 0;
    let categoryMap = {};

    data.forEach(exp => {
        total += Number(exp.amount);

        // group by category
        if (!categoryMap[exp.category]) {
            categoryMap[exp.category] = 0;
        }
        categoryMap[exp.category] += Number(exp.amount);

        const li = document.createElement("li");
        li.innerHTML = `
            ₹ ${exp.amount} - ${exp.category} (${exp.date})
            <button onclick="deleteExpense(${exp.id})">❌</button>
        `;
        list.appendChild(li);
    });

    document.getElementById("total").innerText = "Total: ₹ " + total;

    // 💰 Budget alert
    const budget = Number(document.getElementById("budget").value);
    if (budget && total > budget) {
        alert("⚠️ Budget exceeded!");
    }

    // 📊 CHART LOGIC
    const labels = Object.keys(categoryMap);
    const values = Object.values(categoryMap);

    const ctx = document.getElementById("myChart").getContext("2d");

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "Expenses",
                data: values
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}


// ❌ DELETE
async function deleteExpense(id) {
    await fetch(`/delete/${id}`, { method: "DELETE" });
    loadExpenses();
}


// 🚫 Don't auto-load before login
// loadExpenses();