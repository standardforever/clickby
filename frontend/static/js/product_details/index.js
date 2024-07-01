import { get_environment_url } from "../config.js";
import { formatNumber, formatPercentage, roundToTwoDP } from "../utils.js";
import { getUrlComponents } from "./utils.js"

$(document).ready(function () {

    const token = localStorage.getItem('clickbuy_access')
    const dynamic_url = get_environment_url()
    if(!token){
        window.location.href = `${dynamic_url.url}/login`
    }
    document.getElementById('productASIN').textContent = getUrlComponents().productId
    document.getElementById('productCategory').textContent = getUrlComponents().categoryPath;
   
    
    const productId = getUrlComponents().productId;

    // Construct the API endpoint URL
    const apiUrl = `${dynamic_url.api_url}/product/${productId}`;

    // Make an AJAX request to the API
    function fetchProductData (token=localStorage.getItem('clickbuy_access')) {
        console.log(token)
        $.ajax({
            url: apiUrl,
            type: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            success: function (product) {
                // Assuming the API returns a product object structured as mentioned in your question
                // document.getElementById('productImage').alt = product[0].category;
    
                const sellersTableBody = document.getElementById('sellersTableBody');
                sellersTableBody.innerHTML = '';
    
                product.forEach(seller => {
                    document.getElementById('amzTitle').textContent = seller.title
                    const row = `
                        <tr>
                            <td>${seller.seller_name}</td>
                            <td><a href="${seller.supplier_code}" target="_blank">${getUrlComponents().productId}</a></td>
                            <td>${formatNumber(seller.seller_price)}</td>
                            <td>${formatNumber(roundToTwoDP(seller.profit_uk))}</td>
                            <td>${formatPercentage(roundToTwoDP(seller.roi_uk))}</td>
                            <td>${formatNumber(seller.total_fees_UK)}</td>
                            <td><a target="_blank" href="https://amazon.co.uk/dp/${seller.asin}">${seller.asin}</a></td>  
                        </tr>
                    `;
                    sellersTableBody.innerHTML += row;
                });
            },
            error: async function () {
                console.error('Failed to retrieve product data');
    
                try {
                    const retry = await $.ajax({
                        url: `${dynamic_url.api_url}/auth/token/refresh/`,
                        method: 'GET',
                        dataType: 'json',
                        contentType: 'application/json',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem("clickbuy_refresh")}`
                        }
                    });
                    
                    localStorage.setItem("clickbuy_access", retry.access_token);
                    localStorage.setItem("clickbuy_refresh", retry.refresh_token);
                    fetchProductData(retry.access_token);
                } catch (error) {
                    window.location.href = `${dynamic_url.url}/login`;
                }  
            }
        });

    }

    fetchProductData(token)
})