const songs=document.getElementById("right_cnt");
const song_button=document.getElementById("song_btn");

function updateHeading(headingNumber) {
    const dropdown = document.getElementById(`dropdown${headingNumber}`);
    const heading = document.getElementById(`heading${headingNumber}`);
    const selectedSong = dropdown.value;
    
    heading.textContent = selectedSong !== '' ? selectedSong : `Default Heading ${headingNumber}`;
}
  

song_button.onclick=unblock;

function unblock(){
    songs.style.display="block";
}


