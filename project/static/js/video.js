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
const updateStatus = (id, currentStatus, src='') => {
    const target = document.getElementById(id);
    switch (currentStatus) {
        case 'PROCESS':
            updateProcess(target, src);
            getEventData(target, '/export_status', 'COMPLETE');
            break;
        case 'COMPLETE':
            updateComplete(target, src);
            break;
        case 'DISABLED':
            updateDisabled(target);
            break;
        case 'READY':
            updateReady(target);
            break;
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
    // prev
    const prev = document.getElementById("prev");
    if (prev)
        prev.classList.add('hide');

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

const updateDisabled = (target) => {
    target.classList.add('disabled');
    target.querySelector('button').classList.add('hide');
}

const updateReady = (target) => {
    target.classList.remove('disabled');
    target.querySelector('button').classList.remove('hide');
}

const postJson = (json_data) => {
    return {
        method: 'POST',
        headers: { 'Content-Type' : 'application/json' },
        body : JSON.stringify(json_data)
    }
}

const shortcut = (url, rmStatus, addStatus) => {
    fetch(url, postJson(
        {
            "rm_silence": {
                "status": rmStatus,
                "src": ""
            },
            "add_effect": {
                "status": addStatus,
                "src": ""
            }
        }
    ))
    .then( res => { return res.json() } )
    .then( data => {
        updateStatus("rm-silence", data.rmStatus);
        updateStatus("add-effect", data.addStatus);
    })
    .catch( error => { console.log(error) } )
};