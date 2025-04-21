const generateButton = document.getElementById('generate-button');
const promptInput = document.getElementById('prompt');
const generatedImage = document.getElementById('generated-image');
const loading = document.getElementById('loading');

generateButton.addEventListener('click', async () => {
    const prompt = promptInput.value;
    if (prompt.trim() === "") {
        alert("Please enter a scene description.");
        return;
    }



generatedImage.style.display = 'none'; loading.style.display = 'block';



    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        generatedImage.src = data.image_url;
        generatedImage.style.display = 'block';
    } catch (error) {
        console.error("Error generating image:", error);
        alert("Error generating image. Please try again.");
    } finally {
        loading.style.display = 'none';
    }
});