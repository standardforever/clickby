

export function getUrlComponents() {
    // Get the hash part of the current URL
    const hash = window.location.hash;

    // Split the hash by '?' to separate the product ID and any additional parameters
    const parts = hash.split('?');

    // Product ID: Remove the '#' from the first part to get only the product ID
    const productId = parts[0].substring(1);

    // Category Path: Decode URI component and replace '&' with space
    let categoryPath = "";
    if (parts.length > 1) {
        categoryPath = decodeURIComponent(parts[1]).replace(/&/g, ' ');
    }

    return {
        productId: productId,
        categoryPath: categoryPath
    };
}