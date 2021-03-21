// wavesurfer.js
const load_waveform = path => {
    // console.log(path);

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
    
    // 구역 설정 : waveserfer.js regions 라이브러리로 불러온 addRegion
    wavesurfer.on('ready', function () {
        // Enable creating regions by dragging
        wavesurfer.enableDragSelection({});
      
        // Add a couple of pre-defined regions
        wavesurfer.addRegion({
          start: 2, // time in seconds
          end: 5, // time in seconds
          color: 'hsla(100, 100%, 30%, 0.1)'
        });
        
        wavesurfer.addRegion({
          start: 8,
          end: 14,
          color: 'hsla(200, 100%, 30%, 0.1)'
        });
        
        wavesurfer.addRegion({
          start: 28,
          end: 36,
          color: 'hsla(400, 100%, 30%, 0.1)'
        });
      });
}

