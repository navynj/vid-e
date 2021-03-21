                                    // 인자로 받은 url(서버)에 전송하되
                                            // POST 메소드로, body 안에 tobdb 정보 전달하기
const input_tobdb = url => { fetch ( url, {
                                            method: 'POST',
                                            headers: {
                                                'Content-Type' : 'application/json'
                                            },
                                            body: JSON.stringify({
                                                'tdb' : document.getElementById('topdb_input').value
                                        })
                            // 성공 시 : url(서버)에서 리턴받은 response의 json을 리턴
                            }).then(res => {return res.json()})
                            //       : 리턴받은 json을 output 변수에 저장
                              .then(data => {
                                  const output = data.output;
                            // 에러 시 : 콘솔창에 에러 띄우기
                            }).catch(error => {console.log(error)}
                            )};


// // download button - get removed video for download
// const get_removed_video = (url, sr, intervals, tdb, name, ext) => {fetch(url,{
//     method: 'POST',
//     headers: {'Content-Type':'application/json'},
//     body: JSON.stringify({
//         'sr': sr,
//         'intervals': intervals,
//         'fname': `${tdb}dB_removed_${name}.${ext}`
//     })
// })
// .then(res => {return res.json})
// .then(data => {console.log(data)})
// }


// show waveform & video button -> 사용자의 이해를 돕기 위한 옵션, .. . 