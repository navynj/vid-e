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
const updateStatus = (id, process, status, src) => {
    const targetParent = document.getElementById(id);
    const target = targetParent.querySelector(process);
    switch (status) {
        case 'PROCESS':
            updateProcess(target, src);
            onComplete(target);
            break;
        case 'COMPLETE':
            updateComplete(target, src);
            break;
        case 'DISABLED':
            target.classList.add('disabled');
            break;
        default:
    }
}

// 다 함
function updateComplete(target, src) {

    const video = target.querySelector('.vids');
    video.src = src;

    const loader = target.querySelector('.loader');
    const preCheck = target.querySelector('.pre-checkmark');
    const checked = target.querySelector(' .checkmark');
    loader.classList.add("hide");
    preCheck.classList.add("hide");
    checked.classList.remove("hide");
    // console.log(loader);
    // console.log(preCheck);
    // console.log(checked);
}

// 하는 중
function updateProcess(target, src) {
    // console.log("target");
    // console.log(target);
    // console.log("src");
    // console.log(src);
    const video = target.querySelector('.vids');
    video.src = src;
    // console.log(src);
    const loader = target.querySelector('.loader');
    const preCheck = target.querySelector('.pre-checkmark');
    const checked = target.querySelector('.checkmark');
    loader.classList.remove("hide");
    preCheck.classList.add("hide");
    checked.classList.add("hide");
}