// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Preview uploaded image
    const imageInput = document.getElementById('product-image');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const preview = document.getElementById('image-preview');
            if (preview) {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    };
                    
                    reader.readAsDataURL(this.files[0]);
                }
            }
        });
    }
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.delete-btn');
    if (deleteButtons) {
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                    e.preventDefault();
                }
            });
        });
    }
    
    // Toggle category edit form
    const editCategoryButtons = document.querySelectorAll('.edit-category-btn');
    if (editCategoryButtons) {
        editCategoryButtons.forEach(button => {
            button.addEventListener('click', function() {
                const categoryId = this.dataset.categoryId;
                const viewRow = document.getElementById(`category-view-${categoryId}`);
                const editRow = document.getElementById(`category-edit-${categoryId}`);
                
                if (viewRow && editRow) {
                    viewRow.style.display = 'none';
                    editRow.style.display = 'table-row';
                }
            });
        });
    }
    
    // Cancel category edit
    const cancelEditButtons = document.querySelectorAll('.cancel-edit-btn');
    if (cancelEditButtons) {
        cancelEditButtons.forEach(button => {
            button.addEventListener('click', function() {
                const categoryId = this.dataset.categoryId;
                const viewRow = document.getElementById(`category-view-${categoryId}`);
                const editRow = document.getElementById(`category-edit-${categoryId}`);
                
                if (viewRow && editRow) {
                    viewRow.style.display = 'table-row';
                    editRow.style.display = 'none';
                }
            });
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
    
    // Initialize any datepickers
    const datepickers = document.querySelectorAll('.datepicker');
    if (datepickers.length > 0 && typeof flatpickr !== 'undefined') {
        flatpickr(datepickers, {
            dateFormat: "Y-m-d"
        });
    }
    
    // Format currency inputs
    const currencyInputs = document.querySelectorAll('.currency-input');
    if (currencyInputs) {
        currencyInputs.forEach(input => {
            input.addEventListener('blur', function() {
                const value = parseFloat(this.value);
                if (!isNaN(value)) {
                    this.value = value.toFixed(2);
                }
            });
        });
    }
}); 