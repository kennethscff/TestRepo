$(document).ready(function() {
    $('#search').click(function(event) {
        event.preventDefault(); // Prevent default form submission

        // Get values from form fields  
        let location = $('#job-keyword-index').val();

        // Construct the search URL
        let searchUrl = '/facets?location=' + encodeURIComponent(location)

        // Redirect the user to the search URL
        window.location.href = searchUrl;
    });
});

function handleSubmit(event) {
    event.preventDefault(); // Prevent the default form submission

    const form = event.target; // or document.getElementById('searchForm');
    const formData = new FormData(form);

    // Convert FormData to a query string
    let queryString = new URLSearchParams(formData).toString();

    // Redirect to the search page with query string
    window.location.href = `/search?${queryString}`;
}
