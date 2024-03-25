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
