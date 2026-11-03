/* EduForecaster XAI - Frontend Controller & UX Interactions */

let branchChartInstance = null;
let academicChartInstance = null;
let shapChartInstance = null;
let activeRecourseProfile = null;

// Initialize on page load
document.addEventListener("DOMContentLoaded", async () => {
    // If on main predictor page, auto-trigger canonical preset or preset from URL
    if (document.getElementById("student-form")) {
        const urlParams = new URLSearchParams(window.location.search);
        const sampleParam = urlParams.get("sample");
        if (sampleParam) {
            await loadPreset(sampleParam);
        } else {
            await loadPreset("at_risk");
        }

        const autoSubmit = urlParams.get("auto");
        if (autoSubmit) {
            setTimeout(async () => {
                await handleFormSubmit();
                const autoRecourse = urlParams.get("recourse");
                if (autoRecourse) {
                    setTimeout(() => {
                        applyCounterfactualRecourse();
                    }, 1200);
                }
            }, 500);
        }
    }

    // Initialize image lightbox for all figures across pages
    initImageLightbox();
});

async function loadPreset(presetType) {
    try {
        const response = await fetch(`/api/sample/${presetType}`);
        if (!response.ok) throw new Error("Failed to load preset");
        const data = await response.json();

        // Populate form fields with subtle transition
        for (const [key, value] of Object.entries(data)) {
            const el = document.getElementById(key);
            if (el) {
                el.value = value;
            }
        }
    } catch (err) {
        console.error("Error loading preset:", err);
    }
}

async function handleFormSubmit(event) {
    if (event && event.preventDefault) {
        event.preventDefault();
    }

    const form = document.getElementById("student-form");
    if (!form) return;

    const formData = new FormData(form);
    const payload = {};

    // Cast numbers properly
    formData.forEach((value, key) => {
        if (!isNaN(value) && value.trim() !== '') {
            payload[key] = Number(value);
        } else {
            payload[key] = value;
        }
    });

    // UI state transitions
    document.getElementById("empty-state").style.display = "none";
    document.getElementById("results-container").style.display = "none";
    document.getElementById("loading-spinner").style.display = "block";
    document.getElementById("submit-btn").disabled = true;

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || "Prediction request failed");
        }

        renderResults(result.data);
    } catch (err) {
        alert("Error generating prediction: " + err.message);
        console.error(err);
    } finally {
        document.getElementById("loading-spinner").style.display = "none";
        document.getElementById("submit-btn").disabled = false;
    }
}

function renderResults(data) {
    document.getElementById("results-container").style.display = "block";

    // 1. Executive Summary Banner
    const placementPred = data.stage3.placement_prediction;
    const placementProb = data.stage3.placement_probability * 100.0;
    const confidence = data.stage3.confidence;

    const badgeEl = document.getElementById("placement-badge");
    const badgeText = document.getElementById("placement-text");
    badgeText.textContent = placementPred;

    if (placementPred === "Placed") {
        badgeEl.className = "placement-badge placed";
    } else {
        badgeEl.className = "placement-badge not-placed";
    }

    const probBar = document.getElementById("prob-bar");
    probBar.style.width = `${Math.min(Math.max(placementProb, 5), 100)}%`;
    probBar.style.backgroundColor = placementPred === "Placed" ? "#10b981" : "#ef4444";

    document.getElementById("prob-val").textContent = `${placementProb.toFixed(1)}%`;
    document.getElementById("conf-val").textContent = `${confidence.toFixed(1)}%`;

    document.getElementById("preview-branch").textContent = data.stage1.recommended_branch;
    document.getElementById("preview-tier").textContent = data.stage2.forecasted_academic_tier;

    // Populate Cascading Stepper Flow
    const st1 = document.getElementById("stepper-stage1");
    if (st1) st1.textContent = data.stage1.recommended_branch;
    const st2 = document.getElementById("stepper-stage2");
    if (st2) st2.textContent = data.stage2.forecasted_academic_tier;
    const st3 = document.getElementById("stepper-stage3");
    if (st3) st3.textContent = `${placementPred} (${placementProb.toFixed(1)}%)`;

    // 2. Stage 1: Branch Recommendation
    document.getElementById("stage1-recommended").textContent = data.stage1.recommended_branch;
    renderBranchChart(data.stage1.probabilities);

    // 3. Stage 2: Academic Performance Forecast
    document.getElementById("stage2-tier").textContent = data.stage2.forecasted_academic_tier;
    renderAcademicChart(data.stage2.probabilities);

    // 4. SHAP Waterfall Attribution
    renderShapChart(data.shap_attribution);

    // 5. Actionable Counterfactual Recourse
    const baselineProb = (data.recourse.baseline_probability * 100.0).toFixed(1);
    const targetProb = (data.recourse.target_probability * 100.0).toFixed(1);

    document.getElementById("current-prob-stat").textContent = `${baselineProb}%`;
    document.getElementById("target-prob-stat").textContent = `${targetProb}%`;

    // Cache counterfactual profile for simulator
    activeRecourseProfile = data.recourse.counterfactual_profile || null;

    const tableBody = document.getElementById("recourse-table-body");
    tableBody.innerHTML = "";

    data.recourse.interventions.forEach(item => {
        const tr = document.createElement("tr");
        if (item.Modality === "Socio-Econ.") {
            tr.className = "text-muted";
        }
        tr.innerHTML = `
            <td><strong>${item['Feature Name']}</strong></td>
            <td><span class="badge ${item.Modality === 'Academic' ? 'badge-primary' : (item.Modality === 'Behavioral' ? 'badge-warning' : 'badge-info')}">${item.Modality}</span></td>
            <td><code>${item['Current Value']}</code></td>
            <td><strong class="text-success">${item['Counterfactual Target (x_i*)']}</strong></td>
            <td>${item['Actionable Recommendation']}</td>
        `;
        tableBody.appendChild(tr);
    });
}

function applyCounterfactualRecourse() {
    if (!activeRecourseProfile) {
        alert("No counterfactual targets available for simulation.");
        return;
    }

    // Update form input values smoothly
    for (const [key, val] of Object.entries(activeRecourseProfile)) {
        const el = document.getElementById(key);
        if (el) {
            el.value = val;
            el.style.transition = "all 0.3s ease";
            el.style.boxShadow = "0 0 0 3px rgba(16, 185, 129, 0.4)";
            el.style.borderColor = "#10b981";
            setTimeout(() => {
                el.style.boxShadow = "";
                el.style.borderColor = "";
            }, 2500);
        }
    }

    // Scroll to results top and re-run prediction
    const banner = document.getElementById("summary-banner");
    if (banner) {
        banner.scrollIntoView({ behavior: "smooth" });
    }

    // Submit form
    document.getElementById("student-form").dispatchEvent(new Event("submit"));
}

function renderBranchChart(probDict) {
    const ctx = document.getElementById("branchChart").getContext("2d");
    if (branchChartInstance) branchChartInstance.destroy();

    const labels = Object.keys(probDict).map(k => {
        return k.replace("Computer Science & Engineering", "CSE")
                .replace("Data Science & AI", "DSAI")
                .replace("Electronics & Communication", "ECE")
                .replace("Electrical & Electronics", "EEE")
                .replace("Mechanical Engineering", "ME")
                .replace("Information Technology", "IT");
    });
    const values = Object.values(probDict).map(v => (v * 100.0).toFixed(1));

    branchChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Probability (%)",
                data: values,
                backgroundColor: "#0ea5e9",
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, max: 100, grid: { color: "#f1f5f9" } },
                x: { grid: { display: false } }
            }
        }
    });
}

function renderAcademicChart(probDict) {
    const ctx = document.getElementById("academicChart").getContext("2d");
    if (academicChartInstance) academicChartInstance.destroy();

    const labels = Object.keys(probDict);
    const values = Object.values(probDict).map(v => (v * 100.0).toFixed(1));

    academicChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Probability (%)",
                data: values,
                backgroundColor: "#10b981",
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, max: 100, grid: { color: "#f1f5f9" } },
                x: { grid: { display: false } }
            }
        }
    });
}

function renderShapChart(shapRecords) {
    const ctx = document.getElementById("shapChart").getContext("2d");
    if (shapChartInstance) shapChartInstance.destroy();

    const labels = shapRecords.map(r => r.feature);
    const values = shapRecords.map(r => r.shap_value);
    const colors = values.map(v => v >= 0 ? "#10b981" : "#ef4444");

    shapChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "SHAP Impact (φ_j)",
                data: values,
                backgroundColor: colors,
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` SHAP Impact: ${context.parsed.x > 0 ? '+' : ''}${context.parsed.x.toFixed(4)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: "#f1f5f9" }
                },
                y: {
                    grid: { display: false }
                }
            }
        }
    });
}

/* Lightbox Modal for Zooming Benchmark Figures */
function initImageLightbox() {
    if (!document.getElementById("image-modal")) {
        const modal = document.createElement("div");
        modal.id = "image-modal";
        modal.className = "image-modal";
        modal.innerHTML = '<img class="modal-content-img" id="modal-img" alt="Zoomed Benchmark Plot">';
        modal.onclick = () => modal.classList.remove("active");
        document.body.appendChild(modal);
    }

    document.querySelectorAll(".figure-container img, .responsive-img").forEach(img => {
        img.style.cursor = "zoom-in";
        img.title = "Click to enlarge in high resolution";
        img.onclick = () => {
            const modal = document.getElementById("image-modal");
            const modalImg = document.getElementById("modal-img");
            modalImg.src = img.src;
            modal.classList.add("active");
        };
    });
}
