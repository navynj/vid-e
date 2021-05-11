// sse 이벤트
const getEvent = (targetId) => {
    var es = new EventSource('/stream');
    es.addEventListener('COMPLETE', (event) => {
        const data = JSON.parse(event.data);
        updateComplete(targetId, data.src);
    }, false);
}

// status별 상태 업데이트 : 추후 경우별 수정
const rmSilenceUpdate = (status) => {
    const id = 'rm-silence';
    switch (status) {
        case 'PROCESS':
            updateProcess(id);
            getEvent(id);
        case 'COMPLETE':
            updateComplete(id);
        case 'READY':
            updateReady(id);
            // 건너뛰기 버튼
        case 'DISABLED':
            updateComplete(id);
            updateDisabled(id);
        default:
            console.log(id + ' : no valid status');
    }
}

const addEffectUpdate = (status) => {
    const id = 'add-effect';
    switch (status) {
        case 'PROCESS':
            updateProcess(id);
            getEvent(id);
        case 'COMPLETE':
            updateComplete(id);
        case 'READY':
            updateReady(id);
        case 'DISABLED':
            updateReady(id);
            updateDisabled(id);
        default:
            console.log(id + ' : no valid status');
    }
}


// 
function updateComplete(targetId, src) {
    const target = document.getElementById(targetId);
    const video = target.querySelector('video');
    video.src = src;
    video.classList.remove('hide');
}
function updateReady(targetId) {;}
function updateProcess(targetId) {;}
function updateDisabled(targetId) {;}