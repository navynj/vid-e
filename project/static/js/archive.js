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
const updateStatus = (id, process, currentStatus) => {

    const targetParent = document.getElementById(id);

    const target = targetParent.querySelector(process);
    const status = target.querySelector('.status');


    switch (currentStatus) {
        case 'PROCESS':
            // console.log(target);
            getEventData(target, '/export_status', 'COMPLETE')
            // onComplete(target);
            break;
        case 'COMPLETE':
            updateComplete(target, status);
            // target.classList.remove('active');
            break;A
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