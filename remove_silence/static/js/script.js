function loadFile(){
    var file = document.getElementById("input-file").files[0];
    var data = document.getElementById("input-file").files[0];
    var label = document.getElementById("input-label")

    var video = document.getElementById('input-video');
    video.setAttribute("src", URL.createObjectURL(file))
    video.classList.remove("hide")
    label.classList.add("hide")

    document.getElementById("tb").innerHTML += "<tr><td>파일이름</td><td>"+data.name+"</td></tr>";
    document.getElementById("tb").innerHTML += "<tr><td>파일크기</td><td>"+data.size+"</td></tr>";
    document.getElementById("tb").innerHTML += "<tr><td>파일타입</td><td>"+data.type+"</td></tr>";
    document.getElementById("tb").innerHTML += "<tr><td>수정날짜</td><td>"+data.lastModifiedDate.toString().split(' ').slice(0, 4).join(' ')+"</td></tr>";
}