function changeTextarea() {
    document.getElementById("_text").style.border = "1px solid cornflowerblue";
}

function changeTextarea1() {
    document.getElementById("_text").style.border = "1px solid  fblack";
}

function wordStatic(input) {
    // 获取已经输入字数文本框对象
    var content = document.getElementById('num');
    if (content && input) {
        // 获取输入内容长度并更新到界面
        var value = input.value;
        // 将换行符不计算为单词数
        value = value.replace(/\n|\r/gi, "");
        // 更新计数
        content.innerText = value.length;
    }
}

    $("#text").bind("input propertychange", function (event) {
    var viewName = this.value;
    viewName = $.trim(viewName);
    this.value = viewName;

    if (viewName.length == 0) {
        layer.tips("名称不能为空！", this, {tips: [1, "#FF5722"]});
        return;
    }

    $("#test").html(viewName.toUpperCase());
});
