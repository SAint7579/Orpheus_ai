const songs=document.getElementById("right_cnt");
const song_button=document.getElementById("song_btn");


localStorage.setItem("song1", "None");
localStorage.setItem("song2", "None");
localStorage.setItem("song3", "None");

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
localStorage.setItem("slidervalue", slider.value);
slider.addEventListener('input', function() {
  sliderValue.textContent = slider.value;
  localStorage.setItem("slidervalue", slider.value);
});

var generateButton = document.getElementById("generate");

function changingSong(){
  localStorage.setItem("loadingSong", "firstsong");
}

var generate_randomly=document.getElementById("generate_randomly");

function randomly(){
  localStorage.setItem("song1", "22");
  localStorage.setItem("loadingSong", "firstsong");
}









document.getElementById('upload_btn').addEventListener('click', function(event) {
  event.preventDefault(); // Prevent default button click behavior
  document.getElementById('fileToUpload').click(); // Trigger the file input click event
});

document.getElementById('uploadForm').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the default form submission behavior

  var formData = new FormData(this);

  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:3000/upload', true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        console.log(xhr.responseText);
        // Handle the response from the server here
      } else {
        console.error('Error:', xhr.status);
        // Handle any errors that occurred during the request
      }
    }
  };
  xhr.send(formData);
});

// document.getElementById('uploadForm').addEventListener('submit', function(event) {
//   event.preventDefault(); // Prevent the default form submission behavior

//   var formData = new FormData(this);

//   var xhr = new XMLHttpRequest();
//   xhr.open('POST', 'http://localhost:3000/upload', true);
//   xhr.onreadystatechange = function() {
//     if (xhr.readyState === 4 && xhr.status === 200) {
//       console.log(xhr.responseText);
//       // Handle the response from the server here
//     } else if (xhr.readyState === 4 && xhr.status !== 200) {
//       console.error('Error:', xhr.status);
//       // Handle any errors that occurred during the request
//     }
//   };
//   xhr.send(formData);
// });