import { roundToTwoDP } from "../utils.js";
import { getUrlComponents } from "./utils.js"

$(document).ready(function() {
    document.getElementById('productASIN').textContent = getUrlComponents().productId
    document.getElementById('productCategory').textContent = getUrlComponents().categoryPath;

    const productId = getUrlComponents().productId;

    // Construct the API endpoint URL
    const apiUrl = `http://systemiseselling.com/api/v1/product/${productId}`;

    // Make an AJAX request to the API
    $.ajax({
        url: apiUrl,
        type: 'GET',
        success: function(product) {
            console.log(product);
            // Assuming the API returns a product object structured as mentioned in your question
            document.getElementById('productImage').alt = product[0].category;

            const sellersTableBody = document.getElementById('sellersTableBody');
            sellersTableBody.innerHTML = ''; // Clear existing rows if any

            product.forEach(seller => {
                const row = `
                    <tr>
                        <td>${seller.seller_name}</td>
                        <td><a href="${seller.supplier_code}" target="_blank">${getUrlComponents().productId}</a></td>
                        <td>${seller.seller_price}</td>
                        <td>${roundToTwoDP(seller.profit_uk)}</td>
                        <td>${roundToTwoDP(seller.roi_uk)}</td>
                    </tr>
                `;
                sellersTableBody.innerHTML += row;
            });
        },
        error: function() {
            console.error('Failed to retrieve product data');
        }
    });
})