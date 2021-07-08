document.querySelector('#play').onclick = play;
document.querySelector('#pause').onclick = pause;
document.querySelector('#speed-up').onclick = speedUp;
document.querySelector('#speed-down').onclick = speedDown;
document.querySelector('#volume').oninput = volume;


let video = document.querySelector('#video-player');
let progress = document.querySelector('#progress');

video.ontimeupdate = progressUpdate;

progress.onclick = videoRewind;

function play() {
    video.play();
}

function pause() {
    video.pause();
}

function speedUp() {
    video.play();
    video.playbackRate = 1.25;
    
}

function speedDown() {
    video.play();
    video.playbackRate = 1;
}

function volume() {
    let v = this.value;
    console.log(v);
    video.volume = v / 100;
}

function progressUpdate() {
    let d = video.duration;
    let c = video.currentTime;
    progress.value = (100 * c) / d;
}

function videoRewind() {
    let w = this.offsetWidth;
    let o = event.offsetX;
    // console.log(video.duration)
    // console.log(video.currentTime);
    // console.log(w)
    // console.log(o)
    this.value = 100 * o / w;
    console.log(video.duration * (o / w));
    video.pause();
    video.currentTime = video.duration * (o / w);
    video.play();
    // console.log(video.currentTime)
    // console.log(video.duration)
}