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
    preview.pause();
    // style update
    target.classList.remove('fa-stop');
    target.classList.add('fa-play');
    target.removeAttribute('id');
}

const playPreview = (i, isUpdated=false) => {
    clearTimeout(pauseTimeout);
    clearTimeout(effectTimeout);
    const prevPlayBtn = document.getElementById('playing');
    const playBtn = document.getElementById(`play-${i}`).querySelector("i");
    if (prevPlayBtn)
        pause(preview, prevPlayBtn);
    // 이전 영상 정지
    if (!isUpdated){
        if (playBtn === prevPlayBtn)
            return ;
    }
    // 데이터 가져오기
    const position = document.getElementById(`position-${i}`).querySelector("input[type=radio]:checked").value;
    const time = timeList[i];
    const source = sourceList[effectList[i]];
    const duration = time.sentence.end - time.sentence.start;
    const offset = time.offset[position];
    // 영상 재생
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
document.querySelectorAll(".select-position").forEach(radio => radio.addEventListener("click", function(){
    // console.log(this);
    const position = this.querySelector("input[type=radio]:checked");
    i = position.dataset.idx;
    updateTime(i, position.value);
    playPreview(i, true);
}));

// LI : update style
document.querySelectorAll("#sentence-list li").forEach(li => li.addEventListener("click", function(){
    currentIdx = this.dataset.idx;
    console.log(currentIdx);
    const prevSelected = document.getElementById("selected");
    if (!li.id){
        li.id = "selected";
        console.log('추가');
    }
    if (prevSelected) prevSelected.removeAttribute("id");
}));

// TEXT : update style
document.querySelectorAll(".text").forEach(text => text.addEventListener("click", function(){
    const li = this.closest("li");
    // if (li.id){
    //     console.log('해제');
    //     li.removeAttribute("id");
    // }
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
    const effectData = JSON.parse(data);
    const short = document.querySelector('#short-effect > ul');
    const long = document.querySelector('#long-effect > ul');
    loadEffectContainer(short, effectData.short);
    loadEffectContainer(long, effectData.long);
}

function loadEffectContainer(parent, effectCategory){
    const container = document.createElement("li");
    const items = document.createElement("ul");
    container.className = "effect-container";
    items.className = "effect-items";

    for (let effect of Object.keys(effectCategory))
        loadEffectItems(items, effectCategory[effect]);

    container.appendChild(items);
    parent.appendChild(container);
}


function loadEffectItems(parent, effects){
    for (let i in effects){
        const li = document.createElement("li");
        const radio = document.createElement("input");
        const label = document.createElement("label");
        
        li.className = "effect-item";

        // [TODO] : li 안에 radio로 바꾸기, name은 다 같게
        li.innerText = effects[i].name;
        li.addEventListener("click", () => {
            const currentEffect = effects[i].index;
            const currentSource = sourceList[currentEffect];
            if (currentIdx){
                updateEffect(currentEffect);
                playPreview(currentIdx, true);
            } else
                currentSource.play();
        });

        // li.appendChild(radio);
        // li.appendChild(label);
        parent.appendChild(li);
    }
}