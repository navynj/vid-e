// ================
// SPLIT
// ================
const create_radio = (tdb) => {
    // 동일값 존재하면 false 반환
    if (document.getElementById(`${tdb}-radio`))
        return false;
    // 라디오 정의 [value: tdb, display: none]
    const radio = document.createElement('input');
    radio.type = "radio";
    radio.name = "tdb";
    radio.id = `${tdb}-radio`;
    radio.value = tdb;
    radio.checked = false;
    radio.classList.add("hide");
    // 라벨 정의 [click : update_waveform]
    const label = document.createElement('label');
    label.id = `${tdb}-label`;
    label.htmlFor = radio.id;
    label.innerText = tdb;
    label.classList.add("processing");
    // 폼에 현재 라디오+라벨 추가
    const form = document.getElementById('split-outputs');
    form.appendChild(radio);
    form.appendChild(label);
    return true;
}

const update_radio = (tdb) => {
    // 라디오 선택 상태 초기화
    const radios = document.getElementsByName("tdb");
    for(let i=0; i<radios.length; i++)
      if(radios[i].checked)
        radios[i].checked = false;
    // 현재 라디오 선택 처리
    const radio = document.getElementById(`${tdb}-radio`);
    radio.checked = true;
}

const update_label = (tdb, sr, intervals) => {
    // 라벨 클래스 업데이트
    const label = document.getElementById(`${tdb}-label`);
    label.classList.remove("processing");
    label.classList.add("complete");
    // // waveform 업데이트
    // label.addEventListener('click', (e)=>update_waveform(sr, intervals));
    // update_waveform(sr, intervals);
}

const post_json = (json_data) => {
    return {
        method: 'POST',
        headers: { 'Content-Type' : 'application/json' },
        body : JSON.stringify(json_data)
    }
}

const tdb_split = url => {
    const tdb = document.getElementById("tdb-input").value;
    if (create_radio(tdb)){
        fetch( url, post_json({ 'tdb' : tdb }) )
        .then( res => { return res.json() } )
        .then( data => {
            update_radio(tdb);
            update_label(tdb, data.sr, data.intervals);
        })
        .catch( error => { console.log(error) } )
    }
    else update_radio(tdb);
};

// ================
// EXPORT
// ================
const export_result = url => {
    fetch( url, { 
        method: 'POST',
        headers: { 'Content-Type' : 'application/json' },
        body : { 'tdb' : document.getElementById("tdb-input").value }
    })
    .then( res => { return res.json() } )
    .then( data => { console.log(data) } )
    .catch( error => { console.log(error) } )
};