// sse 이벤트
const getEvent = (targetId) => {
    var es = new EventSource('/stream');
    es.addEventListener('COMPLETE', (event) => {
        const data = JSON.parse(event.data);
        updateComplete(targetId, data.src);
    }, false);
}