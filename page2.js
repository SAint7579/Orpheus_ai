const songs=document.getElementById("right_cnt");
const song_button=document.getElementById("song_btn");

song_button.onclick=unblock;

function unblock(){
    songs.style.display="block";
}


