// Get DOM elements
const imageUpload = document.getElementById('image-upload');
const videoUpload = document.getElementById('video-upload');
const inputDisplay = document.getElementById('input-display');
const outputDisplay = document.getElementById('output-display');

// Handle image upload
imageUpload.addEventListener('change', (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      // Display the uploaded image
      inputDisplay.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image">`;

      // Send the image to the backend for processing
      processImage(file);
    };
    reader.readAsDataURL(file);
  }
});

// Handle video upload
videoUpload.addEventListener('change', (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      // Display the uploaded video
      inputDisplay.innerHTML = `<video controls src="${e.target.result}" alt="Uploaded Video"></video>`;

      // Send the video to the backend for processing
      processVideo(file);
    };
    reader.readAsDataURL(file);
  }
});

// Process image using the backend API
function processImage(file) {
  const formData = new FormData();
  formData.append('file', file);

  fetch('/process-image', {
    method: 'POST',
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      // Display the processed image
      outputDisplay.innerHTML = `<img src="${data.output_url}" alt="Processed Image">`;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// Process video using the backend API
function processVideo(file) {
  const formData = new FormData();
  formData.append('file', file);

  fetch('/process-video', {
    method: 'POST',
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      // Display the processed video
      outputDisplay.innerHTML = `<video controls src="${data.output_url}" alt="Processed Video"></video>`;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}