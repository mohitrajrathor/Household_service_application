// file to store service related code
const origin = window.location.origin;

// add service
async function addService() {
    const form = document.getElementById('add-service');

    // form data
    const name = form.querySelector('input[name="name"]').value;
    const price = form.querySelector('input[name="price"]').value;
    const time_required = form.querySelector('input[name="time_required"]').value;
    const description = form.querySelector('textarea[name="description"]').value;

    const url = `${origin}/api/service/create`;

    const payload = {
        name: name,
        price: price,
        time_required: time_required,
        description: description
    };

    try{
        const response = await fetch(url,
            {
                method: 'POST',
                headers: {
                    'content-type' : 'application/json'
                },
                body: JSON.stringify(payload)
            }
        );

        const data = response.json();

        if (response.ok) {
            console.log(data.message);
            alert(data.message || "Service created successfully!");

            location.reload();
        }
        else {
            console.error(data.error || "Failed to add service");
            alert(data.error || "Unable to add service!")
        }
    }
    catch (error) {
        console.error('Error:', error);
        alert('An error occurred while adding the service.');
    }
}

// delete service
async function deleteService(service_id) {
    const url = `${origin}/api/service/delete-${service_id}`;
    try{
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'content-type' : 'application/json'
            },
            body: ''
        });

        const data = await response.json;

        if (response.ok) {
            console.log(data.message);
            alert(`Service with id ${service_id} is deleted successfully!`)

            location.reload();
        }
        else {
            console.error(data.error || "Failed to delete the service")
            alert(`Unable to delete service!`)
        }
    }
    catch (error) {
        console.error('Error:', error);
        alert('An error occurred while updating the service.');
    }

}

async function updateService(service_id) {

    const form = document.getElementById(`service-update-${service_id}`);

    const name = form.querySelector('input[name="name"]').value;
    const price = parseFloat(form.querySelector('input[name="price"]').value);
    const timeRequired = parseInt(form.querySelector('input[name="time_required"]').value);
    const description = form.querySelector('textarea[name="description"]').value;

    const url = `${origin}/api/service/update-${service_id}`;

    const payload = {
        name: name,
        price: price,
        time_required: timeRequired,
        description: description
    };

    try {
        // Make the PUT request
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        // Parse and log the response message
        const data = await response.json();

        if (response.ok) {
            console.log(data.message);
            alert(data.message);  // Optional: Show a success message to the user

            // Reload the page to reflect updated data
            location.reload();
        } else {
            console.error(data.error || 'Failed to update service');
            alert(data.error || 'Failed to update service');  // Show an error message to the user
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while updating the service.');
    }
}
