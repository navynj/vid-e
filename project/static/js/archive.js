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
            updateProcess(target, status);
            getEventData(target, '/export_status', 'COMPLETE');
            break;
        case 'COMPLETE':
            updateComplete(target, status);
            target.classList.remove('active');
            break;
        case 'DISABLED':
            status.className = "status";
            status.classList.add('disabled');
            target.classList.remove('active');
            break;
    }
}

// COMPLETE
function updateComplete(target, status) { 
    status.className = "status";
    status.classList.add("download");
    target.classList.add("active");
}

// PROCESS
function updateProcess(target, status) {
    status.className = "status";
    status.classList.add("loader");
    target.classList.remove('active');
}

// update list
const update = (video) => {
    for (let n=0; n<videoData.length; n++){
        updateStatus(videoData[n].id, video[n].rm_silence.status, '.process.rm-silence');
        updateStatus(videoData[n].id, video[n].add_effect.status, '.process.add-effect');
    };
};