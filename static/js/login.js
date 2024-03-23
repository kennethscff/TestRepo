document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('login-form').addEventListener('submit', function(e) {
      e.preventDefault(); // Prevent the default form submission
      
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
  
      // Make sure both fields are filled out
      if (!email || !password) {
        alert('Please fill out both email and password.');
        return;
      }
  
      const loginData = {
        email: email, // Changed from username to match your HTML form and Flask code
        password: password
      };
  
      fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      })
      .then(response => {
        if(response.ok) {
          return response.json();
        }
        throw new Error('Invalid login'); // This will be caught by the catch block below
      })
      .then(data => {
        console.log('Success:', data);
        window.location.href = data.next_url; // Redirect to the returned URL
      })
      .catch((error) => {
        console.error('Error:', error);
        document.getElementById('login-error').classList.remove('d-none'); // Show the error message
      });
    });
  });
  