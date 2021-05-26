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
    const current_audio = document.getElementById('current_audio');
    
    for (let i=0; i<sentenceList.length; i++){
        const li = liList[i];
        sentenceList[i].addEventListener("click", () => { 
            currentIdx = i;
            // if(exportEffectList[currentIdx]!== undefined){
            //     current_audio.innerText = currentIdx+" - "+exportEffectList[currentIdx];
            // }
            // else{
            //     current_audio.innerText = currentIdx+" - "+"효과음없음"
            // } 
            time = getTimeData();

            //선택된 리스트
            if (li.classList.contains("selected")){
                currentIdx = null;
                li.classList.remove("selected");
            } else {
                for (let i=0; i<liList.length; i++)
                    liList[i].classList.remove("selected");
                li.classList.add("selected");
            }
            console.log(currentIdx);
        });
    }
}

function removeEffect(idx){
    //export리스트의 인덱스요소를 삭제
    //어차피 뒤에서 export할 때 리스트빈거면 없애주는 filter함
    delete exportEffectList[idx]; 
    delete exportTimeList[idx] 
    console.log(exportEffectList, exportTimeList);

    const current_audio = document.getElementById('current_audio');
    current_audio.innerText = "효과음이 삭제되었습니다."

    const selected_sentence = document.querySelectorAll("#sentence-list > li");
    sentence_remove = selected_sentence[currentIdx];
    sentence_remove.classList.add("audio_removed");
    sentence_remove.classList.remove("audio_selected");
}

function setEffectEvent(effectAudio){
    const position = document.querySelector('.select-position input:checked').value;
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
        const audio = document.getElementById(effectList[i].index);
        
        li.className = "effect-item";
        li.innerText = effectList[i].name;
        li.addEventListener("click", () => {
            if (currentIdx !== undefined){
                currentEffect = effectList[i].index;
                setEffectEvent(audio);
                // const selected_sentence = document.querySelectorAll("#sentence-list li");
                // sentence_add = selected_sentence[currentIdx];
                // sentence_add.classList.remove("audio_removed");
                // sentence_add.classList.add("audio_selected");
                // if(exportEffectList[currentIdx]!== undefined){
                //     current_audio.innerText = currentIdx+" - "+exportEffectList[currentIdx];
                // }
                // else{
                //     current_audio.innerText = currentIdx+" - "+"효과음없음"
                // }
            } else {
                audio.play;
            }
        })

        parent.appendChild(li);
    }
}