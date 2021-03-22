// wavesurfer.js


let wavesurfer = WaveSurfer.create({
    container: '#waveform',
    progressColor: '#444444',
    cursorColor: 'transparent',
    waveColor: '#C8C8C8',
    hideScrollbar: false,
    height: 80, // 파형출력공간 높이
    barWidth: 1, // 가로 네모 너비
    normalize: true // max값을 제일 높은 바로 크기 조정
    // 플러그인은 왜인지 에러가 뜬다..
    // plugins: [
    //     // WaveSurfer.regions.create({}),
    //     // WaveSurfer.timeline.create({
    //     //     container: '#wave-timeline'
    //     // })
    //     // WaveSurfer.cursor.create({
    //     //     showTime: true,
    //     //     opacity: 1,
    //     //     customShowTimeStyle: {
    //     //         'background-color': '#000',
    //     //         color: '#fff',
    //     //         padding: '2px',
    //     //         'font-size': '10px'
    //     //     }
    //     // })
    // ]
});

const load_waveform = path => {

    wavesurfer.load(path);

    var analyser = wavesurfer.backend.analyser,
    frequencyData = new Uint8Array(analyser.frequencyBinCount),
    play = document.getElementById('play');

    //play button click
    play.addEventListener('click', function() {
        wavesurfer.playPause();
        if (this.textContent === 'Play') {
        this.textContent = "Pause";
        } else {
        this.textContent = "Play";
        }
    });

    wavesurfer.on('audioprocess', function(e) {
        analyser.getByteFrequencyData(frequencyData);
        var w = frequencyData[0] * 0.05;
    });

    wavesurfer.on('ready', function () {
    });
    
}

const mute_region = (sr, intervals, tdb) => {
    // set non-mute-intervals to mute-intervals
    console.log(tdb)
    wavesurfer.clearRegions();
    for (i=0; i<intervals.length-1; i+=2){
        wavesurfer.addRegion({
            start: intervals[i]/sr, // time in seconds
            end: intervals[i+1]/sr, // time in seconds
            color: 'hsla(30, 30%, 30%, 0.1)'
          });
  }
}