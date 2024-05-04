import { populateCATEGORIESDropdown, populateROIDropdown, populateSNDropdown, populateTable, populateSPDropdown } from "./utils.js";

$(document).ready(function() {
    $(".loaderContainer").show();

    // PAGINATION CONTROL
    var currentPage = 1;
    var totalPages = 1;

    // Add event listeners to checkboxes in dropdowns
    $('.dropdown-content').on('change', 'input[type="checkbox"]', function() {
        fetchDataAndUpdatePagination();
    });

    // Function to get the checked values of checkboxes in a dropdown
    function getCheckedValues(dropdownId) {
        console.log($(this).val())
        var checkedValues
        if( dropdownId === "SP") {
            $('#' + dropdownId + ' input[type="checkbox"]').on('change', function() {
                if (this.checked) {
                    // Uncheck all other checkboxes
                    $('#' + dropdownId + ' input[type="checkbox"]').not(this).prop('checked', false);
                }
                checkedValues = this.checked ? $(this).val() : null;
            });

            // Get the value of the currently checked checkbox
            $('#' + dropdownId + ' input[type="checkbox"]:checked').each(function() {
                checkedValues = $(this).val(); // This will now always hold only the last checked value
            });
        }else{
            const tempArray = [];
            $('#' + dropdownId + ' input[type="checkbox"]:checked').each(function() {
                tempArray.push($(this).val());
            });
            checkedValues = tempArray
        }
        
        return checkedValues;
    }

   
    $('#clear-filter-id').click(function() {
        // Reset the values of all dropdown checkboxes to unchecked
        $('.dropdown-content input[type="checkbox"]').prop('checked', false);
        $('#search-input').val("")
        currentPage = 1
        // Trigger the search functionality with empty filter values
        fetchDataAndUpdatePagination();
    });


    // Update the data object for the POST request with the checked values
    function updateDataObject() {
        console.log('Updating data object')
        return {
            "roi": getCheckedValues('ROI'),
            "categories": getCheckedValues('CATEGORIES'),
            "supplier_name": getCheckedValues('SN'),
            "market_place": [], 
            "store_price": getCheckedValues('SP'),
            "search_term": $('#search-input').val()
        };
    }

    function makeAjaxCall(url) {
        return $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json'
        });
    }

    function makePostRequest(url, data) {
        return $.ajax({
            url: url,
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json', // Set content type to JSON
            data: JSON.stringify(data) // Convert data object to JSON string
        });
    }

    function updatePagination() {
        var paginationList = $(".pagination");
        paginationList.empty();

        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="first-page">First</a></li>');
        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="prev-page">Previous</a></li>');

        for (var i = 1; i <= totalPages; i++) {
            var pageClass = (i === currentPage) ? "active" : "";
            paginationList.append('<li class="page-item ' + pageClass + '"><a class="page-link text-black " href="#" data-page="' + i + '">' + i + '</a></li>');
        }

        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="next-page">Next</a></li>');
        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="last-page">Last</a></li>');
    }

    function updateUniqueProductCount(totalCount) {
        $('#unique-product-count').text(totalCount.toLocaleString());
    }

    function fetchDataAndUpdatePagination(pageNumber) {
        pageNumber = currentPage; // Use currentPage if pageNumber is not provided
       return makePostRequest('http://52.3.255.252/api/v1/home/10/' + ((pageNumber - 1) * 15) + '', updateDataObject())
        .done(function(response) {
            populateTable(response.data);
            totalPages = Math.ceil(response.total_count / 15);  
            updateUniqueProductCount(response.total_count);
            currentPage = pageNumber; // Update currentPage
            updatePagination();
            $(".loaderContainer").hide();
        })
        .fail(function(err) {
            console.log('An error occurred during AJAX calls.', err);
            $(".loaderContainer").hide();
        });
    }

    const OnLoadPageFunc = () => {
        var promises = [
            makeAjaxCall('http://52.3.255.252/api/v1/category'),
            makeAjaxCall('http://52.3.255.252/api/v1/supplier-name'),
            makeAjaxCall('http://52.3.255.252/api/v1/roi'),
            makeAjaxCall('http://52.3.255.252/api/v1/store-price'),
           
        ];
    
        $.when.apply($, promises).then(function() {   
            populateROIDropdown(promises[2].responseJSON)
            populateCATEGORIESDropdown(promises[0].responseJSON)
            populateSNDropdown(promises[1].responseJSON)
            populateSPDropdown(promises[3].responseJSON)
          
            // $(".loaderContainer").hide();
            return true;
        }).fail(function(err) {
            console.log('An error occurred during AJAX calls.', err);
            // $(".loaderContainer").hide();
            return false;
        });
    }

    fetchDataAndUpdatePagination().then(function() {
        // When fetchDataAndUpdatePagination is done, execute the rest of the AJAX calls
        OnLoadPageFunc();
    });

    var pagesToShow = 5;

    function updatePagination() {
        var paginationList = $(".pagination");
        paginationList.empty();

        // First Page Button
        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="first-page">First</a></li>');

        // Previous Page Button
        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="prev-page">Previous</a></li>');

        // Display pagination with current page in the middle
        var startPage = Math.max(1, currentPage - Math.floor(pagesToShow / 2));
        var endPage = Math.min(totalPages, startPage + pagesToShow - 1);
        for (var i = startPage; i <= endPage; i++) {
            var pageClass = (i === currentPage) ? "active" : "";
            paginationList.append('<li class="page-item ' + pageClass + '"><a class="page-link text-black " href="#" data-page="' + i + '">' + i + '</a></li>');
        }

        // Next Page Button
        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="next-page">Next</a></li>');

        // Last Page Button
        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="last-page">Last</a></li>');
    }

    $('.pagination').on('click', 'a', function(e) {
        e.preventDefault();
        var pageId = $(this).attr('id');
        if (pageId === 'first-page') {
            currentPage = 1;
        } else if (pageId === 'prev-page') {
            if (currentPage > 1) {
                currentPage--;
            }
        } else if (pageId === 'next-page') {
            if (currentPage < totalPages) {
                currentPage++;
            }
        } else if (pageId === 'last-page') {
            currentPage = totalPages;
        } else {
            currentPage = parseInt($(this).attr('data-page'));
        }
        fetchDataAndUpdatePagination();
    });

    // Initialize pagination
    updatePagination();

    
    $('#search-button').click(function() {
        $(".tableLoadContainer").show();
        $('#myTable tbody').hide();
        $.ajax({
            url: "http://52.3.255.252/api/v1/home/15/0",
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json', // Set content type to JSON
            data: JSON.stringify({
                "roi": [],
                "categories": [],
                "supplier_name": [],
                "market_place": [],
                "store_price": "",
                "search_term": $('#search-input').val()
            }),
            success: function(response) {
                $(".tableLoadContainer").hide();
                $('#myTable tbody').show();
                populateTable(response.data);
                totalPages = Math.ceil(response.total_count / 15);  
                updateUniqueProductCount(response.total_count);
                currentPage = 1; // Update currentPage
                updatePagination();
                $(".loaderContainer").hide();
            },
            error: function(xhr, status, error) {
                $(".tableLoadContainer").hide();
                $('#myTable tbody').show();
                console.error('Error occurred during search:', error);
            }
        });
    });

    function countChecked() {
        return $('.new-content-item input[type="checkbox"]:checked').length;
    }

    $('.new-content-item input[type="checkbox"]').on('change', function() {
        var isChecked = $(this).prop('checked');
        var itemName = $(this).closest('.new-content-item').text().trim();
        if (!isChecked && countChecked() <= 4) {
            alert('You must have at least four checked columns.');
            $(this).prop('checked', true);
            return;
        }
        if (isChecked && countChecked() > 4) {
            if ($('#myTable th:contains(' + itemName + ')').length === 0) {
                $('#myTable thead tr').append('<th>' + itemName + '</th>');
                $('#myTable tbody tr').each(function() {
                    $(this).append('<td></td>');
                });
            }
        } else if (!isChecked && countChecked() > 3) {
            var index = $('#myTable th:contains(' + itemName + ')').index();
            if (index !== -1) {
                $('#myTable th:eq('+index+')').remove();
                $('#myTable td:nth-child('+(index+1)+')').remove();
            }
        }
        var updatedData = fetchDataAndUpdatePagination();
        populateTable(updatedData);
    });

    $('.new-content-item input[type="checkbox"]').each(function(index, item) {
        var itemName = $(item).closest('.new-content-item').text().trim();
        var index = $('#myTable th').filter(function() {
            return $(this).text() === itemName;
        }).index();
        if (!$(item).prop('checked')) {
            $('#myTable td:nth-child('+(index+1)+')').hide();
        }
    });
});

document.getElementById('scrollLeftBtn').addEventListener('click', function() {
    scrollTable('left');
});

document.getElementById('scrollRightBtn').addEventListener('click', function() {
    scrollTable('right');
});

let currentTranslateX = 0;

function scrollTable(direction) {
    const table = document.getElementById('myTable');
    const tableWidth = table.offsetWidth;
    const containerWidth = table.parentElement.offsetWidth;
    const firstColumnLeftEdge = table.querySelector('th:first-child').getBoundingClientRect().left;
    const lastColumn = table.querySelector('th:last-child');
    const lastColumnRightEdge = lastColumn.getBoundingClientRect().right;
    const containerRightEdge = table.parentElement.getBoundingClientRect().right;

    const maxScrollLeft = 0;
    const maxScrollRight = tableWidth - containerWidth;

    if (direction === 'left' && currentTranslateX === maxScrollLeft) {
        return;
    }

    if (direction === 'right' && containerRightEdge >= lastColumnRightEdge) {
        return;
    }

    const scrollStep = 50;

    if (direction === 'left') {
        currentTranslateX = Math.max(currentTranslateX - scrollStep, maxScrollLeft);
    } else if (direction === 'right') {
        currentTranslateX = Math.min(currentTranslateX + scrollStep, maxScrollRight);
    }

    table.style.transform = `translateX(-${currentTranslateX}px)`;
}

document.querySelector('.addBtn').addEventListener('click', function() {
    var dropdown = document.querySelector('.new-content');
    if (dropdown.style.display === 'none') {
        dropdown.style.display = 'flex';
    } else {
        dropdown.style.display = 'none';
    }
});

document.querySelector('.filterBtn').addEventListener('click', function() {
    var dropdown = document.querySelector('.filter-content');
    if (dropdown.style.display === 'none') {
        dropdown.style.display = 'flex';
    } else {
        dropdown.style.display = 'none';
    }
});

document.body.addEventListener('click', function(event) {
    var target = event.target;
    var dropdown = document.querySelector('.new-content');
    var addBtn = document.querySelector('.addBtn');
    if (target !== addBtn && !addBtn.contains(target) && target !== dropdown && !dropdown.contains(target)) {
        dropdown.style.display = 'none';
    }
});

document.body.addEventListener('click', function(event) {
    var target = event.target;
    var dropdown = document.querySelector('.filter-content');
    var filterBtn = document.querySelector('.filterBtn');
    if (target !== filterBtn && !filterBtn.contains(target) && target !== dropdown && !dropdown.contains(target)) {
        dropdown.style.display = 'none';
    }
});

