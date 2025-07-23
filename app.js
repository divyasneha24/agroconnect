// Fetch MSP Information
document.getElementById('fetch-msp').addEventListener('click', async () => {
    const region = document.getElementById('region').value.trim();

    if (!region) {
        alert("Please enter a region.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/msp?region=`+region);
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const resultsDiv = document.getElementById('msp-results');
        resultsDiv.innerHTML = data.length
            ? data.map(item => `<p>Crop: ${item.crop}, Price: ₹${item.price}</p>`).join('')
            : "<p>No data found for the specified region.</p>";
    } catch (error) {
        console.error("Error fetching MSP data:", error);
        alert("Failed to fetch MSP data. Please try again.");
    }
});

// Compare Prices
document.getElementById('compare-prices').addEventListener('click', async () => {
    const product = document.getElementById('product').value.trim();

    if (!product) {
        alert("Please enter a product.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/compare?product=`+product);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const resultsDiv = document.getElementById('comparison-results');
        resultsDiv.innerHTML = data.length
            ? data.map(item => `<p>Region: ${item.region}, Price: ₹${item.price}</p>`).join('')
            : "<p>No comparison data found for the specified product.</p>";
    } catch (error) {
        console.error("Error comparing prices:", error);
        alert("Failed to fetch comparison data. Please try again.");
    }
});
