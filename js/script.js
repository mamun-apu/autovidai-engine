// Wait until the entire HTML document is loaded before running the script
document.addEventListener('DOMContentLoaded', () => {

    // Get references to all the elements we need to interact with
    const promptForm = document.querySelector('.prompt-form');
    const formCard = document.getElementById('form-card');
    const loadingCard = document.getElementById('loading-card');
    const resultCard = document.getElementById('result-card');
    const resultVideo = document.getElementById('result-video');
    const downloadLink = document.getElementById('download-link');

    // This is our fake API call from before
    async function fakeLumaApiCall(userPrompt) {
        console.log("API called with prompt:", userPrompt);
        await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds

        const fakeResponse = {
            video: {
               url: "https://storage.googleapis.com/luma-labs-public/sample-video.mp4"
            }
        };
        console.log("Fake API responded:", fakeResponse);
        return fakeResponse;
    }

    // Listen for the form submission
    promptForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Stop the form from refreshing the page

        // 1. Hide the form and show the loading spinner
        formCard.style.display = 'none';
        loadingCard.style.display = 'block';
        resultCard.style.display = 'none'; // Ensure result is hidden

        // Get the user's prompt
        const promptText = document.getElementById('prompt').value;
        
        // 2. Call our fake API function and wait for it to finish
        const result = await fakeLumaApiCall(promptText);

        // 3. Once we have a result, update the UI
        // In a real app, you would get the URL from the 'result' object
        // resultVideo.src = result.video.url;
        // downloadLink.href = result.video.url;

        loadingCard.style.display = 'none';
        resultCard.style.display = 'block';
    });
});