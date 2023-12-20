// Function to read Excel file using Fetch API
async function readExcelFile(filePath) {
    try {
        const response = await fetch(filePath);
        const arrayBuffer = await response.arrayBuffer();
        const data = new Uint8Array(arrayBuffer);
        const workbook = XLSX.read(data, { type: 'array' });
        return workbook;
    } catch (error) {
        throw error;
    }
}

// Function to search for a product in the Excel file.
// Function to search for a product in the Excel file.
document.querySelector('.search-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const searchInput = document.querySelector('.searchbar').value.trim();

    if (searchInput) {
        try {
            const filePath = 'datascrap.xlsx';

            const workbook = await readExcelFile(filePath);
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];

            const productData = XLSX.utils.sheet_to_json(worksheet);
            console.log('Search Input:', searchInput);
            console.log(productData);

            const searchKeywords = searchInput.toLowerCase().split(/\s+/);
            const matchingProducts = productData.filter((product) => {
                const productName = String(product["Product Name"]).toLowerCase();
                console.log('Product Name:', productName);

                // Check if all search keywords are present in the product name
                return searchKeywords.every(keyword => productName.includes(keyword));
            });

            console.log("Matching Products", matchingProducts);

            // Generate cards for matching products
            const productContainer = document.querySelector('.product-container');
            productContainer.innerHTML = ''; // Clear previous results

            matchingProducts.forEach((product) => {
                const card = createProductCard(product);
                productContainer.appendChild(card);
            });

            if (matchingProducts.length === 0) {
                productContainer.innerHTML = '<p>No matching products found.</p>';
            }
        } catch (error) {
            console.error('Error reading Excel file:', error);
        }
    }
});



// Function to create a product card
function createProductCard(product) {
    const card = document.createElement('div');
    card.classList.add('product-card');

    // Create elements for displaying product information.
    const productName = document.createElement('h3');
    productName.textContent = product['Product Name'];

    const gemPrice = document.createElement('p');
    gemPrice.textContent = `Gem Price: ₹${product['Price']}`;
    

    const gemLink = document.createElement('a');
    gemLink.textContent = 'View on GeM   ';
    gemLink.href = product['link'];
    gemLink.target = '_blank';


    const space1 = document.createElement('br');
    const space2 = document.createElement('br');

    const image=document.createElement('img');
    image.src=""+product["image"];
    image.style.width='90%';
    image.style.height='50%';


    // Add elements to the card.
    card.appendChild(image);
    card.appendChild(productName);
    card.appendChild(gemPrice);

   // card.appendChild(amazonPrice);
    // card.appendChild(flipkartPrice);
    card.appendChild(gemLink);
    // card.appendChild(space2);
    // card.appendChild(amazonLink);
    // card.appendChild(space1);
    // card.appendChild(flipkartLink);

    // Apply styles to the card (you can customize this).
    card.style.border = '1px solid #ccc';
    card.style.padding = '10px';
    card.style.margin = '10px';
    card.style.width='400px';
    card.style.borderRadius = '5px';

    return card;
}

