// for control
let currentIdx;
let pauseTimeout;
let effectTimeout;
// html obj
const sourceList = document.querySelectorAll("audio");
const preview = document.querySelector("video");


// ===============
// # MAIN FUNCTION
// ===============
//  UPDATE DATA
const updateTime = (i, position) => { 
    exportTime[i] = timeList[i].keyword[position]
};

const updateEffect = (effectIdx) => {
    // data update
    exportEffect[currentIdx] = effectIdx;
    // style update : effect true
    const effect = document.getElementById(`effect-${currentIdx}`).querySelector(".effect");
    if (effect.classList.contains('empty'))
        effect.classList.remove('empty');
    // style update : effect name
    const name =  effect.querySelector('.name');
    name.innerText = effectIdx+ '.' + effectList[effectIdx];
};

const removeEffect = (i) => {
    delete exportEffect[i]; 
    delete exportTime[i];
    // style update
    const effect = document.getElementById(`effect-${i}`).querySelector(".effect");
    const name =  effect.querySelector('.name');
    effect.classList.add('empty');
    name.innerText = "효과음을 추가하세요";
}

// PREVIEW
const play = (preview, target, start) => {
    preview.currentTime = start;
    preview.play();
    // style update
    target.classList.remove('fa-play');
    target.classList.add('fa-stop');
    target.id = 'playing';
}

const pause = (preview, target) => {
    clearTimeout(pauseTimeout);
    clearTimeout(effectTimeout);
    preview.pause();
    // style update
    target.classList.remove('fa-stop');
    target.classList.add('fa-play');
    target.removeAttribute('id');
}

const playPreview = (i, replay=false) => {
    // 이전 영상 정지
    const prevPlayBtn = document.getElementById('playing');
    const playBtn = document.getElementById(`play-${i}`).querySelector("i");
    if (prevPlayBtn)
        pause(preview, prevPlayBtn);
    if (!replay && playBtn === prevPlayBtn) // 효과음, 위치 업데이트 아닐 시 그대로 정지
        return ;
    // 영상 재생
    const position = document.getElementById(`position-${i}`).querySelector("input[type=radio]:checked").value;
    const time = timeList[i];
    const source = sourceList[effectList[i]];
    const duration = time.sentence.end - time.sentence.start;
    const offset = time.offset[position];
    play(preview, playBtn, time.sentence.start / 1000); // 영상 재생 : millisec -> sec
    if (source)
        effectTimeout = setTimeout(() => source.play(), offset); // 효과음 재생
    pauseTimeout = setTimeout(() => pause(preview, playBtn), duration); // 영상 정지
}

// EXPORT
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


// ===============
// # EVENT BINDING
// ===============
// POSITION : update time
document.querySelectorAll(".select-position input[type=radio]").forEach(radio => radio.addEventListener("click", function(){
    // console.log(this);
    if (this.checked == true){
        i = this.dataset.idx;
        updateTime(i, this.value);
        playPreview(i, true);
    }
}));

// LI : update style
document.querySelectorAll("#sentence-list li").forEach(li => li.addEventListener("click", function(event){
    currentIdx = this.dataset.idx;
    const prevSelected = document.getElementById("selected");
    const prevPlayBtn = document.getElementById("playing");

    if (prevSelected && event.target == prevSelected.querySelector(".text")){
        // .text 클릭 시 선택 해제
        li.removeAttribute("id");
        pause(preview, prevPlayBtn);
    }
    else {
        // 이전 선택 해제
        if (prevSelected)
            prevSelected.removeAttribute("id");
        // 이전 재생 정지
        if (prevPlayBtn && prevPlayBtn.closest("li") != this)
            pause(preview, prevPlayBtn);
        // 선택 스타일  추가
        li.id = "selected";

    }
}));

// PLAY : play preview
document.querySelectorAll(".play").forEach(play => play.addEventListener("click", function(){
    playPreview(this.dataset.idx);
}));

// REMOVE : remove effect
document.querySelectorAll(".remove-btn").forEach(rmBtn => rmBtn.addEventListener("click", function(){
    // console.log(this.dataset.idx);
    removeEffect(this.dataset.idx);
}))


// ===============
// # EFFECT LIB LOADING
// ===============

function loadEffect(data) {
    // const short = document.querySelector('#short-effect > ul');
    // const long = document.querySelector('#long-effect > ul');
    const effectLib = document.getElementById('effect-lib');
    for (category in data){
        const categoryItem = document.createElement("li");
        const title = document.createElement("h4");
        const effectList = document.createElement("ul");

        title.innerText = category;
        effectList.className = "effect-container";

        categoryItem.appendChild(title);
        categoryItem.appendChild(effectList);
        effectLib.appendChild(categoryItem);

        for (effect in data[category]) {
            const effectIdx = data[category][effect].index;
            const effectItem = document.createElement("li");
            const effectInput = document.createElement("input");
            const effectLabel = document.createElement("label");
            
            // update input
            effectInput.type = "radio";
            effectInput.className = "hide";
            effectInput.id = `lib-${data[category][effect].index}`;
            effectInput.name = "effect";

            // update label
            effectLabel.htmlFor = effectInput.id;
            effectLabel.innerText = data[category][effect].name;
            effectLabel.addEventListener("click", function() {
                const currentSource = sourceList[effectIdx];
                if (currentIdx){
                    updateEffect(effectIdx);
                    // console.log(currentSource);
                    playPreview(currentIdx, true);
                } else
                    currentSource.play();
                    // console.log(currentSource);
            });

            // update effectItem
            effectItem.className = "effect-item";
            effectItem.appendChild(effectInput);
            effectItem.appendChild(effectLabel);

            // update effectList
            effectList.appendChild(effectItem);
        }
    }
}