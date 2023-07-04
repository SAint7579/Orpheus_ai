// const {Client} = require('pg');
// const client = new Client({
//     user: 'postgres',
//     password: '1234',
//     host: 'localhost',
//     port: 5432,
//     database: 'orpheus',
// });

// client.connect()
// .then(() => console.log('Connected successfully'))
// // .then(() => client.query('INSERT INTO music values ($1,$2)',[1,3]))
// .then(() => client.query('SELECT * FROM music '))
// .then(results => console.table(results.rows))
// .catch(e => console.log(e))
// .finally(() => client.end());




// const { Pool } = require('pg');

// // Create a PostgreSQL connection pool
// const pool = new Pool({
//   user: 'postgres',
//   host: 'localhost',
//   database: 'orpheus',
//   password: '1234',
//   port: 5432,
// });

// module.exports = pool;





// // Middleware to parse JSON data in the request body
// app.use(express.json());

// // API endpoint to save data
// app.post('/saveData', (req, res) => {
//   const { encoding, ratings } = req.body; // Assuming the data contains 'encoding' and 'ratings' properties

//   // Insert data into PostgreSQL using a parameterized query
//   pool.query('INSERT INTO users (encoding, ratings) VALUES ($1, $2)', [encoding, ratings])
//     .then(() => {
//       res.status(200).send('Data saved successfully');
//     })
//     .catch((error) => {
//       console.error('Error saving data:', error);
//       res.status(500).send('Error saving data');
//     });
// });

// // Start the server
// app.listen(port, () => {
//   console.log(`Server is listening on port ${port}`);
// });

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