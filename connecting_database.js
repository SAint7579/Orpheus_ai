// Description: Connecting to the database and inserting data into the database
const data = {
    encoding: 1,
    ratings: 5
};
fetch('/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({data: data}),
})
.then(response => response.text())
.then(result => {
    console.log('Server response:', result);
})
.catch(error => {
    console.error('Error:', error);
});