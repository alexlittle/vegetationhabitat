const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const photo = document.getElementById('photo');
const captureButton = document.getElementById('capture');
const photoForm = document.getElementById('ObservationForm');
const photoDataInput = document.getElementById('id_observation_image');
const context = canvas.getContext('2d');

let stream;

function getMediaStream(facingMode) {
    if (facingMode === 'default'){
        return navigator.mediaDevices.getUserMedia({
        video: true
    });
    } else {
    return navigator.mediaDevices.getUserMedia({
        video: { facingMode: facingMode }
    });
    }
}

// Attempt to access the camera with the desired facingMode
function startCamera(facingMode) {
    getMediaStream(facingMode)
        .then(function(cameraStream) {
            // If successful, display the stream in the video element
            stream = cameraStream;
            video.srcObject = stream;
            video.style.display = "block";
            photo.style.display = "none";
            captureButton.textContent = "Capture";
        })
        .catch(function(error) {
            console.error(`Failed to access ${facingMode} camera:`, error);

            // If the requested facingMode is not available, try the other camera or fall back to default
            if (facingMode === 'environment') {
                console.log("Falling back to front camera (user).");
                startCamera('user'); // Try front camera
            } else if (facingMode === 'default') {
                startCamera('default');
                console.log("Both front and back cameras are unavailable.");
                document.getElementById('error-message').style.display = 'block'; // Show error message
            }
        });
}

// Request access to the camera
startCamera('environment');

// Capture the image and store it in the hidden form field
captureButton.addEventListener('click', () => {
    if (captureButton.textContent === "Capture") {
        // Capture the image
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert canvas to Base64 image
        const photoData = canvas.toDataURL('image/png');
        photoDataInput.value = photoData;

        // Replace webcam view with the captured photo
        photo.src = photoData;
        photo.style.display = "block";
        video.style.display = "none";

        // Update button to retry
        captureButton.textContent = "Try Again";

    } else {
        // Retry logic
        photoDataInput.value = '';
        startCamera('environment');

    }
});

// Function to prefill the image if base64 is already present in the input field
function prefillImage() {
    const base64Image = photoDataInput.value;
    if (base64Image) {
        // If base64 image exists in the input field, display it
        photo.src = base64Image;
        photo.style.display = "block";  // Show the captured photo
        video.style.display = "none";   // Hide the video
        captureButton.textContent = "Try Again"; // Button text for retry
    } else {
        // If no image is present, continue with camera
        photo.style.display = "none";
        video.style.display = "block";
        captureButton.textContent = "Capture"; // Button text for capture
    }
}

// Call prefillImage when the page loads (e.g., in case the form is re-rendered with a base64 image in the input)
document.addEventListener('DOMContentLoaded', function() {
    prefillImage();
});