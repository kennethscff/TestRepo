function fetchTypeahead(searchTerm, inputId, suggestionsContainerId) {
  const inputElement = document.getElementById(inputId);
  const suggestionsContainer = document.getElementById(suggestionsContainerId);
  
  // Clear previous suggestions
  suggestionsContainer.innerHTML = '';

  if (searchTerm.length < 3) {
      suggestionsContainer.style.display = 'none';
      return;
  }

  fetch(`/typeahead?term=${encodeURIComponent(searchTerm)}`)
    .then(response => response.json())
    .then(data => {
      suggestionsContainer.innerHTML = ''; // Clear previous suggestions
      if (data.length > 0) {
          data.forEach(item => {
              const suggestionElement = document.createElement('div');
              suggestionElement.className = 'suggestion';
              suggestionElement.textContent = item.name;
              suggestionElement.onclick = function() {
                  inputElement.value = item.name;
                  suggestionsContainer.innerHTML = '';
                  suggestionsContainer.style.display = 'none';
              };
              suggestionsContainer.appendChild(suggestionElement);
          });
          suggestionsContainer.style.display = 'block';
      } else {
          suggestionsContainer.style.display = 'none';
      }
    })
    .catch(error => {
      console.error('Error fetching typeahead data:', error);
      suggestionsContainer.style.display = 'none';
    });
}


document.addEventListener('DOMContentLoaded', function () {
  document.getElementById("searchForm").addEventListener("submit", function(event) {
      var locationValue = document.getElementById("job-keyword-index").value;
      console.log("Location Value at Submission:", locationValue);
      if (!locationValue) {
          console.warn("Location value is empty or undefined at submission.");
          event.preventDefault(); // Prevent form submission if location is undefined
      }
  });
});
