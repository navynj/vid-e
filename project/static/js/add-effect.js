// for control
let currentIdx;
// html obj
const sourceList = document.querySelectorAll("audio");
const preview = document.querySelector("video");


// ===============
// # MAIN FUNCTION
// ===============
const updateTime = (i, position) => { 
    exportTime[i] = timeList[i].keyword[position]
};
const updateEffect = (i, effectIdx) => {
    // data update
    exportEffect[i] = effectList[effectIdx];
    // style update : effect true
    const effect = liList[currentIdx].querySelector(".effect");
    if (effect.classList.contains('empty'))
        effect.classList.remove('empty');
    // style update : effect name
    const name =  effect.querySelector('.name');
    name.innerText = effectIdx+ '.' + effectList[effectIdx];
};
const removeEffect = (i) => {
    delete exportEffect[i]; 
    delete exportTime[i];
}

const play = (preview, target, start) => {
    preview.currentTime = start;
    preview.play();
    target.classList.remove('fa-play');
    target.classList.add('fa-stop');
    target.id = 'playing';
}
const pause = (preview, target) => {
    preview.pause();
    target.classList.remove('fa-stop');
    target.classList.add('fa-play');
    target.removeAttribute('id');
}

const playPreview = (i) => {
    // 이전 영상 정지
    const prevPlay = document.getElementById('#playing');
    if(prevPlay) pause(prePlay);
    // 데이터 가져오기
    const btn = document.getElementById(`play-${i}`);
    const position = document.getElementById(`position-${i}`).querySelector("input[type=radio]:checked").value;
    const time = timeList[i];
    const source = sourceList[effectList[i]];
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

// ===============
// # EVENT BINDING
// ===============
// POSITION : update time
document.querySelectorAll(".select-position").forEach(radio => radio.addEventListener("click", function(){
    // console.log(this);
    const position = this.querySelector("input[type=radio]:checked");
    i = position.dataset.idx;
    updateTime(i, position.value);
}));
// TEXT : update style
document.querySelectorAll(".text").forEach(text => text.addEventListener("click", function(){
    const li = this.closest("li");
    if (li.classList.contains("selected")){
        currentIdx = null;
        li.classList.remove("selected");
    } else {
        const prevSelected = this.closest("#sentence-list").querySelector("li.selected");
        if (prevSelected) prevSelected.classList.remove("selected");
        li.classList.add("selected");
    }
}))
// PLAY : play preview
document.querySelectorAll(".play").forEach(play => play.addEventListener("click", function(){
    playPreview(this.dataset.idx);
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
        
        li.className = "effect-item";
        li.innerText = effects[i].name;
        li.addEventListener("click", () => {
            const currentEffect = effects[i].index;
            const currentSource = sourceList[currentEffect];
            if (currentIdx){
                updateEffect(i, currentEffect);
                playPreview(i);
            } else {
                currentSource.play();
            }
        })
        parent.appendChild(li);
    }
}
