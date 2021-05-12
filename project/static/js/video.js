// sse 이벤트
const getEvent = (target) => {
    var es = new EventSource('/stream');
    es.addEventListener('COMPLETE', (event) => {
        const data = JSON.parse(event.data);
        updateComplete(target, data.src);
    }, false);
}

// status별 상태 업데이트 : 추후 경우별 수정
const updateStatus = (id, status) => {
    const target = getElementById(id);
    switch (status) {
        case 'PROCESS':
            updateProcess(target);
            getEvent(target);
            break;
        case 'COMPLETE':
            updateComplete(target);
            break;
        case 'READY':
            updateReady(target);
            break;
        case 'DISABLED':
            target.classList.add('disabled');
            break;
        default:
            console.log(id + ' : no valid status');
    }
}
const rmSilenceUpdate = (status) => updateStatus('rm-silence', status);
const addEffectUpdate = (status) => updateStatus('add-effect', status);

// 상태별 html 업데이트
function updateComplete(target, src) {
    // video
    const video = target.querySelector('.placeholder > video');
    video.src = src;
    video.classList.remove('hide');
    // a
    const a = target.querySelector('placeholder > a');
    a.classList.add('hide');
    // btn : download (, skip)
    const btn = target.querySelectorAll('button');
    for (i=0; i<btn.length; i++) btn[i].classList.add('hide');
    btn[0].classList.remove('hide');
}

function updateReady(target) {
    // video
    const video = target.querySelector('.placeholder > video');
    video.classList.add('hide');
    // a
    const a = target.querySelector('placeholder > a');
    a.classList.remove('hide');
    // btn : download (, skip)
    const btn = target.querySelectorAll('button');
    for (i=0; i<btn.length; i++) btn[i].classList.remove('hide');
    btn[0].classList.add('hide');
}

function updateProcess(target) {
    // video
    const video = target.querySelector('.placeholder > video');
    video.classList.add('hide');
    // a
    const a = target.querySelector('placeholder > a');
    a.classList.add('hide');
    // btn : all
    const btn = target.querySelectorAll('button');
    for (i=0; i<btn.length; i++) btn[i].classList.remove('hide');

    // # target.innerHTML로 스피너 추가하기

    // # 하단 notification 블록 추가하기 : innerHTML, a 태그
    const process = document.getElementById('process');
    const note = document.createElement('div');
    
}

function skip() {
    const rmSilence = document.getElementById('rm-silence');
    const addEffect = document.getElementById('add-effect');
    rmSilence.classList.add('disabled');
    addEffect.classList.remove('disabled');
}