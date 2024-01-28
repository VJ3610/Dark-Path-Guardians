document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM content loaded');

    var form = document.getElementById('darkPatternForm');
    var predictButton = document.getElementById('predictButton');

    if (form && predictButton) {
        console.log('Form and Predict button elements found.');
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            predictDarkPatterns();
        });
    } else {
        console.error('Form or Predict button element not found.');
    }

    if (predictButton) {
        predictButton.addEventListener('click', predictDarkPatterns);
        console.log('Predict button element found.');
    } else {
        console.error('Predict button element not found.');
    }
});

function predictDarkPatterns() {
    var urlInput = document.getElementById("website_url");
    var resultList = document.getElementById('resultList');

    console.log('urlInput:', urlInput);
    console.log('resultList:', resultList);

    if (urlInput) {
        var url = urlInput.value;

        if (!url) {
            console.error('URL input is empty.');
            return;
        }

        console.log('Predicting dark patterns for URL:', url);

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'website_url=' + encodeURIComponent(url),
        })
        .then(response => {
            console.log('Response Status:', response.status);
            return response.text();
        })
        .then(data => {
            console.log('Received data:', data);

            // Split the data into an array of lines
            var lines = data.split('\n');

            // Clear previous results
            resultList.innerHTML = '';

            // Add each detected pattern as a list item
            lines.forEach(function (line) {
                var listItem = document.createElement('li');
                listItem.innerHTML = line;
                resultList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            console.log('Request URL:', 'http://127.0.0.1:5000/predict');
        });
    } else {
        console.error('URL input element not found.');
    }
}