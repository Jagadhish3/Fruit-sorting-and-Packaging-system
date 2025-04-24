const imageUpload = document.getElementById('imageUpload');
const imagePreview = document.getElementById('imagePreview');
const predictButton = document.getElementById('predictButton');
const resultText = document.getElementById('resultText');
const loader = document.getElementById('loader');
const resetButton = document.getElementById('resetButton');
const uploadMessage = document.getElementById('uploadMessage');
const fruitCountsText = document.getElementById('fruitCountsText');
const predictAnotherButton = document.getElementById('predictAnotherButton');

const classLabels = [
    'apple fruit', 'banana fruit', 'cherry fruit', 'chickoo fruit', 'grapes fruit',
    'kiwi fruit', 'mango fruit', 'orange fruit', 'strawberry fruit'
];

// Fruit counts and seen status
const fruitCounts = {};
const fruitSeen = {}; // Track if a fruit has been seen
classLabels.forEach(label => {
    fruitCounts[label] = 0;
    fruitSeen[label] = false;
});

// Update fruit counts display
function updateFruitCountsDisplay() {
    let countsDisplay = '';
    classLabels.forEach(label => {
        if (fruitSeen[label]) {
            countsDisplay += `${label}: ${fruitCounts[label]}, `;
        }
    });
    fruitCountsText.textContent = countsDisplay.slice(0, -2); // Remove trailing comma and space
}

// Initial display (empty)
fruitCountsText.textContent = '';

// Handle image upload & preview
imageUpload.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.innerHTML = `<img src="${e.target.result}" alt="Image Preview">`;
        }
        reader.readAsDataURL(file);

        uploadMessage.textContent = "Image uploaded successfully!";
        uploadMessage.style.display = 'block';

        setTimeout(() => {
            uploadMessage.style.display = 'none';
        }, 2000);
    }
});

// Handle prediction
predictButton.addEventListener('click', function () {
    if (!imageUpload.files[0]) {
        alert("Please upload an image first.");
        return;
    }

    loader.style.display = 'block';
    resultText.textContent = "Please wait while the model is predicting...";
    predictButton.disabled = true;

    const formData = new FormData();
    formData.append('file', imageUpload.files[0]);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        loader.style.display = 'none';
        resultText.textContent = `Predicted: ${data}`;
        predictAnotherButton.style.display = 'inline-block';
        predictButton.disabled = false;
    
        // Update fruit counts and seen status
        const predictedLabel = classLabels.find(label => data.toLowerCase().includes(label.toLowerCase()));
        if (predictedLabel) {
            fruitCounts[predictedLabel]++;
            fruitSeen[predictedLabel] = true; // Mark fruit as seen
            updateFruitCountsDisplay();
        }
    })
    .catch(err => {
        loader.style.display = 'none';
        resultText.textContent = "Something went wrong.";
        predictButton.disabled = false;
    });
});

// Reset Functionality
resetButton.addEventListener('click', function () {
    classLabels.forEach(label => {
        fruitCounts[label] = 0;
        fruitSeen[label] = false; // Reset seen status
    });
    updateFruitCountsDisplay();
    predictAnotherButton.style.display = 'none';
    predictButton.disabled = false;
});

//Predict another button function
predictAnotherButton.addEventListener('click', ()=>{
    imageUpload.value = '';
    imagePreview.innerHTML = '';
    resultText.textContent = '';
    predictAnotherButton.style.display = 'none';
});

const liveDetectButton = document.getElementById('liveDetectButton');
if (liveDetectButton) {
    liveDetectButton.addEventListener('click', function () {
        window.location.href = '/camera';
    });
}
