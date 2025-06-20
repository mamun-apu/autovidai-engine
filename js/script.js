document.addEventListener('DOMContentLoaded', () => {

    // --- ELEMENT REFERENCES ---
    const promptForm = document.querySelector('.prompt-form');
    const generateBtn = document.getElementById('generate-button');
    const promptInput = document.getElementById('prompt');

    const formCard = document.getElementById('form-card');
    const loadingCard = document.getElementById('loading-card');
    const resultCard = document.getElementById('result-card');
    const errorCard = document.getElementById('error-card');
    
    const resultVideo = document.getElementById('result-video');
    const downloadLink = document.getElementById('download-link');
    const resultPromptDisplay = document.getElementById('result-prompt-display');
    
    const generateAnotherBtn = document.getElementById('generate-another-button');
    const tryAgainBtn = document.getElementById('try-again-button');


    // --- STATE MANAGEMENT ---
    // A simple function to switch between UI states
    function showState(state) {
        // Hide all cards first
        formCard.style.display = 'none';
        loadingCard.style.display = 'none';
        resultCard.style.display = 'none';
        errorCard.style.display = 'none';

        // Show the correct card based on the state
        if (state === 'form') {
            formCard.style.display = 'block';
        } else if (state === 'loading') {
            loadingCard.style.display = 'block';
        } else if (state === 'result') {
            resultCard.style.display = 'block';
        } else if (state === 'error') {
            errorCard.style.display = 'block';
        }
    }


    // --- API CALL LOGIC ---

    // This is where the REAL API call will go.
    // It's commented out for now.
    /*
    async function realLumaApiCall(prompt, apiKey) {
        const API_URL = 'https://api.lumalabs.ai/dream-machine/v1/generations';

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                aspect_ratio: '16:9' // or '1:1', '9:16', etc.
            }),
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        // NOTE: The real Luma API is asynchronous. You first get an ID,
        // then you have to poll another endpoint to check the status.
        // For now, we'll keep our simpler mock flow.
        return await response.json();
    }
    */

    // Our FAKE API call, now with random success/failure for testing
    async function fakeLumaApiCall(userPrompt) {
        console.log("Mock API called with prompt:", userPrompt);
        await new Promise(resolve => setTimeout(resolve, 4000)); // Wait 4 seconds

        // Randomly decide if the API call "succeeds" or "fails"
        if (Math.random() > 0.25) { // 75% chance of success
            const fakeResponse = {
                video: {
                   url: "https://storage.googleapis.com/luma-labs-public/sample-video.mp4"
                }
            };
            console.log("Mock API responded with SUCCESS:", fakeResponse);
            return fakeResponse;
        } else { // 25% chance of failure
             console.log("Mock API responded with FAILURE");
             throw new Error("This is a simulated error. The raccoon spilled coffee on the server!");
        }
    }


    // --- EVENT HANDLERS ---
    promptForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const userPrompt = promptInput.value.trim();
        if (!userPrompt) {
            alert("Please enter a prompt!");
            return;
        }

        // Disable button to prevent multiple clicks
        generateBtn.disabled = true;
        generateBtn.textContent = "Generating...";

        showState('loading');

        try {
            // When you get your key, you'll swap this line:
            const result = await fakeLumaApiCall(userPrompt);
            // with this line:
            // const result = await realLumaApiCall(userPrompt, 'YOUR_API_KEY_HERE');

            // Update the result card with the new data
            resultPromptDisplay.textContent = userPrompt;
            resultVideo.src = result.video.url;
            downloadLink.href = result.video.url;

            showState('result');

        } catch (error) {
            console.error("An error occurred:", error.message);
            // Update the error message if you want
            // document.getElementById('error-message').textContent = error.message;
            showState('error');
        } finally {
            // Re-enable the button regardless of success or failure
            generateBtn.disabled = false;
            generateBtn.textContent = "Generate";
        }
    });

    // Event listener for the "Generate Another" button
    generateAnotherBtn.addEventListener('click', () => {
        promptInput.value = ''; // Clear the input field
        showState('form');
    });
    
    // Event listener for the "Try Again" button on the error card
    tryAgainBtn.addEventListener('click', () => {
        showState('form');
    });


    // --- INITIAL STATE ---
    // Start the app in the 'form' state when the page loads
    showState('form');
});