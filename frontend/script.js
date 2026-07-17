async function loadCount() {

    try {

        const response = await fetch("http://127.0.0.1:8000/student-count");

        const data = await response.json();

        // Update dashboard
        document.getElementById("count").innerHTML = data.students;
        document.getElementById("attendance").innerHTML = data.attendance + "%";
        document.getElementById("empty").innerHTML = data.empty_seats;
        document.getElementById("status").innerHTML = data.status;

    } catch (error) {

        console.log(error);

        document.getElementById("count").innerHTML = "--";
        document.getElementById("attendance").innerHTML = "--";
        document.getElementById("empty").innerHTML = "--";
        document.getElementById("status").innerHTML = "Camera Error";

    }

}

// Load immediately
loadCount();

// Refresh every second
setInterval(loadCount, 1000);


// -----------------------------
// Live Date & Time
// -----------------------------
function updateDateTime() {

    const now = new Date();

    document.getElementById("datetime").innerHTML =
        now.toLocaleString();

}

updateDateTime();

setInterval(updateDateTime, 1000);