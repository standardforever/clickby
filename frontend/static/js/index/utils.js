export const truncateString = (str, maxLength, truncateReturn = true) => {
    if (str.length > maxLength && truncateReturn) {
        return str.substring(0, maxLength) + '...';
    }
    return str;
}

export function populateTable(data) {
    // $(document).ajaxStop(function () {
        if (!$(this).data('ajax_in_progress')) {
            // When all AJAX requests are complete
            if (data.length === 0) {
                // If data is empty, update the table as empty
                clearTable();
            } else {
                // If data is not empty, populate the table with the new data
                populateTableWithData(data);
                sessionStorage.setItem('cachedData', JSON.stringify(data)); // Store data in sessionStorage
            }
        }
    // });
}

function clearTable() {
    var $tbody = $('#myTable tbody');
    $tbody.empty(); // First, clear the current content

    // Determine the number of columns by checking the headers
    var columnCount = $('#myTable thead tr th').length;

    // Add 10 empty rows with the correct number of cells
    for (var i = 0; i < 10; i++) {
        var $row = $('<tr>');
        for (var j = 0; j < columnCount; j++) {
            $row.append('<td>&nbsp;</td>'); // Append an empty cell; `&nbsp;` ensures the cell has height if styled
        }
        $tbody.append($row);
    }

    sessionStorage.removeItem('cachedData'); // Remove cached data from sessionStorage
}

function populateTableWithData(data) {
    var tbody = $('#myTable tbody');
        // Clear existing table rows
        tbody.empty();
    
        data.forEach(function(item) {
            var row = '<tr>';
            // Loop through each table header and retrieve data based on the object path
            $('#myTable th').each(function(index, header) {
                var headerTitle = $(header).text().trim();
                var objectPath = getObjectPath(headerTitle, item);

                const linkedItem = ['Amazon UK Link', 'Supplier Link', 'Coupon Code']                
                const productName = ['Product Name']                
                if(productName.includes(headerTitle)){
                    (row += '<td>' + objectPath + '<a target="_blank" id="dynamicLink" class="btn btn-primary ms-3 btn-sm" href="/product_details.html#'+ getObjectPath('asin', item, false)+ '?' + getObjectPath('Category', item, false)+'">' + "more seller" + '</a>' + '</td>')
                    // (row += '<td>' + objectPath + '<a target="_blank" class="btn btn-primary d-block" href="' + getObjectPath(headerTitle, item, false) + '">' + "view more" + '</a>' + '</td>')
                }else if(linkedItem.includes(headerTitle)) {
                    row += '<td><a target="_blank" href="' + getObjectPath(headerTitle, item, false) + '">' + getObjectPath('asin', item, false) + '</a></td>';
                }else{
                    (row += '<td>' + objectPath + '</td>')
                }   
                
            });
            row += '</tr>';
            tbody.append(row);
        });
}




function roundToTwoDP(num) {
    return Number(num.toFixed(2));
  }

// Function to get object path for a given header title
function getObjectPath(headerTitle, item, truncateReturn) {
    switch (headerTitle) {
        case "Product Name":
            return  item.title;
        case "Date Added":
            return item.last_update_time;

            // amazon link
        case "Amazon UK Link":
            return  item.amz_uk_link;
        case "Amazon GER Link":
            return  item.amz_ger_link;
        case "Amazon FR Link":
            return  item.amz_fr_link;
        case "Amazon IT Link":
            return  item.amz_it_link;
        case "Amazon SP Link":
            return  item.amz_sp_link;
        case "Amazon NT Link":
            return  item.amz_nt_link;
        case "Amazon USA Link":
            return  item.amz_usa_link;
        case "Amazon eBAY Link":
            return  item.amz_ebay_link;

        case "Supplier Link":
            return truncateString(item.supplier_code, 20, truncateReturn);
       
        case "UK Profit":
            return roundToTwoDP(item.profit_uk);
        case "GER Profit":
            return roundToTwoDP(item.profit_ger);
        case "FR Profit":
            return roundToTwoDP(item.profit_fr);
        case "IT Profit":
            return roundToTwoDP(item.profit_ir);
        case "SP Profit":
            return roundToTwoDP(item.profit_sp);
        case "NT Profit":
            return roundToTwoDP(item.profit_nt);
        case "USA Profit":
            return roundToTwoDP(item.profit_usa);
        case "UK eBAY Profit":
            return roundToTwoDP(item.profit_ebay_uk);
       
        case "Category":
            return item.category;

        case "UK Sales Rank":
            return item.Rank;
        case "GER Sales Rank":
            return item.ger_Rank;
        case "FR Sales Rank":
            return item.fr_Rank;
        case "IT Sales Rank":
            return item.it_Rank;
        case "SP Sales Rank":
            return item.sp_Rank;
        case "NT Sales Rank":
            return item.nt_Rank;
        case "USA Sales Rank":
            return item.usa_Rank;

        case "UK AMZ £":
            return  "undefined";
        case "GER Amazon fees":
            return  item.ger_seller_price;
        case "FR Amazon fees":
            return  item.fr_seller_price;
        case "IT Amazon fees":
            return  item.it_seller_price;
        case "SP Amazon fees":
            return  item.sp_seller_price;
        case "NT Amazon fees":
            return  item.nt_seller_price;
        case "USA Amazon fees":
            return  item.usa_seller_price;
        case "UK eBAY Amazon fees":
            return  item.uk_ebay_seller_price;


        case "Supplier Name":
            return  item.seller_name;
        case "Manufacturer":
            return  item.seller_name;
        case "ROI":
            return  roundToTwoDP(item.roi_uk);
        case "asin":
            return  item.asin;
        case "Amazon Selling Price":
            return  roundToTwoDP(item.amazon_price);
        case "Coupon Code":
            return item.supplier_code;
        case "Supplier Notes":
            return  "supplier note";
        // Add cases for other header titles as needed
        default:
            return ""; // Default to empty string if no object path is found
    }
}


export function populateROIDropdown(roiData) {
    var dropdownContent = $('#ROI');

    dropdownContent.empty();

    roiData.forEach(function(option) {
        var label = $('<label>');
        var checkbox = $('<input type="checkbox">').attr('name', 'roi_option').attr('value', option).attr('class', 'me-3');
        label.append(checkbox).append(option);
        dropdownContent.append(label);
    });
}

export function populateCATEGORIESDropdown(categoriesData) {
    var dropdownContent = $('#CATEGORIES');

    dropdownContent.empty();

    categoriesData.forEach(function(option) {
        var label = $('<label>');
        var checkbox = $('<input type="checkbox">').attr('name', 'category').attr('value', option).attr('class', 'me-3');
        label.append(checkbox).append(option);
        dropdownContent.append(label);
    });
}

export function populateSNDropdown(SNData) {
    var dropdownContent = $('#SN');

    dropdownContent.empty();

    SNData.forEach(function(option) {
        if(option !== null) {
            var label = $('<label>');
            var checkbox = $('<input type="checkbox">').attr('name', 'supplier-name').attr('value', option).attr('class', 'me-3');
            label.append(checkbox).append(option);
            dropdownContent.append(label);
        }
    });
}

export function populateSPDropdown(SpData) {
    var dropdownContent = $('#SP');

    dropdownContent.empty();

    SpData.forEach(function(option) {
        if(option !== null) {
            var label = $('<label>');
            var checkbox = $('<input type="checkbox">').attr('name', 'store-price').attr('value', option).attr('class', 'me-3');
            label.append(checkbox).append(option);
            dropdownContent.append(label);
        }
    });
}