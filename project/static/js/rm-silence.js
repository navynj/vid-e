// ================
// SPLIT
// ================
const createRadio = (tdb) => {
    // 동일값 존재하면 false 반환
    if (document.getElementById(`${tdb}-radio`))
        return false;
    // 라디오 정의 [value: tdb, display: none]
    const radio = document.createElement('input');
    radio.type = "radio";
    radio.name = "tdb";
    radio.id = `${tdb}-radio`;
    radio.value = tdb;
    radio.className = "hide";
    radio.checked = false;
    // 라벨 정의 [click : update_waveform]
    const label = document.createElement('label');
    label.id = `${tdb}-label`;
    label.htmlFor = radio.id;
    label.innerText = `${tdb}dB`;
    label.classList.add("processing");
    // 폼에 현재 라디오+라벨 추가
    const list = document.getElementById('split-output-list');
    const li = document.createElement("li");
    li.appendChild(radio);
    li.appendChild(label);
    list.appendChild(li);
    return true;
}

const updateRadio = (tdb) => {
    // 라디오 선택 상태 초기화
    const radios = document.getElementsByName("tdb");
    for(let i=0; i<radios.length; i++)
      if(radios[i].checked)
        radios[i].checked = false;
    // 현재 라디오 선택 처리
    const radio = document.getElementById(`${tdb}-radio`);
    radio.checked = true;
}

const updateLabel = (tdb, intervals) => {
    // 라벨 클래스 업데이트
    const radio = document.getElementById(`${tdb}-radio`);
    const label = document.getElementById(`${tdb}-label`);
    radio.classList.remove("hide");
    label.classList.remove("processing");
    // waveform 업데이트
    label.addEventListener('click', (e)=>{
        updateWaveform(intervals);
        resultOn(intervals);
    });
    updateWaveform(intervals);
    resultOn(intervals);
}

const postJson = (json_data) => {
    return {
        method: 'POST',
        headers: { 'Content-Type' : 'application/json' },
        body : JSON.stringify(json_data)
    }
}

const tdbSplit = url => {
    const tdb = document.getElementById("tdb-input").value;
    if (createRadio(tdb)){
        fetch( url, postJson({ 'tdb' : tdb }) )
        .then( res => { return res.json() } )
        .then( data => {
            updateRadio(tdb);
            updateLabel(tdb, data.intervals);
        })
        .catch( error => { console.log(error) } )
    }
    else updateRadio(tdb);
};