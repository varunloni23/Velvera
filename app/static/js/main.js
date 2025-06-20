// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Cart quantity update
    const quantityInputs = document.querySelectorAll('.cart-quantity-input');
    if (quantityInputs) {
        quantityInputs.forEach(input => {
            input.addEventListener('change', function() {
                const cartId = this.dataset.cartId;
                const quantity = this.value;
                
                if (quantity < 1) {
                    this.value = 1;
                    return;
                }
                
                updateCartQuantity(cartId, quantity);
            });
        });
    }
    
    // Product image gallery
    const productThumbs = document.querySelectorAll('.product-thumb');
    if (productThumbs) {
        productThumbs.forEach(thumb => {
            thumb.addEventListener('click', function() {
                const mainImg = document.querySelector('.product-detail-img');
                if (mainImg) {
                    mainImg.src = this.src;
                    
                    // Remove active class from all thumbnails
                    productThumbs.forEach(t => t.classList.remove('active'));
                    
                    // Add active class to clicked thumbnail
                    this.classList.add('active');
                }
            });
        });
    }
    
    // Newsletter subscription
    const subscribeBtn = document.getElementById('subscribe-btn');
    if (subscribeBtn) {
        subscribeBtn.addEventListener('click', function() {
            const emailInput = this.previousElementSibling;
            const email = emailInput.value.trim();
            
            if (!email || !isValidEmail(email)) {
                alert('Please enter a valid email address');
                return;
            }
            
            // Here you would typically send the email to your server
            alert('Thank you for subscribing!');
            emailInput.value = '';
        });
    }
    
    // Dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages) {
        flashMessages.forEach(message => {
            setTimeout(() => {
                const closeBtn = message.querySelector('.btn-close');
                if (closeBtn) {
                    closeBtn.click();
                }
            }, 5000);
        });
    }
});

// Helper function to update cart quantity
function updateCartQuantity(cartId, quantity) {
    fetch('/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `cart_id=${cartId}&quantity=${quantity}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Reload the page to update the cart summary
            window.location.reload();
        } else {
            alert('Failed to update cart: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the cart');
    });
}

// Helper function to validate email
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
} 