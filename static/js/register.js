document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = {
        email: document.getElementById('floatingEmail').value,
        password: document.getElementById('floatingPassword').value,
    };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            window.location.href = '/auth-register-property.html';
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.querySelector('form');
    const passwordInput = document.getElementById('floatingPassword');
    const confirmPasswordInput = document.getElementById('floatingConfirmPassword');
    const termsCheckbox = document.getElementById('flexCheckDefault');
    const registerButton = document.querySelector('form button[type="submit"]');
    const passwordErrorText = document.createElement('div');
    
    // Set up the error text element
    passwordErrorText.textContent = 'Passwords do not match.';
    passwordErrorText.style.color = 'red';
    passwordErrorText.style.display = 'none'; // Hide by default
    confirmPasswordInput.parentNode.insertBefore(passwordErrorText, confirmPasswordInput.nextSibling);

    function validateForm() {
        const passwordsMatch = passwordInput.value === confirmPasswordInput.value;
        const termsChecked = termsCheckbox.checked;

        registerButton.disabled = !(passwordsMatch && termsChecked);
        passwordErrorText.style.display = passwordsMatch ? 'none' : 'block'; // Show error text if passwords do not match

        if (!passwordsMatch) {
            confirmPasswordInput.setCustomValidity("Passwords do not match");
        } else {
            confirmPasswordInput.setCustomValidity("");
        }
    }

    // Add event listeners
    passwordInput.addEventListener('input', validateForm);
    confirmPasswordInput.addEventListener('input', validateForm);
    termsCheckbox.addEventListener('change', validateForm);

    registerForm.addEventListener('submit', function (e) {
        e.preventDefault();
        // Assuming you have set up the AJAX call to submit the form
        // You can place the AJAX call here
    });
});

function selectListingType(type) {
    // Reset styles for both cards
    const basicCard = document.getElementById('basicCard');
    const premiumCard = document.getElementById('premiumCard');
    basicCard.classList.remove('selected-card');
    premiumCard.classList.remove('selected-card');
    
    // Apply selected style to the clicked card
    if (type === 'basic') {
        basicCard.classList.add('selected-card');
    } else if (type === 'premium') {
        premiumCard.classList.add('selected-card');
    }
    
    // Optional: Set a hidden form field value based on selection if needed for form submission
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('propertyForm').addEventListener('submit', async function(e) {
        e.preventDefault(); // Prevent default form submission

        const formData = new FormData(this);
        const json = {};

        // Iterate over all form entries
        for (let [key, value] of formData.entries()) {
            // Special handling for checkboxes: check if the form element is present and if it's checked
            if (document.getElementById(key) && document.getElementById(key).type === 'checkbox') {
                json[key] = document.getElementById(key).checked;
            } else {
                // For all other input types, including selects and text inputs
                json[key] = value;
            }
        }

        // Placeholder for file handling logic
        // NOTE: Files cannot be directly converted to JSON. You might need to handle them separately
        // or encode them to base64, which is not covered here due to its complexity.

        console.log(json); // Debugging: log the JSON to be sent

        try {
            const response = await fetch('/register-property', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(json),
            });
            const data = await response.json();
            console.log('Success:', data);
            // Handle success (e.g., show success message, redirect, etc.)
        } catch (error) {
            console.error('Error:', error);
            // Handle errors (e.g., show error message)
        }
    });
});