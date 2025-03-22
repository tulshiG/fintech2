document.addEventListener("DOMContentLoaded", function() {
    const ctx = document.getElementById("creditScoreChart").getContext("2d");
    
    const creditScore = 806; // Example Score
    
    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Credit Score"],
            datasets: [{
                data: [creditScore, 900 - creditScore],
                backgroundColor: ["#2ecc71", "#dcdcdc"], // Green for score, gray for remaining
                borderWidth: 0
            }]
        },
        options: {
            cutout: "75%",
            plugins: {
                tooltip: { enabled: false },
                legend: { display: false }
            }
        }
    });
});

function toggleAuthForms() {
    let loginForm = document.getElementById("loginForm");
    let signupForm = document.getElementById("signupForm");
    let modalTitle = document.getElementById("authModalLabel");
    let toggleButton = document.querySelector(".modal-footer button");

    if (loginForm.classList.contains("d-none")) {
        loginForm.classList.remove("d-none");
        signupForm.classList.add("d-none");
        modalTitle.innerText = "Login";
        toggleButton.innerText = "Switch to Sign Up";
    } else {
        loginForm.classList.add("d-none");
        signupForm.classList.remove("d-none");
        modalTitle.innerText = "Sign Up";
        toggleButton.innerText = "Switch to Login";
    }
}