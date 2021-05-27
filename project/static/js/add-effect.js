// for control
let currentIdx;
// html obj
const radioList = document.querySelectorAll(".select-position input[type=radio]");
const sourceList = document.querySelectorAll("audio");
const preview = document.querySelector("video");

// MAIN FUNCTION
const updateTime = (i, position) => { 
    console.log('update: ', i, position);
    exportTime[i] = timeList[i].keyword[position]
};
const updateEffect = (i, effectIdx) => { exportEffect[i] = effectList[effectIdx] };
const removeEffect = (i) => {
    delete exportEffect[i]; 
    delete exportTime[i];
}

const play = (preview, target, start) => {
    preview.currentTime = start;
    preview.play();
    play.classList.remove('fa-play');
    play.classList.add('fa-stop');
    target.id = 'playing';
}
const pause = (preview, target) => {
    preview.pause();
    target.classList.remove('fa-stop');
    target.classList.add('fa-play');
    target.removeAttribute('id');
}

const playPreview = (i, position) => {
    // 이전 영상 정지
    const prevPlay = document.getElementById('#playing');
    if(prevPlay) pause(prePlay);
    // 데이터 가져오기
    const btn = playBtn[i];
    const time = timeList[i];
    const source = sourceList[EffectList[i]];
    // 시간 데이터
    const duration = time.sentence.start - time.sentence.start;
    const offset = time.offset[position];
    // 영상 재생 : millisec -> sec
    play(preview, btn, time.sentence.start / 1000);
    // 효과음 재생
    if (source) setTimeout(() => source.play(), offset);
    // 영상 정지
    setTimeout(pause(preview, btn), duration);
}

const exportResult = (url) => {
    // filter data
    const data  = {
        'time_list' : exportTime.filter( item => exportEffect[exportTime.indexOf(item)] ),
        'effect_list' : exportEffect.filter( item => item )
    };
    // fetch data
    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type' : 'application/json' },
        body : JSON.stringify(data)
    })
    .then( response => { 
        if (response.redirected)
            window.location.href = response.url;
    });
}

// EVENT BIDNING
// click SENENCE : update currentIdx
radioList.forEach(sentence => sentence.addEventListener("click", function(){
    // console.log(this);
    const position = this.querySelector("input[type=radio]:checked");
    currentIdx = position.dataset.idx;
    console.log(currentIdx, position.value);
    updateTime(currentIdx, position.value);
}));

// click effect
// 업데이트 - effectList

// click play -  playpause preview

// click text - remove style(selected)

// click position
// 업데이트 - timeList


// LOAD EFFECT
function loadEffect(data) {
    const effectData = JSON.parse(data);
    const short = document.querySelector('#short-effect > ul');
    const long = document.querySelector('#long-effect > ul');
    // loadEffectContainer(short, effectData.short);
    // loadEffectContainer(long, effectData.long);
}