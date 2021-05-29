// sse 이벤트
const getEventData = (target, stream, event) => {
    var es = new EventSource(stream);
    es.addEventListener(event, (e) => {
        const data = JSON.parse(e.data);
        updateComplete(target, 'static/' + data.src);
        if (target.id === 'rm-silence')
            document.getElementById('add-effect').classList.remove('disabled');
    }, false);
}

// status별 상태 업데이트 : 추후 경우별 수정
const updateStatus = (id, status, src) => {
    const target = document.getElementById(id);

    switch (status) {
        case 'PROCESS':
            updateProcess(target, src);
            getEventData(target, '/export_status', 'COMPLETE');
            break;
        case 'COMPLETE':
            updateComplete(target, src);
            break;
        case 'DISABLED':
            target.classList.add('disabled');
            break;
        case 'READY':
            target.classList.remove('disabled');
    }
}

// 상태별 html 업데이트
// COMPLETE
function updateComplete(target, src) {
    target.classList.remove('disabled');
    // status
    const status = target.querySelector('.status');
    status.classList.add("icon");
    status.classList.add("checked");
    // video
    const video = target.querySelector('.placeholder > video');
    video.src = src;
    video.classList.remove('hide');
    target.classList.remove('ready');
    // a : start
    const a = target.querySelector('.placeholder > .start');
    console.log(a.classList);
    a.classList.add('hide');
    console.log(a.classList);
    // loader
    const loader = target.querySelector(".placeholder > .load");
    loader.classList.add("hide");
    // btn : download (, skip)
    const btn = target.querySelectorAll('button');
    for (i=0; i<btn.length; i++) btn[i].classList.add('hide');
    btn[0].classList.add('hide');
    // a : download
    const download = target.querySelector('.download');
    download.classList.remove('hide');
    // prev
    const prev = document.getElementById("prev");
    if (prev)
        prev.classList.add('hide');

}

// PROCESS
function updateProcess(target) {
    console.log("=====UPDATE PROCESS=======");
    target.classList.remove('disabled');
    // video
    const video = target.querySelector('.placeholder > video');
    video.classList.add('hide');
    // a : start
    const a = target.querySelector('.placeholder > a');
    a.classList.add('hide');
    // loader
    const loader = target.querySelector(".placeholder > .load");
    loader.classList.remove("hide");
    // a : download
    const dl = target.querySelector('a');
    dl.classList.add('hide');
    // btn : download (, skip)
    const btn = target.querySelectorAll('button');
    for (i=0; i<btn.length; i++) btn[i].classList.add('hide');
    btn[0].classList.add('hide');
}

function skip() {
    const rmSilence = document.getElementById('rm-silence');
    const addEffect = document.getElementById('add-effect');
    const prevBtn = document.getElementById('prev');
    const skipBtn = document.getElementById('skip');
    rmSilence.classList.add('disabled');
    addEffect.classList.remove('disabled');
    skipBtn.classList.add('hide');
    prevBtn.classList.remove('hide');
}

function prev() {
    const rmSilence = document.getElementById('rm-silence');
    const addEffect = document.getElementById('add-effect');
    const prevBtn = document.getElementById('prev');
    const skipBtn = document.getElementById('skip');
    rmSilence.classList.remove('disabled');
    addEffect.classList.add('disabled');
    skipBtn.classList.remove('hide');
    prevBtn.classList.add('hide');
}