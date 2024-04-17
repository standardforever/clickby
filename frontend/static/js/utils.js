export const truncateString = (str, maxLength) => {
    if (str.length > maxLength) {
        return str.substring(0, maxLength) + '...';
    }
    return str;
}

export function populateTable(data) {
    $(document).ajaxStop(function () {
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
    });
}

function clearTable() {
    // Clear the table content
    $('#myTable tbody').empty();
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
                // var cellData = getValueByPath(item, objectPath);
                row += '<td>' + objectPath + '</td>';
            });
            row += '</tr>';
            tbody.append(row);
        });
}

// export function populateTable(data) {
//     let cachedData = sessionStorage.getItem('cachedData'); // Retrieve cached data from sessionStorage
//     if (cachedData && data.length === 0) {
//         // If cached data exists, parse it and use it to populate the table
//         populateTableWithData(JSON.parse(cachedData));
//     } else if (data.length === 0) {
//         // If data is an empty array, retrieve cached data from sessionStorage and use it
//         populateTableWithData([]);
//     } else {
//         // If data is not an empty array, populate the table with the new data and store it in sessionStorage
//         populateTableWithData(data);
//         sessionStorage.setItem('cachedData', JSON.stringify(data));
//     }
//     // populateTableWithData(data)
// }

// function populateTableWithData(data) {
//     var tbody = $('#myTable tbody');
//     // Clear existing table rows
//     tbody.empty();

//     data.forEach(function(item) {
//         var row = '<tr>';
//         // Loop through each table header and retrieve data based on the object path
//         $('#myTable th').each(function(index, header) {
//             var headerTitle = $(header).text().trim();
//             var objectPath = getObjectPath(headerTitle, item);
//             // var cellData = getValueByPath(item, objectPath);
//             row += '<td>' + objectPath + '</td>';
//         });
//         row += '</tr>';
//         tbody.append(row);
//     });
// }


// Function to get object path for a given header title
function getObjectPath(headerTitle, item) {
    switch (headerTitle) {
        case "Product Name":
            return  item.title;
        case "Date Added":
            return item.last_update_time;

            // amazon link
        case "Amazon UK Link":
            return  item.asin;
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
            return truncateString(item.supplier_code, 20);
       
        case "UK Profit":
            return item.profit_uk;
        case "GER Profit":
            return item.profit_ger;
        case "FR Profit":
            return item.profit_fr;
        case "IT Profit":
            return item.profit_ir;
        case "SP Profit":
            return item.profit_sp;
        case "NT Profit":
            return item.profit_nt;
        case "USA Profit":
            return item.profit_usa;
        case "UK eBAY Profit":
            return item.profit_ebay_uk;
       
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

        case "UK Amazon fees":
            return  item.seller_price;
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