function loadFile(){
    var file = document.getElementById("input-file").files[0];

    var label = document.getElementById("input-label");
    var video = document.getElementById('input-video');
    video.setAttribute("src", URL.createObjectURL(file));
    video.classList.remove("hide");
    label.classList.add("hide");

    document.getElementById("tb").innerHTML += "<tr><td>파일이름</td><td>"+file.name+"</td></tr>";
    document.getElementById("tb").innerHTML += "<tr><td>파일크기</td><td>"+file.size+"</td></tr>";
    document.getElementById("tb").innerHTML += "<tr><td>파일타입</td><td>"+file.type+"</td></tr>";
    document.getElementById("tb").innerHTML += "<tr><td>수정날짜</td><td>"+file.lastModifiedDate.toString().split(' ').slice(0, 4).join(' ')+"</td></tr>";

    var form = document.getElementById("input-form");
    form.submit();
    console.log('여기까지 왔나');
}