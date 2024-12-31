const longUrlInput = document.getElementById('long-url');
const shortenBtn = document.getElementById('shorten-btn');
const shortUrlContainer = document.getElementById('short-url-container');
const shortenedUrlLink = document.getElementById('shortened-url');

shortenBtn.addEventListener('click', async () => {
    const longUrl = longUrlInput.value;
    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: longUrl })
        });

        if (response.ok) {
            const data = await response.json();
            shortenedUrlLink.href = data.short_url;
            shortenedUrlLink.textContent = data.short_url;
            shortUrlContainer.style.display = 'block';
        } else {
            alert('Error shortening URL:', response.status);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while shortening the URL.');
    }
});