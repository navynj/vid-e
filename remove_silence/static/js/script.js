function loadFile(){
    var file = document.getElementById("input-file").files[0];

    var label = document.getElementById("input-label");
    var video = document.getElementById('input-video');
    video.setAttribute("src", URL.createObjectURL(file));
    video.classList.remove("hide");
    label.classList.add("hide");  

    function bytesToSize(bytes) {
        var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        if (bytes == 0) return 'n/a';
        var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
        if (i == 0) return bytes + ' ' + sizes[i];
        return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
    };

    document.getElementById("tb").innerHTML += "<tr><td>파일 이름</td><td>"+file.name+"</td></tr>";
    document.getElementById("tb").innerHTML += "<tr><td>파일 크기</td><td>"+bytesToSize(file.size)+"</td></tr>";
    document.getElementById("tb").innerHTML += "<tr><td>파일 타입</td><td>"+file.type+"</td></tr>";
    document.getElementById("tb").innerHTML += "<tr><td>수정 날짜</td><td>"+file.lastModifiedDate.toString().split(' ').slice(0, 4).join(' ')+"</td></tr>";
    
    var form = document.getElementById("input-form");
    form.submit();
    console.log('여기까지 왔나');
}