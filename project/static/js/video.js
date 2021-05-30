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
const updateStatus = (id, currentStatus, src) => {
    const target = document.getElementById(id);
    switch (currentStatus) {
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
    console.log("==========");
    console.log(status.classList);
    status.classList.add("icon");
    status.classList.add("checked");
    console.log("==========");
    console.log(status.classList);
    // video
    const video = target.querySelector('.placeholder > video');
    video.src = src;
    video.classList.remove('hide');
    target.classList.remove('ready');
    // a : start
    const a = target.querySelector('.placeholder > .start');
    a.classList.add('hide');
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

}

// PROCESS
function updateProcess(target) {
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

function shortcut(activeProcessId, activeBtnId, disableProcessId, disableBtnId) {
    // get html
    const activeProcess = document.getElementById(activeProcessId);
    const activeBtn = document.getElementById(activeBtnId);
    const disableProcess = document.getElementById(disableProcessId);
    const disableBtn = document.getElementById(disableBtnId);
    // class manipulation
    activeProcess.classList.remove('disabled');
    activeBtn.classList.remove('hide');
    disableProcess.classList.add('disabled');
    disableBtn.classList.add('btn');
    // skip, prev JSON data
    switch (disableBtnId) {
        case 'skip':
            break;
        case 'prev':
            break;
    }

    const postJson = (json_data) => {
        const skipBtn = document.getElementById('skip');
        skipBtn.addEventListener('click', (e) => {
            console.log("skip btn is clicked");
            // return {
    
            // }
        })
}