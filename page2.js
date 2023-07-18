const songs=document.getElementById("right_cnt");
const song_button=document.getElementById("song_btn");

function updateHeading(headingNumber) {
    const dropdown = document.getElementById(`dropdown${headingNumber}`);
    const heading = document.getElementById(`heading${headingNumber}`);
    const thumbnail_song = document.getElementById(`thumbnail_song${headingNumber}`);
    const selectedSong = dropdown.value;

    localStorage.setItem(`song${headingNumber}`, selectedSong);

    heading.textContent = selectedSong !== '' ? selectedSong : `Default Heading ${headingNumber}`;
    thumbnail_song.src = selectedSong !== '' ? `images/${selectedSong}.jpg` : thumbnail_song.src;
}
  

song_button.onclick=unblock;

function unblock(){
    songs.style.display="block";
}


const slider = document.getElementById('slider');
const sliderValue = document.getElementById('sliderValue');

slider.addEventListener('input', function() {
  sliderValue.textContent = slider.value;
  localStorage.setItem("slidervalue", slider.value);
});

var generateButton = document.getElementById("generate");

function changingSong(){
  localStorage.setItem("loadingSong", "firstsong");
}


function uploadSong(){
  const express = require('express');
  const multer = require('multer');
  const path = require('path');

  const app = express();

  // Configure multer for file upload
  const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, 'uploads/'); // Specify the directory where you want to store the uploaded files
    },
    filename: function (req, file, cb) {
      cb(null, Date.now() + path.extname(file.originalname)); // Rename the file with a timestamp
    }
  });

  const upload = multer({ storage: storage });

  // Handle file upload
  app.post('/upload', upload.single('file'), (req, res) => {
    if (req.file) {
      // File has been uploaded successfully
      res.send('File uploaded!');
    } else {
      // No file was uploaded
      res.status(400).send('No file selected!');
    }
  });

  // Start the server
  app.listen(3000, () => {
    console.log('Server is running on port 3000');
  });

}