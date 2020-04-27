document.getElementById("jsMusicUploadBtn").addEventListener("click", function () {
    verify = verifySubmit(
        [
            {id: '#music_name', tips: Dml.Msg.eperror, require: true},
            {id: '#music_times', tips: Dml.Msg.eperror, require: true},
            {id: '#music_price1', tips: Dml.Msg.eperror, require: true},
            {id: '#music_price2', tips: Dml.Msg.eperror, require: true},
            {id: '#music_price3', tips: Dml.Msg.eperror, require: true},
            {id: '#music_price4', tips: Dml.Msg.eperror, require: true},
            {id: '#music_price5', tips: Dml.Msg.eperror, require: true},
            {id: '#music_price6', tips: Dml.Msg.eperror, require: true},
            {id: '#music_image', tips: Dml.Msg.eperror, require: true},
            {id: '#demoLinkfile', tips: Dml.Msg.eperror, require: true},
            {id: '#hashLinkfile', tips: Dml.Msg.eperror, require: true},
            {id: '#keyfile', tips: Dml.Msg.eperror, require: true},
            {id: '#music_desc', tips: Dml.Msg.eperror, require: true},
            {id: '#music_bpm', tips: Dml.Msg.eperror, require: true},
        ]
    );
    if (!verify) {
        alert('请将表格填写完整！')
        return;
    }
    if (ethereum.selectedAddress == undefined) {
        alert('请登录METAMASK！')

        async function testAsync() {
            const accounts = await ethereum.enable();
            return accounts;
        }

        const account = testAsync()
        return;
    }
    if (ethereum.networkVersion != 428) {
        alert('请切换网到http://428')

        return;
    }
    var checkID = [];//定义一个空数组
    $("input[name='music_tags']:checked").each(function (i) {//把所有被选中的复选框的值存入数组
        checkID[i] = $(this).val();
    });
    if (checkID.length > 5) {
        Dml.fun.showTipsDialog({
            title: '标签过多',
            h2: '最多勾选五个标签'
        });
    }
    var demoLinkfile = $("#demoLinkfile")[0].files[0];
    var hashLinkfile = $("#hashLinkfile")[0].files[0];
    var image = $("#music_image")[0].files[0];
    var keyfile = $("#keyfile")[0].files[0];
    var music_name = $("#music_name").val();
    var music_times = $("#music_times").val();
    var music_desc = $("#music_desc").val();
    var music_price1 = $("#music_price1").val();
    var music_price2 = $("#music_price2").val();
    var music_price3 = $("#music_price3").val();
    var music_price4 = $("#music_price4").val();
    var music_price5 = $("#music_price5").val();
    var music_price6 = $("#music_price6").val();
    var address = ethereum.selectedAddress;
    var music_detail = id_music_detail.getContent();
    var music_bpm = $("#music_bpm").val();
    var music_issell = $("#music_issell").val();
    // console.log(music_bpm)
    // console.log(music_issell);

    // console.log(checkID);
    var formdata = new FormData();
    formdata.append('demoLinkfile', demoLinkfile);
    formdata.append('hashLinkfile', hashLinkfile);
    formdata.append('keyfile', keyfile);
    formdata.append('image', image);
    formdata.append('music_name', music_name);
    formdata.append('music_desc', music_desc);
    formdata.append('music_price1', music_price1);
    formdata.append('music_price2', music_price2);
    formdata.append('music_price3', music_price3);
    formdata.append('music_price4', music_price4);
    formdata.append('music_price5', music_price5);
    formdata.append('music_price6', music_price6);
    formdata.append('music_tags', checkID);
    formdata.append('music_times', music_times);
    formdata.append('address', address);
    formdata.append('music_detail', music_detail);
    formdata.append("music_bpm", music_bpm);
    formdata.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val(),);
    // console.log(music_price1)
    //   console.log(music_price2)
    //   console.log(music_price3)
    //   console.log(music_price4)
    //   console.log(music_price5)
    //   console.log(music_price6)
    $.ajax({
        cache: false,
        type: 'post',
        dataType: 'json',
        url: "/users/uploadone/",
        data: formdata,
        processData: false,    // 不处理数据
        contentType: false,    // 不设置内容类型
        success: function (data) {
            console.log(data);
            if (data.errormsg) {
                alert(data.errormsg);
                return;
            } else if (data.music_detail || data.image || data.music_name || data.music_desc || data.music_times || data.music_price1 || data.music_price2 || data.music_price3 || data.music_price4 || data.music_price5 || data.music_price6 || data.demoLinkfile || data.hashLinkfile || data.keyfile) {
                if (data.music_desc) $("#music_desc")[0].style.border = '2px solid red';
                if (data.demoLinkfile) $("#demoLinkfile")[0].style.border = '2px solid red';
                if (data.image) $("#music_image")[0].style.border = '2px solid red';
                if (data.music_name) $("#music_name")[0].style.border = '2px solid red';
                if (data.music_bpm) $("#music_bpm")[0].style.border = '2px solid red';
                if (data.music_bpm) $("#music_bpm")[0].style.border = '2px solid red';
                if (data.music_times) $("#music_times")[0].style.border = '2px solid red';
                if (data.music_price1) $("#music_price1")[0].style.border = '2px solid red';
                if (data.music_price2) $("#music_price2")[0].style.border = '2px solid red';
                if (data.music_price3) $("#music_price3")[0].style.border = '2px solid red';
                if (data.music_price4) $("#music_price4")[0].style.border = '2px solid red';
                if (data.music_price5) $("#music_price5")[0].style.border = '2px solid red';
                if (data.music_price6) $("#music_price6")[0].style.border = '2px solid red';
                if (data.hashLinkfile) $("#hashLinkfile")[0].style.border = '2px solid red';
                if (data.keyfile) $("#keyfile")[0].style.border = '2px solid red';
                alert('请按规定填写！');
                return;
            } else if (data.msg == 'success') {
                var hashLinkfileHash = data.hashLinkfileHash
                // console.log(data.msg);
                //                 // console.log(data.demoLinkfileHash)
                //                 // console.log(data.hashLinkfileHash)
                //                 // console.log(data.price_list)
                web3 = new Web3(web3.currentProvider);
                var MyContract = new web3.eth.Contract(abi, addresss);
                MyContract.methods.addProductToStorage(data.music_name_utf8, data.hashLinkfileHash, data.demoLinkfileHash, data.music_desc_utf8, music_issell, data.price_list).send({from: ethereum.selectedAddress})
                    .on('transactionHash', function (hash) {
                    })
                    .on('receipt', function (receipt) {
                        console.log(receipt)
                        alert('上链成功，系统正在确认，请稍等');
                        setTimeout(function () {
                            window.location.href = '/users/musicianmusic/'
                        }, 500)

                        // var formdata1 = new FormData();
                        // formdata1.append('transactionHash', receipt.transactionHash);
                        // formdata1.append('blockNumber', receipt.blockNumber);
                        // formdata1.append('transactionIndex', receipt.transactionIndex);
                        // formdata1.append('from', receipt.from);
                        // formdata1.append('keyfile', keyfile);
                        // formdata1.append('hashLinkfileHash', hashLinkfileHash);
                        // formdata1.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val(),);
                        // $.ajax({
                        //     cache: false,
                        //     type: 'post',
                        //     url: "/users/uploadtwo/",
                        //     data: formdata1,
                        //     async: true,
                        //     processData: false,    // 不处理数据
                        //     contentType: false,    // 不设置内容类型
                        //     success: function (data) {
                        //         console.log(data)
                        //         if (data.transactionHash || data.blockNumber || data.transactionIndex || data.keyfile || data.hashLinkfileHash) {
                        //             alert('错误，请联系管理员')
                        //             return;
                        //         } else if (data.msg) {
                        //             alert(data.msg)
                        //             location.reload();
                        //         } else if (data.errormsg) {
                        //             alert(data.errormsg)
                        //             return;
                        //         }
                        //     }
                        // });
                    })
                    .on('confirmation', function (confirmationNumber, receipt) {

                    })
                    .on('error', function (error, receipt) {

                    })
            }
        },
    });
});


var demofileInput = document.getElementById('demoLinkfile');
demofileInput.addEventListener('change', function () {
    var demoLinkfile = $("#demoLinkfile")[0].files[0];
    alert('文件上传中，请等待。。。。。。');
    var formdata = new FormData();
    formdata.append('ipfs_file', demoLinkfile);
    formdata.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val(),);
    $.ajax({
        cache: false,
        type: 'post',
        url: "/users/uploadfile/",
        data: formdata,
        async: true,
        processData: false,    // 不处理数据
        contentType: false,    // 不设置内容类型
        success: function (data) {
            console.log(data)
            if (data.status == 'success') {
                alert('文件上传成功，ipfshash为' + data.fileHash["Hash"])
                return;
            } else if (data.errormsg) {
                alert(data.errormsg)
                return;
            }
        }
    });
});

var fileInput = document.getElementById('hashLinkfile');
fileInput.addEventListener('change', function () {
    var hashLinkfile = $("#hashLinkfile")[0].files[0];
    alert('文件上传中，请等待。。。。。。');
    var formdata = new FormData();
    formdata.append('ipfs_file', hashLinkfile);
    formdata.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    $.ajax({
        cache: false,
        type: 'post',
        url: "/users/uploadfile/",
        data: formdata,
        async: true,
        processData: false,    // 不处理数据
        contentType: false,    // 不设置内容类型
        success: function (data) {
            console.log(data)
            if (data.status == 'success') {
                alert('文件上传成功，ipfshash为' + data.fileHash["Hash"])
                return;
            } else if (data.errormsg) {
                alert(data.errormsg)
                return;
            }
        }
    });
});
