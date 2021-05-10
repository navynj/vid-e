// split - result to html
const create_radio = (tdb) => {
    // 라디오 정의 [value: tdb, display: none]
    const radio = document.createElement('input');
    radio.type = "radio";
    radio.name = "tdb";
    radio.id = `${tdb}`;
    radio.value = `${tdb}`;
    radio.classList.add("hide");
    radio.checked = true;

    // 라벨 정의 [click : update_waveform]
    const label = document.createElement('label');
    label.htmlFor = `${tdb}`;
    label.innerText = `${tdb}`;
    // label.addEventListener('click', (e)=>update_waveform(sr, intervals));

    // 라디오 선택 상태 초기화
    const radios = document.getElementsByName("tdb");
    for(let i=0; i<radios.length; i++)
      if(radios[i].checked)
        radios[i].checked = false;

    // 폼에 현재 라디오+라벨 추가
    const form = document.getElementById('split_outputs');
    form.appendChild(radio);
    form.appendChild(label);
    // // waveform 업데이트
    // update_waveform(sr, intervals);
}

// split - 2) fetch
const tdb_split = url => {
    const tdb = document.getElementById("topdb_input").value;
    fetch( url, { 
        method: 'POST',
        headers: { 'Content-Type' : 'application/json' },
        body : JSON.stringify({ 'tdb' : tdb })
    })
    .then( res => { return res.json() } )
    .then( data => { 
        create_radio(data.tdb);
    })
    .catch( error => { console.log(error) } )
};

// export
const export_result = url => {
    fetch( url, { 
        method: 'POST',
        headers: { 'Content-Type' : 'application/json' },
        body : { 'tdb' : document.getElementById("topdb_input").value }
    })
    .then( res => { return res.json() } )
    .then( data => { console.log(data) } )
    .catch( error => { console.log(error) } )
};