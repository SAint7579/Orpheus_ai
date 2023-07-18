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
