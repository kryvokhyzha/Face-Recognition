function uploadChange(val) {
    var name_list = val.split('\\')
    document.getElementById('uploadValue').innerHTML = '<br>Завантажений файл: ' + name_list[name_list.length - 1];
}