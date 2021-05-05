// wavesurfer.js


let wavesurfer = WaveSurfer.create({
    container: '#waveform',
    progressColor: '#444444',
    cursorColor: 'transparent',
    waveColor: '#C8C8C8',
    hideScrollbar: false,
    height: 180, // 파형출력공간 높이
    barWidth: 1, // 가로 네모 너비
    normalize: true // max값을 제일 높은 바로 크기 조정
});

const load_waveform = path => {
    // load audio
    wavesurfer.load(path);
    // play button click
    play = document.getElementById('play');
    play.addEventListener('click', function() {
        wavesurfer.playPause();
        const icon_classList = this.firstElementChild.classList;
        if (icon_classList.contains("fa-play")) {
            icon_classList.remove("fa-play");
            icon_classList.add("fa-pause");
        } else {
            icon_classList.remove("fa-pause");
            icon_classList.add("fa-play");
        }
    });
    // skip mute regions
    wavesurfer.on('region-in', function (region) {
        let duration = region.end - region.start;
        wavesurfer.skip(duration);
    });
    
}

const update_waveform = (sr, intervals) => {
    // set non-mute-intervals to mute-intervals
    wavesurfer.clearRegions();
    for (i=0; i<intervals.length-1; i+=2){
        wavesurfer.addRegion({
            start: intervals[i],
            end: intervals[i+1],
            color: 'hsla(30, 30%, 30%, 0.15)',
            drag: false,
            resize: false
        });
    }
}