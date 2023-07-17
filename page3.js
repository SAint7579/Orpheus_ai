// const { time } = require("@amcharts/amcharts5");


var mySong=document.getElementById("song");
var icon= document.getElementById("play");
var star1=document.getElementById("star1");
// var star2=document.getElementById("star2");
// var star3=document.getElementById("star3");
// var star4=document.getElementById("star4");
// var star5=document.getElementById("star5");



var next=document.getElementById("next");

var thumbnail=document.getElementById("song_thumbnail");

icon.onclick= playpause;


var play_time=0
var startTime=0
var endTime=0   


function playpause(){
    
    if(mySong.paused){
        const audioUrl = mySong.src;

        // Generate a unique cache-busting query parameter
        const cacheBuster = new Date().getTime();

        // Append the cache-buster to the audio URL
        const updatedAudioUrl = audioUrl + '?v=' + cacheBuster;

        mySong.src = updatedAudioUrl;
        mySong.play();
        
        icon.src="images/pause.png";
        startTime = new Date();
    }
    else{
        mySong.pause();
        icon.src="images/play.png";
        endTime = new Date();
        play_time = endTime - startTime;
        play_time=play_time/1000
    }
    mySong.addEventListener("ended", function() {
      icon.src = "images/play.png";
    });
}


var rating_number=0;
function rate(starIndex) {
    var stars = document.getElementById('rating').getElementsByTagName('img');
    
    for (var i = 0; i < stars.length; i++) {
      if (i < starIndex) {
        stars[i].src = 'images/filled_star.png';
        rating_number++;
      } else {
        stars[i].src = 'images/empty_star.png';
      }
    }
    
      
}

// store the name of all the songs selected and pass it to the python script for generating music

const song1_name=localStorage.getItem('song1');
const song2_name=localStorage.getItem('song2');
const song3_name=localStorage.getItem('song3');
const similarity=localStorage.getItem('slidervalue');

function changeSong(){
  thumbnail.src="images/loading.gif";

  if (mySong.paused){}
  else{
      mySong.pause();
      icon.src="images/play.png";
  }
 
  const params = new URLSearchParams();
  params.append('param1', song1_name);
  params.append('param2', song2_name);
  params.append('param3', song3_name);
  params.append('param4', similarity);

  

  fetch(`http://localhost:3000/trigger-python?${params.toString()}`)
      .then(response => response.text())
      .then(data => console.log(data))
      .catch(error => console.error(error));

  // location.reload(true);
    
}



// Generate a random integer between min (inclusive) and max (inclusive)

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
  
// Usage example: Generate a random integer between 1 and 10
var randomNum = getRandomInt(1, 10);

// async function loadImageFromPath(path) {
//     const response = await fetch(path);
//     const arrayBuffer = await response.arrayBuffer();
//     const bytes = new Uint8Array(arrayBuffer);
//     const bytea = bytes.reduce((acc, byte) => acc + '\\' + byte.toString(8), '');
//     return bytea;
// }  


function loadImageFromPath(imagePath) {
    return new Promise((resolve, reject) => {
      fetch(imagePath)
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to load the image file.');
          }
          return response.arrayBuffer();
        })
        .then(arrayBuffer => {
          const byteArray = new Uint8Array(arrayBuffer);
          const byteaString = byteArray.reduce((data, byte) => data + String.fromCharCode(byte), '');
          resolve(byteaString);
        })
        .catch(error => {
          reject(error);
        });
    });
  }
function useByteaData(byteaData) {
    // Use the bytea data here or perform other operations
    console.log(byteaData);
    return byteaData;
}
// for inserting ratings into database
document.addEventListener("DOMContentLoaded", function() {
    var insertButton = document.getElementById("insertButton");

    insertButton.addEventListener("click", function() {
        var value1 = randomNum;  // Replace with your desired value
        var value2 = rating_number;
        var value3 = play_time;  // Replace with your desired value
        const imagePath = 'audio/thumbnail.png'; // Replace with the actual file path
        var convertedBytea;
        loadImageFromPath(imagePath)
        .then(bytea => {
            convertedBytea = bytea;
            // Here, you can access and use the convertedBytea variable as needed
            console.log(convertedBytea);
        })
        .catch(error => {
            console.error(error);
        });
        console.log(convertedBytea); // Replace with the path to your .png file
        
        
        
        // Create a new XMLHttpRequest object
        var xhr = new XMLHttpRequest();

        // Set the request URL
        xhr.open("POST", "http://localhost:3000/insert", true);  // Replace with your server-side endpoint

        // Set the request headers
        xhr.setRequestHeader("Content-Type", "application/json");

        // Handle the response from the server
        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log(xhr.responseText);
            } else {
                console.error("Error: " + xhr.status);
            }
        };

        // Handle any errors that occur during the AJAX request
        xhr.onerror = function() {
            console.error("Request failed.");
        };
        
        // Send the data to the server
        var data = {
            value1: value1,
            value2: value2,
            value3: value3,
            value4: convertedBytea
        };
        xhr.send(JSON.stringify(data));
    });
});

// playing
var pp=document.getElementById("pp");
function idk(){
  const song1=localStorage.getItem('slidervalue');
  pp.textContent=song1;
}
 

