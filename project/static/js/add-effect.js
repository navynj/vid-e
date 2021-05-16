// ===================
// # 효과음 추가, 내보내기
// ===================
function getTimeData() {
    // 전역변수 sentences, currentIdx
    // sentence
    const sentenceStart = sentences[currentIdx]['time']['sentence']['start'];
    const sentenceEnd = sentences[currentIdx]['time']['sentence']['end'];
    // keyword
    const keywordStart = sentences[currentIdx]['time']['keyword']['start'];
    const keywordEnd = sentences[currentIdx]['time']['keyword']['end'];
    // effect
    const effectTimeFront = keywordStart - sentenceStart;
    const effectTimeBack = keywordEnd - sentenceStart;
    return {
        'sentence' : {
            'start' : sentenceStart,
            'end' : sentenceEnd
        },
        'keyword' : {
            'start' : keywordStart,
            'end' : keywordEnd
        },
        'effect' : {
            'start' : effectTimeFront,
            'end' : effectTimeBack
        }
    }
}

function setSentenceEvent() {
    for (let i in sentenceList){
        const sentence = sentenceList[i];
        sentence.addEventListener("click", () => { 
            currentIdx = i;
            time = getTimeData();

            // 선택된 리스트
            if (sentence.classList.contains("selected")){
                sentence.classList.remove("selected");
            } else {
                sentence.classList.add("selected");
            }
        });
    }
}

function setEffectEvent(effectAudio){
    const position = document.querySelector('#select-position > input:checked').value;
    if (time){
        const duration = time.sentence.end - time.sentence.start;
        const offset = time.effect[position];
        const exportTime = time.keyword[position];

        // 영상 미리보기 재생
        preview.currentTime = time.sentence.start / 1000; // millisec -> sec
        preview.play(); // 영상 재생
        setTimeout(() => effectAudio.play(), offset); // 효과음 재생
        setTimeout(() => preview.pause(), duration); // 영상 일시정지

        // export 전역변수 업데이트
        exportEffectList[currentIdx] = effectList[currentEffect];
        exportTimeList[currentIdx] = exportTime;
    }
}

const exportResult = (url) => {
    const data  = {
        'effect_list' : exportEffectList.filter(()=>{ return true }),
        'time_list' : exportTimeList.filter(()=>{ return true })
    };
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
// # 효과음 라이브러리 패널 업데이트
// ===============
function loadEffect(data) {
    const effectData = JSON.parse(data);
    const short = document.querySelector('#short-effect > ul');
    const long = document.querySelector('#long-effect > ul');
    addEffectContainer(short, effectData.short);
    addEffectContainer(long, effectData.long);

}

function addEffectContainer(parent, effectCategory){
    const container = document.createElement("li");
    const items = document.createElement("ul");
    container.className = "effect-container";
    items.className = "effect-items";

    for (let effect of Object.keys(effectCategory))
        addEffectItems(items, effectCategory[effect]);

    container.appendChild(items);
    parent.appendChild(container);
}

function addEffectItems(parent, effectList){
    for (let i in effectList){
        const li = document.createElement("li");
        const btn = document.createElement("button");
        const bg = document.createElement("div");
        const audio = document.getElementById(effectList[i].index);
        btn.className = "effect-btn";
        btn.innerHTML = '<i class="fas fa-play"></i>';
        btn.addEventListener("click", () => {
            audio.play();
        });
        
        bg.className = "effect-bg";
        bg.innerText = effectList[i].name;
        bg.addEventListener("click", () => {
            currentEffect = effectList[i].index;
            setEffectEvent(audio);
        })
        
        li.appendChild(btn);
        li.appendChild(bg);
        parent.appendChild(li);
    }
}