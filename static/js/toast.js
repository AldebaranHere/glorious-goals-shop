function showToast(title, message, type = 'normal', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    
    if (!toastComponent) return;

    // Remove all type classes first
    toastComponent.classList.remove(
        'bg-red-50', 'border-red-500', 'text-red-600',
        'bg-green-50', 'border-green-500', 'text-green-600',
        'bg-white', 'border-gray-300', 'text-gray-800'
    );

    // Set type styles and icon
    if (type === 'success') {
        toastComponent.classList.add('bg-green-50', 'border-green-500', 'text-green-600');
        toastComponent.style.border = '1px solid #22c55e';
    } else if (type === 'error') {
        toastComponent.classList.add('bg-red-50', 'border-red-500', 'text-red-600');
        toastComponent.style.border = '1px solid #ef4444';
    } else {
        toastComponent.classList.add('bg-white', 'border-gray-300', 'text-gray-800');
        toastComponent.style.border = '1px solid #d1d5db';
    }

    toastTitle.textContent = title;
    toastMessage.textContent = message;

    toastComponent.classList.remove('opacity-0', 'translate-y-64');
    toastComponent.classList.add('opacity-100', 'translate-y-0');

    setTimeout(() => {
        toastComponent.classList.remove('opacity-100', 'translate-y-0');
        toastComponent.classList.add('opacity-0', 'translate-y-64');
    }, duration);
}

document.getElementById('openCreateModal').onclick = () => document.getElementById('createModal').classList.remove('hidden');
document.getElementById('closeCreateModal').onclick = () => document.getElementById('createModal').classList.add('hidden');
document.getElementById('closeUpdateModal').onclick = () => document.getElementById('updateModal').classList.add('hidden');
document.getElementById('closeDeleteModal').onclick = () => document.getElementById('deleteModal').classList.add('hidden');

// For update and delete, you need to set the product info when opening the modal
document.getElementById('productList').addEventListener('click', function(e) {
  if (e.target.classList.contains('openUpdateModal')) {
    document.getElementById('updateName').value = e.target.dataset.name;
    document.getElementById('updatePrice').value = e.target.dataset.price;
    document.getElementById('updateModal').classList.remove('hidden');
    // Store product id for update
    window.currentUpdateId = e.target.dataset.id;
  }
  if (e.target.classList.contains('openDeleteModal')) {
    document.getElementById('deleteModal').classList.remove('hidden');
    window.currentDeleteId = e.target.dataset.id;
  }
});

document.addEventListener('DOMContentLoaded', function() {
  const productList = document.getElementById('productList');
  const refreshBtn = document.getElementById('refreshBtn');
  const loadingState = document.getElementById('loadingState');
  const errorState = document.getElementById('errorState');
  const emptyState = document.getElementById('emptyState');

  function showLoading() { loadingState.classList.remove('hidden'); }
  function hideLoading() { loadingState.classList.add('hidden'); }
  function showError(msg) { errorState.textContent = msg; errorState.classList.remove('hidden'); }
  function hideError() { errorState.classList.add('hidden'); }
  function showEmpty() { emptyState.classList.remove('hidden'); }
  function hideEmpty() { emptyState.classList.add('hidden'); }

  function fetchProducts() {
    showLoading();
    hideError();
    hideEmpty();
    fetch('/products/')
      .then(res => res.json())
      .then(data => {
        hideLoading();
        productList.innerHTML = '';
        if (data.length === 0) {
          showEmpty();
        } else {
          hideEmpty();
          data.forEach(product => {
            let div = document.createElement('div');
            div.className = 'border p-2 mb-2 flex justify-between items-center';
            div.innerHTML = `
              <span>${product.name} - $${product.price}</span>
              <div>
                <button class="openUpdateModal bg-yellow-400 px-2 py-1 rounded" data-id="${product.id}" data-name="${product.name}" data-price="${product.price}">Update</button>
                <button class="openDeleteModal bg-red-400 px-2 py-1 rounded" data-id="${product.id}">Delete</button>
              </div>
            `;
            productList.appendChild(div);
          });
        }
      })
      .catch(() => {
        hideLoading();
        showError('Failed to fetch products.');
      });
  }

  refreshBtn.addEventListener('click', fetchProducts);

  // Call fetchProducts after create/update/delete actions
  // Example: after successful product creation
  // fetchProducts();

  // Initial load
  fetchProducts();
});

const createProductForm = document.getElementById('createProductForm');
const createModal = document.getElementById('createModal');

if (createProductForm) {
  createProductForm.onsubmit = function(e) {
    e.preventDefault();
    showLoading();
    let formData = new FormData(this);
    fetch('/products/create/', {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      hideLoading();
      if (data.success) {
        showToast('Success', 'Product created successfully!', 'success');
        createModal.classList.add('hidden');
        fetchProducts();
      } else {
        showToast('Error', 'Failed to create product.', 'error');
        showError('Error: ' + JSON.stringify(data.errors));
      }
    })
    .catch(() => {
      hideLoading();
      showToast('Error', 'Failed to create product.', 'error');
      showError('Failed to create product.');
    });
  };
}

const updateProductForm = document.getElementById('updateProductForm');
const updateModal = document.getElementById('updateModal');

if (updateProductForm) {
  updateProductForm.onsubmit = function(e) {
    e.preventDefault();
    showLoading();
    let formData = new FormData(this);
    fetch(`/products/${window.currentUpdateId}/update/`, {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      hideLoading();
      if (data.success) {
        showToast('Success', 'Product updated successfully!', 'success');
        updateModal.classList.add('hidden');
        fetchProducts();
      } else {
        showToast('Error', 'Failed to update product.', 'error');
        showError('Error: ' + JSON.stringify(data.errors));
      }
    })
    .catch(() => {
      hideLoading();
      showToast('Error', 'Failed to update product.', 'error');
      showError('Failed to update product.');
    });
  };
}

const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
const deleteModal = document.getElementById('deleteModal');

if (confirmDeleteBtn) {
  confirmDeleteBtn.onclick = function() {
    showLoading();
    fetch(`/products/${window.currentDeleteId}/delete/`, {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')}
    })
    .then(res => res.json())
    .then(data => {
      hideLoading();
      if (data.success) {
        showToast('Success', 'Product deleted successfully!', 'success');
        deleteModal.classList.add('hidden');
        fetchProducts();
      } else {
        showToast('Error', 'Failed to delete product.', 'error');
        showError('Error deleting product.');
      }
    })
    .catch(() => {
      hideLoading();
      showToast('Error', 'Failed to delete product.', 'error');
      showError('Failed to delete product.');
    });
  };
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Show welcome, logout, and registration success messages
showToast('Welcome', 'Logged in successfully!', 'success');
showToast('Goodbye', 'Logged out successfully!', 'success');
showToast('Welcome', 'Account registered successfully!', 'success');