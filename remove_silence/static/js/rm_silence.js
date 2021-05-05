// top_db input 창에서 엔터 입력 허용
document.getElementById('topdb_input').addEventListener('keyup', (e)=>{
  if (e.keyCode === 13) {
    const submit = document.getElementById('topdb_submit');
    submit.onclick();
  }  
});

// top_db 서버 전송 및 결과 수신과정
// - 인자로 받은 url(서버)에 전송
// - POST 메소드로, body 안에 tobdb 정보 전달하기
const input_topdb = url => { fetch ( url, {
    method: 'POST',
    headers: {
      'Content-Type' : 'application/json'
    },
    body: JSON.stringify({
      'tdb' : document.getElementById('topdb_input').value
    })
    // 성공 시 : url(서버)에서 리턴받은 response의 json을 리턴
  }).then(res => {return res.json()})
  .then(data => {
    // 변수 정의
    const tdb = data.split.tdb;
    const sr = data.split.sr;
    const intervals = data.split.mute_intervals;

    // 라디오 정의 (display: none)
    const radio = document.createElement('input');
    radio.type = "radio";
    radio.name = "tdb";
    radio.id = `${tdb}`;
    radio.value = `${tdb}`;
    radio.classList.add("hide");
    radio.checked = true;
    // 라벨 정의 (click : update_waveform)
    const label = document.createElement('label');
    label.htmlFor = `${tdb}`;
    label.innerText = `${tdb}`;
    label.addEventListener('click', (e)=>update_waveform(sr, intervals));

    // 라디오 선택 상태 초기화
    const radios = document.getElementsByName("tdb");
    for(let i=0; i<radios.length; i++)
      if(radios[i].checked)
        radios[i].checked = false;
    // 폼에 현재 라디오+라벨 추가
    const form = document.getElementById('split_outputs');
    form.appendChild(radio);
    form.appendChild(label);

    // waveform 업데이트
    update_waveform(sr, intervals);
  }).catch(error => {console.log(error)} // 에러 시 : 콘솔창에 에러 띄우기
)};