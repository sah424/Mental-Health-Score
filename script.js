// FastAPI backend URL
const API_URL = "https://mental-health-score-edtm.onrender.com";


// Get elements from HTML
const form = document.getElementById("predictionForm");

const button = document.getElementById("predictButton");

const errorMessage = document.getElementById("errorMessage");

const resultCard = document.getElementById("resultCard");

const score = document.getElementById("score");


// Run this code when the form is submitted
form.addEventListener("submit", async function (event) {

    // Prevent page refresh
    event.preventDefault();


    // Hide old error message
    errorMessage.style.display = "none";


    // Hide previous result
    resultCard.style.display = "none";


    // Show loading animation
    button.disabled = true;
    button.classList.add("loading");


    // Collect data from form
    const studentData = {

        age: Number(document.getElementById("age").value),

        gender: document.getElementById("gender").value,

        country: document.getElementById("country").value,

        academic_level:
            document.getElementById("academicLevel").value,

        most_used_platform:
            document.getElementById("platform").value,

        purpose_of_use:
            document.getElementById("purpose").value,

        avg_daily_usage_hours:
            Number(document.getElementById("usageHours").value),

        daily_unlocks:
            Number(document.getElementById("dailyUnlocks").value),

        study_hours:
            Number(document.getElementById("studyHours").value),

        physical_activity_hours:
            Number(document.getElementById("physicalActivity").value),

        sleep_hours_per_night:
            Number(document.getElementById("sleepHours").value),

        stress_level:
            document.getElementById("stressLevel").value
    };


    try {

        // Send data to FastAPI
        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(studentData)
        });


        // Check if API returned an error
        if (!response.ok) {

            const errorData = await response.json();

            throw new Error(getErrorMessage(errorData));
        }


        // Convert response into JavaScript object
        const data = await response.json();


        // Display prediction
        score.textContent =
            Number(data.predicted_mental_health_score).toFixed(2);


        // Show result card
        resultCard.style.display = "block";


        // Scroll to result
        resultCard.scrollIntoView({
            behavior: "smooth"
        });

    }


    catch (error) {

        // Show error message
        errorMessage.textContent =
            error.message || "Something went wrong. Please try again.";

        errorMessage.style.display = "block";
    }


    finally {

        // Stop loading animation
        button.disabled = false;

        button.classList.remove("loading");
    }

});


// Convert FastAPI validation errors into readable text
function getErrorMessage(errorData) {

    // FastAPI validation error
    if (Array.isArray(errorData.detail)) {

        return errorData.detail
            .map(error => {

                const field = error.loc[error.loc.length - 1];

                return `${field}: ${error.msg}`;

            })
            .join(" | ");
    }


    // Normal API error
    if (typeof errorData.detail === "string") {

        return errorData.detail;
    }


    return "Invalid input. Please check your information.";
}
