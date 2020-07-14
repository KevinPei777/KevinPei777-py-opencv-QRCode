function showQRCode(source) {
    var file = source.files[0];
    if (window.FileReader) {
        var fr = new FileReader();
        //console.log(fr);
        var code_pic = document.getElementById('_qrcode');
        fr.onloadend = function (e) {
            code_pic.src = e.target.result;
        };
        fr.readAsDataURL(file);
        // console.log(fr.readAsDataURL(file));
        code_pic.style.display = 'block';
        code_pic.style.width = '180px';
        code_pic.style.height = '180px';
        code_pic.style.margin = 'auto';
    }
}

function click_input() {
    return document.getElementById('_code').click();
}

function showImage(source) {
    var file = source.files[0];
    if (window.FileReader) {
        var fr = new FileReader();
        //console.log(fr);
        var pic = document.getElementById('upload_image');
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

function click_input_2() {
    return document.getElementById('_image').click();
}