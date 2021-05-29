// ================
// WAVEFORM
// ================
let wavesurfer = WaveSurfer.create({
    container: '#waveform',
    progressColor: '#5278FF',
    cursorColor: 'transparent',
    waveColor: '#C8C8C8',
    hideScrollbar: false,
    height: 200, // 파형출력공간 높이
    barWidth: 1, // 가로 네모 너비
    normalize: true, // max값을 제일 높은 바로 크기 조정
    backend: 'MediaElement' // 비디오 preview와 연동
});

const playPause = () => {
    // playpause
    wavesurfer.playPause();
    // play button style
    play = document.getElementById('play');
    const icon_classList = play.firstElementChild.classList;
    if (icon_classList.contains("fa-play")) {
        icon_classList.remove("fa-play");
        icon_classList.add("fa-pause");
    } else {
        icon_classList.remove("fa-pause");
        icon_classList.add("fa-play");
    }
}


const loadWaveform = () => {
    // load audio
    const video = document.getElementById('video');
    wavesurfer.load(video);
    // play button event binding
    play.addEventListener('click', () => playPause());
    document.addEventListener('keydown', function(e) {
        if (e.code === "Space" || e.keyCode === 32)
            playPause();
    }); 
    // skip mute regions
    wavesurfer.on('region-in', function (region) {
        let duration = region.end - region.start;
        wavesurfer.skip(duration);
    });
}

const updateWaveform = (intervals) => {
    // set non-mute-intervals to mute-intervals
    wavesurfer.clearRegions();
    var mute_total_time = 0;
    for (i=0; i<intervals.length-1; i+=2){
        mute_total_time += intervals[i+1]-intervals[i];
        wavesurfer.addRegion({
            start: intervals[i],
            end: intervals[i+1],
            color: '#5278FF33',
            drag: false,
            resize: false
        });
    }
}

// ================
// RESULT DURATION
// ================
const showDuration = (intervals) =>{
    var totalMute = 0;
    const duration = document.getElementById('video').duration;
    const percent = document.getElementById('percent');
    const silenceDuration = document.getElementById('silence-duration');
    const removedDuration = document.getElementById('output-duration');

    //무음구간 시간계산
    for (i=0; i<intervals.length-1; i+=2)
        totalMute += intervals[i+1]-intervals[i];
    var minute = parseInt(totalMute / 60);
    var second = Math.round(totalMute % 60);
    var total = duration - totalMute;
  
    percent.innerText = Math.round((totalMute/duration)*100)+"%";
    silenceDuration.innerText = `${minute}분  ${second}초`;
    removedDuration.innerText = `${parseInt(total / 60)}분 ${parseInt(total % 60)}초`;
}