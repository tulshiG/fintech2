const API_URL = "http://127.0.0.1:8000";

// ✅ Function to decode JWT token
function decodeToken(token) {
    try {
        const base64Url = token.split('.')[1];  // Extract payload
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        return JSON.parse(atob(base64));  // Decode token
    } catch (error) {
        console.error("❌ Error decoding token:", error);
        return null;
    }
}

// ✅ Function to log in a user
async function loginUser() {
    const panNo = document.getElementById("loginPanNo").value;
    const password = document.getElementById("loginPassword").value;

    const formData = new URLSearchParams();
    formData.append("username", panNo);
    formData.append("password", password);

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        const data = await response.json();

        if (data.access_token) {
            console.log("✅ Login Successful. Storing Token...");
            localStorage.setItem("token", data.access_token);

            // ✅ Extract pan_no from JWT token
            const decodedToken = decodeToken(data.access_token);
            if (decodedToken && decodedToken.sub) {
                localStorage.setItem("pan_no", decodedToken.sub);
                console.log("✅ Extracted PAN:", decodedToken.sub);
                fetchCreditDetails(); // ✅ Fetch credit details after login
            } else {
                alert("❌ Failed to extract PAN number from token.");
            }
        } else {
            alert("❌ Login Failed. Please check credentials.");
        }
    } catch (error) {
        console.error("❌ Login Error:", error);
        alert("❌ Login request failed.");
    }
}

// ✅ Function to decode JWT token
function decodeToken(token) {
    try {
        const base64Url = token.split('.')[1];  
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        return JSON.parse(atob(base64));  
    } catch (error) {
        console.error("❌ Error decoding token:", error);
        return null;
    }
}

// ✅ Function to log in a user
async function loginUser() {
    const panNo = document.getElementById("loginPanNo").value;
    const password = document.getElementById("loginPassword").value;

    const formData = new URLSearchParams();
    formData.append("username", panNo);
    formData.append("password", password);

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        const data = await response.json();

        if (data.access_token) {
            console.log("✅ Login Successful. Storing Token...");
            localStorage.setItem("token", data.access_token);

            const decodedToken = decodeToken(data.access_token);
            if (decodedToken && decodedToken.sub) {
                localStorage.setItem("pan_no", decodedToken.sub);
                console.log("✅ Extracted PAN:", decodedToken.sub);
                fetchCreditDetails();
            } else {
                alert("❌ Failed to extract PAN number from token.");
            }
        } else {
            alert("❌ Login Failed. Please check credentials.");
        }
    } catch (error) {
        console.error("❌ Login Error:", error);
        alert("❌ Login request failed.");
    }
}

// ✅ Function to fetch credit details after login
async function fetchCreditDetails() {
    const panNo = localStorage.getItem("pan_no");
    const token = localStorage.getItem("token");

    if (!panNo || !token) {
        alert("❌ Missing credentials. Please log in again.");
        return;
    }

    console.log(`Fetching credit data for PAN: ${panNo}`);

    try {
        const [creditScoresRes, unifiedScoreRes, riskAssessmentRes] = await Promise.all([
            fetch(`${API_URL}/credit/bureaus/${panNo}`, { headers: { "Authorization": `Bearer ${token}` } }),
            fetch(`${API_URL}/credit/bureaus/unified/${panNo}`, { headers: { "Authorization": `Bearer ${token}` } }),
            fetch(`${API_URL}/credit/bureaus/risk/${panNo}`, { headers: { "Authorization": `Bearer ${token}` } })
        ]);

        if (!creditScoresRes.ok || !unifiedScoreRes.ok || !riskAssessmentRes.ok) {
            throw new Error("❌ Error fetching credit details.");
        }

        const creditScoresData = await creditScoresRes.json();
        const unifiedScoreData = await unifiedScoreRes.json();
        const riskAssessmentData = await riskAssessmentRes.json();

        document.getElementById("creditScores").innerText = JSON.stringify(creditScoresData.scores, null, 2);
        document.getElementById("unifiedScore").innerText = unifiedScoreData.unified_score || "N/A";
        document.getElementById("riskAssessment").innerText = riskAssessmentData.risk_assessment || "N/A";

        document.getElementById("creditDetails").style.display = "block";
    } catch (error) {
        console.error("❌ Error fetching credit details:", error);
        alert(error.message);
    }
}
