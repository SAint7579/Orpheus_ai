const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { Client } = require('pg');

const app = express();
const port = 3000;
const { spawn } = require('child_process');
// Enable CORS
app.use(cors());

// PostgreSQL database credentials
const client = new Client({
  user: 'postgres',
  host: 'localhost',
  database: 'orpheus',
  password: '1234',
  port: 5432,
});

app.use(bodyParser.json());

// Connect to the PostgreSQL database
client.connect()
  .then(() => {
    console.log('Connected to the database.');
  })
  .catch((error) => {
    console.error('Error connecting to the database: ' + error.message);
  });


// for python script to trigger
app.get('/trigger-python', (req, res) => {
  // Run the Python script using child_process.spawn
  // const pythonScript = spawn('python', ['C:/VS code projects/Orpheus-2/change_song.py']);

  const param1 = req.query.param1;
  const param2 = req.query.param2;
  const param3 = req.query.param3;
  const param4 = req.query.param4;

  const pythonScript = spawn('python', ['change_song.py',param1 ,param2, param3, param4]);
  pythonScript.stdout.on('data', (data) => {
    console.log(`Python script output: ${data}`);});

  pythonScript.stderr.on('data', (data) => {
    console.error(`Python script error: ${data}`);});

  pythonScript.on('close', (code) => {
    // console.log(`Python script exited with code ${code}`);
    res.send('Python script executed successfully');});
});


app.post('/insert', (req, res) => {
  const { value1, value2, value3, value4 } = req.body;

  // Prepare the SQL statement with placeholders
  const sql = 'INSERT INTO music (encoding, ratings, time_listened, songs) VALUES ($1, $2, $3, $4)';

  let byteaValue4;
  // if (value4 !== undefined) {
  //   // Convert value4 to bytea representation
  //   byteaValue4 = Buffer.from(value4).toString('hex');
  //   console.log(byteaValue4);
  // }

  // Execute the SQL statement with parameters
  client.query(sql, [value1, value2, value3, value4])
    .then(() => {
      res.send('Data inserted successfully.');
    })
    .catch((error) => {
      res.status(500).send('Error inserting data: ' + error.message);
    });
});





// Start the server
app.listen(port, () => {
  console.log('Server is running on port ' + port);
});
