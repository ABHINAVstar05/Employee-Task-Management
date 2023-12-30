// Function to fetch data from the API
async function fetchData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/employee_management');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to render data in cards
async function renderData() {
    const container = document.querySelector('.container');
    const data = await fetchData();

    if (!data) {
        return;
    }

    data.forEach(item => {
        const card = document.createElement('div');
        card.classList.add('card');

        const title = document.createElement('h2');
        title.textContent = "Name: " + item.name;

        const body1 = document.createElement('p');
        body1.textContent = "Email ID: " + item.email;
        const body2 = document.createElement('p');
        body2.textContent = "Employee role: " + item.role;

        card.appendChild(title);
        card.appendChild(body1);
        card.appendChild(body2);
        container.appendChild(card);
    });
}

// Call the renderData function to display data
renderData();