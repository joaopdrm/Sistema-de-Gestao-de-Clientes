document.addEventListener('DOMContentLoaded', loadCustomers);

function loadCustomers() {
    fetch('/customers')
        .then(response => response.json())
        .then(data => {
            const customersList = document.getElementById('customers');
            customersList.innerHTML = '';
            data.forEach(customer => {
                const li = document.createElement('li');
                li.innerHTML = `Name: ${customer.name}, Email: ${customer.email}, Phone: ${customer.phone} <button class="remove-button" onclick="removeCustomer(${customer.id})">Remove</button>`;
                customersList.appendChild(li);
            });
        });
}

function addCustomer() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;

    fetch('/customers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, phone })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadCustomers();
    });
}

function removeCustomer(id) {
    fetch(`/customers/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadCustomers();
    });
}
