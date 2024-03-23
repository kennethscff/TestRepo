function fetchTypeahead(searchTerm) {
    const suggestionsContainer = document.getElementById('typeahead-suggestions');
    
    // Clear previous suggestions
    suggestionsContainer.innerHTML = '';
    
    if (searchTerm.length < 3) {
      suggestionsContainer.style.display = 'none'; // Hide suggestions if search term is too short
      return;
    }
    
    fetch(`/typeahead?term=${encodeURIComponent(searchTerm)}`)
      .then(response => response.json())
      .then(data => {
        if (data.length > 0) {
          // Use the data to create suggestions
          data.forEach(item => {
            if (Array.from(suggestionsContainer.children).some(child => child.textContent === item.name)) {
                return;
            }
            const suggestionElement = document.createElement('div');
            suggestionElement.className = 'suggestion';
            suggestionElement.textContent = item.name;
            suggestionElement.onclick = function() {
              // Fill the input when a suggestion is clicked
              document.getElementById('job-keyword').value = item.name;
              // Clear suggestions
              suggestionsContainer.innerHTML = '';
              suggestionsContainer.style.display = 'none'; // Hide suggestions after selection
            };
            suggestionsContainer.appendChild(suggestionElement);
          });
          suggestionsContainer.style.display = 'block'; // Show suggestions
        } else {
          suggestionsContainer.style.display = 'none'; // Hide suggestions if no data
        }
      })
      .catch(error => {
        console.error('Error fetching typeahead data:', error);
        suggestionsContainer.style.display = 'none'; // Hide suggestions on error
      });
  }
  