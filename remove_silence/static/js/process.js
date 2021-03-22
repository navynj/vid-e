
// top_db input 창에서 엔터 입력 허용
document.getElementById('topdb_input').addEventListener('keyup', (e)=>{
    if (e.keyCode === 13) {
       const submit = document.getElementById('topdb_submit');
       submit.onclick();
  }  
 });

// top_db 서버 전송 및 결과 수신과정:
                                    // 인자로 받은 url(서버)에 전송하되
                                            // POST 메소드로, body 안에 tobdb 정보 전달하기
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
                                  // 오디오 플레이어, 다운로드 버튼, 아웃풋 정보 담을 form 생성 
                                  const audio_output = document.createElement('form');
                                  audio_output.id = `${data.output.tdb}dB`;
                                  audio_output.className = "audio_output";
                                  audio_output.method = "POST";
                                  audio_output.action="/download"
                                  audio_output.enctype="multipart/form-data"

                                  // 리턴받은 data 중 output 정보 추가
                                  const output_info = document.createElement('input');
                                  output_info.type = "hidden";
                                  output_info.name = "output_info";
                                  output_info.value = JSON.stringify(data.output);
                                  audio_output.appendChild(output_info);
                                  // 리턴받은 data 중 file 정보 추가
                                  const file_info = document.createElement('input');
                                  file_info.type = "hidden";
                                  file_info.name = "file_info";
                                  file_info.value = JSON.stringify(data.file);
                                  audio_output.appendChild(file_info);

                                  // output.src로 오디오 태그 생성 후 추가
                                  const player = document.createElement('audio');
                                  player.canPlayType("audio/wave");
                                  player.src = data.output.src;
                                  player.controls = "controls";
                                  player.className = "player";
                                  audio_output.appendChild(player);

                                  // 버튼 태그 생성 후 추가
                                  const btn = document.createElement('button');
                                  btn.type = "submit";
                                  btn.className = "btn"
                                  btn.innerHTML = `<span>(${data.output.tdb}dB) Get video output</span>`;
                                  btn.onclick = audio_output.submit();
                                  audio_output.appendChild(btn);

                                  // 작성된 오디오 아웃풋 태그 html에 추가   
                                  document.getElementById('audio_outputs').appendChild(audio_output);

                                  console.log(data.output.nonmute_intervals);
                                  console.log(data.output.sr);
                                  // 현재 topdB 값으로 처리된 무음구간 파형에 표시
                                  mute_region(data.output.sr, data.output.mute_intervals);
                            // 에러 시 : 콘솔창에 에러 띄우기
                            }).catch(error => {console.log(error)}
                        )};