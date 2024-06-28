import { formatDate } from "../utils.js";
import { populateCATEGORIESDropdown, populateROIDropdown, populateSNDropdown, populateTable, populateSPDropdown , populateSalesRankDropdown, getSortValue} from "./utils.js";

$(document).ready(function () {
    $(".loaderContainer").show();

    // PAGINATION CONTROL
    var currentPage = 1;
    var totalPages = 1;
    var holdData;
    var sortByColumn = 'profit_uk';
    var ascendDecend = -1

    // sort
    $('.sort-icon').on('click', function () {
        // Remove the active class from all sort icons
        $('.sort-icon').removeClass('active');

        // Add the active class to the clicked icon
        $(this).addClass('active');

        // Get the id of the clicked icon
        var iconId = $(this).attr('id');

        // Split the id to get the order and column
        var [order, column] = iconId.split('-');

        // Update the sortByColumn variable
        sortByColumn = getSortValue(column);

        // Update the ascendDecend variable
        ascendDecend = (order === 'asc') ? 1 : -1;

        fetchDataAndUpdatePagination()
    });

    // Add event listener to the "Apply" button
    $('#DA .btn-primary').on('click', function () {
        fetchDataAndUpdatePagination();
    });

    // Prevent typing in datetime-local inputs
    document.querySelectorAll('input[type="datetime-local"]').forEach(input => {
        input.addEventListener('keydown', function (event) {
            event.preventDefault();
        });
    });

    // Add event listeners to checkboxes in dropdowns
    $('.dropdown-content').on('change', 'input[type="checkbox"]', function () {
        fetchDataAndUpdatePagination();
    });
    

    // Function to get the checked values of checkboxes in a dropdown
    function getCheckedValues(dropdownId) {
        var checkedValues;
        if (dropdownId === "SP" || dropdownId === "SR") {
            $('#' + dropdownId + ' input[type="checkbox"]').on('change', function () {
                if (this.checked) {
                    $('#' + dropdownId + ' input[type="checkbox"]').not(this).prop('checked', false);
                }
                checkedValues = this.checked ? $(this).val() : "";
            });
            $('#' + dropdownId + ' input[type="checkbox"]:checked').each(function () {
                checkedValues = $(this).val();
            });
        } else {
            const tempArray = [];
            $('#' + dropdownId + ' input[type="checkbox"]:checked').each(function () {
                tempArray.push($(this).val());
            });
            checkedValues = tempArray;
        }
        return checkedValues;
    }

    $('#clear-filter-id').click(function () {
        $('.dropdown-content input[type="checkbox"]').prop('checked', false);
        $('#search-input').val("");
        $('#startDate').val("");
        $('#endDate').val("")
        currentPage = 1;
        fetchDataAndUpdatePagination();
    });

    // Function to format date to "yyyy-mm-dd hh:mm:ss"

    // Update the data object for the POST request with the checked values
    function updateDataObject() {
        return {
            "roi": getCheckedValues('ROI'),
            "categories": getCheckedValues('CATEGORIES'),
            "supplier_name": getCheckedValues('SN'),
            "market_place": [],
            "store_price": getCheckedValues('SP'),
            "sales_rank": getCheckedValues('SR'),
            "search_term": $('#search-input').val(),
            "start_date": $('#startDate').val() ? formatDate($('#startDate').val()) : "",
            "end_date": $('#endDate').val() ? formatDate($('#endDate').val()) : ""
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
            contentType: 'application/json',
            data: JSON.stringify(data)
        });
    }

    // add column filter
    $('.new-content-item').on('click', function() {
        var targetId = $(this).data('target');

        
        // Hide all filter content divs
        $('.filter-dropdown-content').removeClass('d-block').addClass('d-none');
        
        // Show the selected filter content
        $('#' + targetId).removeClass('d-none').addClass('d-block');


            // Handle clicks outside the filter content and new content items
            $(document).on('click', function(event) {
                if (!$(event.target).closest('.new-content-item, .filter-dropdown-content').length) {
                    // Hide all filter content divs
                    $('.filter-dropdown-content').removeClass('d-block').addClass('d-none');
                }
            });

            // Prevent the filter content div from closing when clicking inside
            $('.filter-dropdown-content, .new-content-item').on('click', function(event) {
                event.stopPropagation(); // Prevent the click event from propagating to the document
            });
    });



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
        pageNumber = currentPage;
        const itemsPerPage = 50;
        return makePostRequest(`http://app.clickbuy.ai/api/v1/home?limit=${itemsPerPage}&skip=${((pageNumber - 1) * itemsPerPage)}&count_doc=false&sort_by_column=${sortByColumn}&ascend_decend=${ascendDecend}`, updateDataObject())
            .done(async function (response) {
                
                const res = await makePostRequest('http://app.clickbuy.ai/api/v1/home?count_doc=true', updateDataObject());
                populateTable(response.data);
                holdData = response.data;
                currentPage = pageNumber;
                totalPages = Math.ceil(res.total_count / 50);
                updateUniqueProductCount(res.total_count);
                updatePagination();
                $(".loaderContainer").hide();
            })
            .fail(function (err) {
                console.log('An error occurred during AJAX calls.', err);
                $(".loaderContainer").hide();
            });
    }

    const OnLoadPageFunc = () => {
        var promises = [
            makeAjaxCall('http://app.clickbuy.ai/api/v1/category'),
            makeAjaxCall('http://app.clickbuy.ai/api/v1/supplier-name'),
            makeAjaxCall('http://app.clickbuy.ai/api/v1/roi'),
            makeAjaxCall('http://app.clickbuy.ai/api/v1/store-price'),
            makeAjaxCall('http://app.clickbuy.ai/api/v1/sales-rank')
        ];

        $.when.apply($, promises).then(function () {
            populateROIDropdown(promises[2].responseJSON);
            populateCATEGORIESDropdown(promises[0].responseJSON);
            populateSNDropdown(promises[1].responseJSON);
            populateSPDropdown(promises[3].responseJSON);
            populateSalesRankDropdown(promises[4].responseJSON);
            return true;
        }).fail(function (err) {
            console.log('An error occurred during AJAX calls.', err);
            return false;
        });
    }

    fetchDataAndUpdatePagination().then(function () {
        OnLoadPageFunc();
    });

    var pagesToShow = 5;

    function updatePagination() {
        var paginationList = $(".pagination");
        paginationList.empty();

        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="first-page">First</a></li>');
        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="prev-page">Previous</a></li>');

        var startPage = Math.max(1, currentPage - Math.floor(pagesToShow / 2));
        var endPage = Math.min(totalPages, startPage + pagesToShow - 1);
        for (var i = startPage; i <= endPage; i++) {
            var pageClass = (i === currentPage) ? "active" : "";
            paginationList.append('<li class="page-item ' + pageClass + '"><a class="page-link text-black " href="#" data-page="' + i + '">' + i + '</a></li>');
        }

        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="next-page">Next</a></li>');
        paginationList.append('<li class="page-item"><a class="page-link text-black " href="#" id="last-page">Last</a></li>');
    }

    $('.pagination').on('click', 'a', function (e) {
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

    updatePagination();

    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    // Event listener for search input with debounce
    $('#search-input').on('input', debounce(function () {
        $(".tableLoadContainer").show();
        $('#myTable tbody').hide();
        $.ajax({
            url: "http://app.clickbuy.ai/api/v1/home?limit=50&skip=0",
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                "roi": [],
                "categories": [],
                "supplier_name": [],
                "market_place": [],
                "store_price": "",
                "sales_rank": "",
                "search_term": $('#search-input').val(),
                "start_date": $('#startDate').val() ? formatDate($('#startDate').val()) : "",
                "end_date": $('#endDate').val() ? formatDate($('#endDate').val()) : ""
            }),
            success: async function (response) {
                $(".tableLoadContainer").hide();
                $('#myTable tbody').show();
                currentPage = 1;
                populateTable(response.data);
                const res = await makePostRequest('http://app.clickbuy.ai/api/v1/home?count_doc=true', updateDataObject());
                totalPages = Math.ceil(res.total_count / 50);
                updateUniqueProductCount(res.total_count);
                updatePagination();
                $(".loaderContainer").hide();
            },
            error: function (xhr, status, error) {
                $(".tableLoadContainer").hide();
                $('#myTable tbody').show();
                console.error('Error occurred during search:', error);
            }
        });
    }, 300)); // 300ms delay

    function countChecked() {
        return $('.new-content-item input[type="checkbox"]:checked').length;
    }

    $('.new-content-item input[type="checkbox"]').on('change', function () {
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
                $('#myTable tbody tr').each(function () {
                    $(this).append('<td></td>');
                });
            }
        } else if (!isChecked && countChecked() > 3) {
            var index = $('#myTable th:contains(' + itemName + ')').index();
            if (index !== -1) {
                $('#myTable th:eq(' + index + ')').remove();
                $('#myTable td:nth-child(' + (index + 1) + ')').remove();
            }
        }
        var updatedData = holdData ?? fetchDataAndUpdatePagination();
        populateTable(updatedData);
    });

    $('.new-content-item input[type="checkbox"]').each(function (index, item) {
        var itemName = $(item).closest('.new-content-item').text().trim();
        var index = $('#myTable th').filter(function () {
            return $(this).text() === itemName;
        }).index();
        if (!$(item).prop('checked')) {
            $('#myTable td:nth-child(' + (index + 1) + ')').hide();
        }
    });
    
});

document.getElementById('scrollLeftBtn').addEventListener('click', function () {
    scrollTable('left');
});

document.getElementById('scrollRightBtn').addEventListener('click', function () {
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

document.querySelector('.addBtn').addEventListener('click', function () {
    var dropdown = document.querySelector('.new-content');
    if (dropdown.style.display === 'none') {
        dropdown.style.display = 'block';
    } else {
        dropdown.style.display = 'none';
    }
});

document.querySelector('.filterBtn').addEventListener('click', function () {
    var dropdown = document.querySelector('.filter-content');
    if (dropdown.style.display === 'none') {
        dropdown.style.display = 'flex';
    } else {
        dropdown.style.display = 'none';
    }
});

document.body.addEventListener('click', function (event) {
    var target = event.target;
    var dropdown = document.querySelector('.new-content');
    var addBtn = document.querySelector('.addBtn');
    if (target !== addBtn && !addBtn.contains(target) && target !== dropdown && !dropdown.contains(target)) {
        dropdown.style.display = 'none';
    }
});

document.body.addEventListener('click', function (event) {
    var target = event.target;
    var dropdown = document.querySelector('.filter-content');
    var filterBtn = document.querySelector('.filterBtn');
    if (target !== filterBtn && !filterBtn.contains(target) && target !== dropdown && !dropdown.contains(target)) {
        dropdown.style.display = 'none';
    }
});
