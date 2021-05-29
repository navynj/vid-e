// sse 이벤트
const getEventData = (stream, event) => {
    var es = new EventSource(stream);
    es.addEventListener(event, (e) => {
        return JSON.parse(e.data);
    }, false);
}

const onComplete = (target) => {
    const data = getEventData('/export_status', 'COMPLETE');
    updateComplete(target);
    if (target.id === 'rm-silence')
        document.getElementById('add-effect').classList.remove('disabled');
}

// status별 상태 업데이트 : 추후 경우별 수정
const updateStatus = (id, process, currentStatus) => {
    // console.log(id);
    const targetParent = document.getElementById(id);
    // console.log(targetParent);
    const target = targetParent.querySelector(process);
    const status = target.querySelector('.status');

    // console.log(target);
    
    switch (currentStatus) {
        case 'PROCESS':
            // console.log(target);
            updateProcess(target, status);
            // onComplete(target);
            break;
        case 'COMPLETE':
            updateComplete(target, status);
            break;
        case 'DISABLED':
            status.className = "status";
            status.classList.add('disabled');
            target.classList.remove('active');
            break;
        default:
    }
}

// 다 함
function updateComplete(target, status) { 
    
    status.className = "status";
    status.classList.add("download");
    target.classList.add("active");
    
}

// 하는 중
function updateProcess(target, status) {
    console.log(status);
    console.log(status);
    status.className = "status";
    console.log(status.classList);
    status.classList.add("loader");
    target.classList.remove('active');
    // console.log(status.classList);
    // console.log(status);
}