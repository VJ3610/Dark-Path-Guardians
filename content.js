// Listen for messages from the extension popup
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'detectDarkPatterns') {
        // Get the current URL of the tab
        const currentUrl = window.location.href;

        // Send a POST request to the Flask server
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            
            body: 'website_url=' + encodeURIComponent(currentUrl),
        })
        .then(response => response.text())
        .then(data => {
            // Send the detected patterns back to the extension popup
            sendResponse({ detectedPatterns: data });
        })
        .catch(error => {
            console.error('Error:', error);
            // Send an error response back to the extension popup
            sendResponse({ error: 'An error occurred while detecting dark patterns.' });
        });

        // Indicate that the response will be sent asynchronously
        return true;
    }
});
