// script.js - JavaScript for Cloud Security Config Checker

document.addEventListener("DOMContentLoaded", () => {
    const scanButton = document.getElementById("scan-button");
    const resultsSection = document.getElementById("results-section");
    const resultsContainer = document.getElementById("results-container");

    // Function to fetch scan results
    async function fetchScanResults() {
        try {
            // Show loading text
            resultsContainer.innerHTML = "<p>Scanning... Please wait.</p>";

            // Make API call to the backend
            const response = await fetch("http://127.0.0.1:5000/scan/s3");
            const data = await response.json();

            // Clear the container
            resultsContainer.innerHTML = "";

            if (data.length === 0) {
                resultsContainer.innerHTML = "<p>No issues found! Your cloud setup looks secure. 🎉</p>";
            } else {
                // Display results
                data.forEach((issue, index) => {
                    const issueElement = document.createElement("div");
                    issueElement.classList.add("issue-item");

                    issueElement.innerHTML = `
                        <h3>Issue ${index + 1}</h3>
                        <p><strong>Bucket:</strong> ${issue.bucket}</p>
                        <p><strong>Issue:</strong> ${issue.issue}</p>
                        <p><strong>Severity:</strong> ${issue.severity}</p>
                    `;

                    resultsContainer.appendChild(issueElement);
                });
            }
        } catch (error) {
            resultsContainer.innerHTML = `<p>Error fetching results: ${error.message}</p>`;
        }
    }

    // Event listener for scan button
    scanButton.addEventListener("click", () => {
        resultsSection.classList.remove("hidden");
        fetchScanResults();
    });
});
