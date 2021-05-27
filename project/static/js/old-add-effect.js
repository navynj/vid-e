// ===================
// # 효과음 추가, 내보내기
// ===================
// [처리] 시간 데이터

// [클릭]
function setSentenceEvent() {
    for (let i=0; i<liList.length; i++){
        const li = liList[i];
        const sentence = li.querySelector(".sentence");
        const play = li.querySelector(".play");
        const text = li.querySelector(".text");
        const radio = li.querySelector(".select-position");
        const radioList = li.querySelectorAll(".select-position input");
        const removeBtn = li.querySelector(".remove-btn");

        // Li 선택 : update data
        li.addEventListener("click", () => {
            currentIdx = i;
            currentPos = radio.querySelector("input:checked").value;
            time = getTimeData();
            exportTimeList[currentIdx] = time.keyword[currentPos];
            console.log('current', currentIdx, currentPos, effectList[currentEffect]);
        });

        // TEXT 클릭 : toggle style
        text.addEventListener("click", () => {
            if (li.classList.contains("selected")){
                currentIdx = null;
                li.classList.remove("selected");
            } else {
                const prevSelected = document.querySelector("#sentence-list > ol > li.selected");
                if (prevSelected) prevSelected.classList.remove("selected");
                li.classList.add("selected");
            }
        });

        // RADIO 클릭 : only select
        for (let p=0; p<radioList.length; p++){
            radioList[p].addEventListener("click", () => {
                playPreview();
                console.log('current', currentIdx, currentPos, effectList[currentEffect]);
            });
        }

        // PLAY 클릭 : only select
        play.addEventListener("click", () => {    
            // update data
            currentIdx = i;
            // update style
            if (!li.classList.contains("selected")){
                const prevSelected = document.querySelector("#sentence-list > ol > li.selected");
                if (prevSelected) prevSelected.classList.remove("selected");
                li.classList.add("selected");
                playPreview();
            } else {
                const prevSelected = document.querySelector("#sentence-list > ol > li.selected");
                if (prevSelected) prevSelected.classList.remove("selected");
                li.classList.add("selected");
                preview.pause();
                const playControl = play.querySelector('i.fa-stop');
                if(playControl){
                    playControl.classList.remove('fa-stop');
                    playControl.classList.add('fa-play');
                }
            }
        });

        // REMOVE : 삭제 버튼
        console.log(i, removeBtn);
        removeBtn.addEventListener("cllick", () => removeEffect(i));

        // HOVER : sentence
        sentence.addEventListener("mouseover", () => {
            li.classList.add("hover");
        })
        sentence.addEventListener("mouseout", () => {
            li.classList.remove("hover");
        })
    }
}

// [기능 1] 효과음 미리듣기
function playPreview(){
    // 이전 영상 정지
    const prevPlay = document.querySelector('#sentence-list .sentence .play i.fa-stop');
    if(prevPlay){
        preview.pause();
        prevPlay.classList.remove('fa-stop');
        prevPlay.classList.add('fa-play');
    }

    // 데이터 가져오기
    time = getTimeData();
    const play = playBtn[currentIdx];
    const duration = time.sentence.end - time.sentence.start;
    const offset = time.effect[currentPos];
    currentSource = sourceList[exportEffectList[currentIdx]];

    // 영상 미리보기 재생
    preview.currentTime = time.sentence.start / 1000; // millisec -> sec
    preview.play();
    play.classList.remove('fa-play');
    play.classList.add('fa-stop');
    // 효과음 재생
    if (currentSource)
        setTimeout(() => currentSource.play(), offset);
    // 영상 정지
    setTimeout(() => {
        preview.pause();
        play.classList.remove('fa-stop');
        play.classList.add('fa-play');
    }, duration);
}

// [기능 2] 효과음 추가
function addEffect(effectIdx) {
    // data update
    exportEffectList[currentIdx] = effectIdx;
    console.log('target', currentIdx, currentPos, effectList[currentEffect].name);
    
    // style update : effect true
    const effect = liList[currentIdx].querySelector(".effect");
    if (effect.classList.contains('empty'))
        effect.classList.remove('empty');
    // style update : effect name
    const name =  effect.querySelector('.name');
    name.innerText = effectIdx+ '.' + effectList[effectIdx];
}

// [기능 3] 효과음 제거
function removeEffect(idx){
    console.log(idx);
    //export리스트의 인덱스요소를 삭제
    //어차피 뒤에서 export할 때 리스트빈거면 없애주는 filter함
    delete exportEffectList[idx]; 
    delete exportTimeList[idx] 
    console.log(exportEffectList, exportTimeList);

    const effect = liList[idx].querySelector(".effect");
    const name =  effect.querySelector('.name');
    if (effect.classList.contains('empty'))
        effect.classList.add('empty');
    name.innerText = "효과음을 추가하세요";
}

// [CLICK] export 버튼
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
            currentEffect = effects[i].index;
            currentSource = sourceList[currentEffect];
            if (currentIdx !== undefined){
                addEffect(currentEffect);
                playPreview();
            } else {
                currentSource.play();
            }
        })
        parent.appendChild(li);
    }
}
