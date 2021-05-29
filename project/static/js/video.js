// sse 이벤트
const getEventData = (stream, event) => {
    var es = new EventSource(stream);
    es.addEventListener(event, (e) => {
        return JSON.parse(e.data);
    }, false);
}

const onComplete = (target) => {
    const data = getEventData('/export_status', 'COMPLETE');
    updateComplete(target, 'static'/data.src);
    if (target.id === 'rm-silence')
        document.getElementById('add-effect').classList.remove('disabled');
}

// status별 상태 업데이트 : 추후 경우별 수정
const updateStatus = (id, status, src) => {
    const target = document.getElementById(id);

    switch (status) {
        case 'PROCESS':
            updateProcess(target, src);
            onComplete(target);
            break;
        case 'COMPLETE':
            console.log(target);
            updateComplete(target, src);
            console.log(target);
            break;
        case 'DISABLED':
            target.classList.add('disabled');
            break;
    }
}

// 상태별 html 업데이트
function updateComplete(target, src) {
    // video
    const video = target.querySelector('.placeholder > video');
    video.src = src;
    video.classList.remove('hide');
    // a
    const a = target.querySelector('.placeholder > a');
    a.classList.add('hide');
    // btn : download (, skip)
    const btn = target.querySelectorAll('button');
    for (i=0; i<btn.length; i++) btn[i].classList.add('hide');
    btn[0].classList.remove('hide');
    // loader
    const loader = target.querySelector(".placeholder > .loader");
    loader.classList.add("hide");

}

function updateProcess(target) {
    // video
    const video = target.querySelector('.placeholder > video');
    video.classList.add('hide');
    // a
    const a = target.querySelector('.placeholder > a');
    a.classList.add('hide');
    // btn : all
    const btn = target.querySelectorAll('button');
    for (i=0; i<btn.length; i++) btn[i].classList.add('hide');
    // loader
    const loader = target.querySelector(".placeholder > .loader");
    loader.classList.remove("hide");

}

function skip() {
    const rmSilence = document.getElementById('rm-silence');
    const addEffect = document.getElementById('add-effect');
    const prevBtn = document.getElementById('prev');
    const skipBtn = document.getElementById('skip');
    rmSilence.classList.add('disabled');
    addEffect.classList.remove('disabled');
    skipBtn.classList.add('hide');
    // prevBtn.classList.remove('hide');
}

function prev() {
    const rmSilence = document.getElementById('rm-silence');
    const addEffect = document.getElementById('add-effect');
    const prevBtn = document.getElementById('prev');
    const skipBtn = document.getElementById('skip');
    rmSilence.classList.remove('disabled');
    addEffect.classList.add('disabled');
    skipBtn.classList.remove('hide');
    // prevBtn.classList.add('hide');
}