function showPicture(source) {
    var file = source.files[0];
    if (window.FileReader) {
        var fr = new FileReader();
        //console.log(fr);
        var pic = document.getElementById('pic');
        fr.onloadend = function (e) {
            pic.src = e.target.result;
        };
        fr.readAsDataURL(file);
        // console.log(fr.readAsDataURL(file));
        pic.style.display = 'block';
        pic.style.width = '180px';
        pic.style.height = '180px';
        pic.style.margin = 'auto';
    }
}


function click_input() {
    return document.getElementById('_image').click();
}
