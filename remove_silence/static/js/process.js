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
                                  // 리턴받은 json을 output 변수에 할당
                                  const output = data.output;
                                  // output.src로 오디오 태그 작성  
                                  const player = document.createElement('audio');
                                  player.canPlayType("audio/wave");
                                  player.setAttribute("src", output.src);
                                  player.setAttribute("controls", "controls");
                                  player.className += " audio_output_player"
                                  // 작성된 오디오 태그 html에 저장   
                                  document.getElementById('topdb_process').appendChild(player);
                            // 에러 시 : 콘솔창에 에러 띄우기
                            }).catch(error => {console.log(error)}
                            )};