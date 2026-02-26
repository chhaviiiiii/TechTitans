function generateFeedback() {
    const outputSection = document.getElementById("outputSection");
    const outputText = document.getElementById("outputText");

    outputSection.classList.remove("d-none");

    outputText.innerHTML = `
        <div class="alert alert-info">
            🔍 Resume analyzed successfully!
        </div>

        <ul class="list-group">
            <li class="list-group-item">✅ Strong technical foundation</li>
            <li class="list-group-item">⚠ Add measurable achievements</li>
            <li class="list-group-item">📌 Improve project impact description</li>
        </ul>
    `;
}

function startInterview() {
    window.location.href = "../templates/interview.html";
}



// ================= VIDEO CAPTURE =================
if (document.getElementById("videoPreview")) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            document.getElementById("videoPreview").srcObject = stream;
        })
        .catch(err => {
            console.error("Camera access denied:", err);
        });
}

// ================= AUDIO RECORDING =================
let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.start();
            audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks);
                const audioURL = URL.createObjectURL(audioBlob);
                document.getElementById("audioPlayback").src = audioURL;
            });
        });
}

function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
    }
}

// ================= REPORTS =================
document.addEventListener("DOMContentLoaded", function () {

    const ctx = document.getElementById('performanceChart').getContext('2d');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Technical Skills', 'Communication', 'Confidence'],
            datasets: [{
                data: [85, 75, 70],
                backgroundColor: [
                    '#0dcaf0',
                    '#198754',
                    '#ffc107'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });

});