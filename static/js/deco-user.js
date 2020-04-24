function refresh_captcha(event) {
    $.get("/captcha/refresh/?" + Math.random(), function (result) {
        $('#jsRefreshCode img.captcha').attr("src", result.image_url);
        $('#id_captcha_0').attr("value", result.key);
    });
    return false;
}

$('#jsRefreshCode img.captcha').on('click', function () {
    refresh_captcha();
});

//修改个人中心邮箱验证码
function sendCodeChangeEmail($btn) {
    var verify = verifyDialogSubmit(
        [
            {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true}
        ]
    );
    if (!verify) {
        return;
    }
    $.ajax({
        cache: false,
        type: "get",
        dataType: 'json',
        url: "/users/sendemail_code/",
        data: $('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend: function (XMLHttpRequest) {
            $btn.val("发送中...");
            $btn.attr('disabled', true);
        },
        success: function (data) {
            if (data.email) {
                Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
            } else if (data.status == 'success') {
                Dml.fun.showErrorTips($('#jsChangeEmailTips'), "邮箱验证码已发送");
            } else if (data.status == 'failure') {
                Dml.fun.showValidateError($('#jsChangeEmail'), "邮箱验证码发送失败");
            } else if (data.status == 'success') {
            }
        },
        complete: function (XMLHttpRequest) {
            $btn.val("获取验证码");
            $btn.removeAttr("disabled");
        }
    });

}

//个人资料邮箱修改
function changeEmailSubmit($btn) {
    var verify = verifyDialogSubmit(
        [
            {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true},
        ]
    );
    if (!verify) {
        return;
    }
    $.ajax({
        cache: false,
        type: 'post',
        dataType: 'json',
        url: "/users/update_email/ ",
        data: $('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend: function (XMLHttpRequest) {
            $btn.val("发送中...");
            $btn.attr('disabled', true);
            $("#jsChangeEmailTips").html("验证中...").show(500);
        },
        success: function (data) {
            if (data.email) {
                Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
            } else if (data.status == "success") {
                Dml.fun.showErrorTips($('#jsChangePhoneTips'), "邮箱信息更新成功");
                setTimeout(function () {
                    location.reload();
                }, 1000);
            } else {
                Dml.fun.showValidateError($('#jsChangeEmail'), "邮箱信息更新失败");
            }
        },
        complete: function (XMLHttpRequest) {
            $btn.val("完成");
            $btn.removeAttr("disabled");
        }
    });
}

//个人资料手机修改
function changePhoneSubmit($btn) {
    var verify = verifyDialogSubmit(
        [
            {id: '#jsChangePhone', tips: Dml.Msg.epPhone, errorTips: Dml.Msg.erPhone, regName: 'phone', require: true},
            {
                id: '#jsChangePhoneCode',
                tips: Dml.Msg.epPhCode,
                errorTips: Dml.Msg.erPhCode,
                regName: 'phoneCode',
                require: true
            }
        ]
    );
    if (!verify) {
        return;
    }
    $.ajax({
        cache: false,
        type: 'post',
        dataType: 'json',
        url: "/users/update/mobile/",
        data: $('#jsChangePhoneForm').serialize(),
        beforeSend: function (XMLHttpRequest) {
            $btn.val("发送中...");
            $btn.attr('disabled', true);
            Dml.fun.showErrorTips($('#jsChangePhoneTips'), "验证中...");
        },
        success: function (data) {
            refresh_captcha({"data": {"form_id": "jsChangePhoneForm"}});
            if (data.mobile) {
                Dml.fun.showValidateError($('#jsChangePhoneCode'), data.mobile);
            } else if (data.mobile_code) {
                Dml.fun.showValidateError($('#jsChangePhoneCode'), data.mobile_code);
            } else if (data.captcha) {
                Dml.fun.showValidateError($('#jsChangePhone'), data.captcha);
            } else if (data.status == "success") {
                //验证成功，回到个人资料修改界面
                Dml.fun.showErrorTips($('#jsChangePhoneTips'), "手机信息更新成功");
                setTimeout(function () {
                    location.reload();
                }, 1000);
            } else {
                Dml.fun.showValidateError($('#jsChangePhone'), "手机信息更新失败");
            }
        },
        complete: function (XMLHttpRequest) {
            $btn.val("完成");
            $btn.removeAttr("disabled");
        }
    });
}

//修改个人中心手机号码时发动短信
function sendCodeChangePhone($btn) {
    var verify = verifyDialogSubmit(
        [
            {id: '#jsChangePhone', tips: Dml.Msg.epPhone, errorTips: Dml.Msg.erPhone, regName: 'phone', require: true},
            {
                id: '#jsChangePhoneForm #id_captcha_1',
                tips: Dml.Msg.epVerifyCode,
                errorTips: Dml.Msg.erVerifyCode,
                regName: 'verifyCode',
                require: true
            }
        ]
    );
    if (!verify) {
        return;
    }

    $.ajax({
        cache: false,
        type: 'post',
        dataType: 'json',
        url: "/send_sms/",
        // data:$('#jsChangePhoneForm').serialize(),
        data: {
            mobile: $("#jsChangePhone").val(),
            captcha_1: $("#id_captcha_1").val(),
            captcha_0: $('#id_captcha_0').val(),
        },
        beforeSend: function (XMLHttpRequest) {
            $btn.val("发送中...");
            $btn.attr('disabled', true);
        },
        success: function (data) {
            if (data.mobile) {
                Dml.fun.showValidateError($('#jsChangePhone'), data.mobile);
            } else if (data.captcha) {
                Dml.fun.showValidateError($('#jsChangePhoneForm #id_captcha_1'), data.captcha);
            } else if (data.status == 'success') {
                Dml.fun.showErrorTips($('#jsChangePhoneTips'), "短信验证码已发送");
            } else if (data.status == 'fail') {
                Dml.fun.showValidateError($('#jsChangePhone'), "短信验证码发送失败");
            }
        },
        complete: function (XMLHttpRequest) {
            $btn.val("获取验证码");
            $btn.removeAttr("disabled");
        }
    });

}

$(function () {
    $('#jsupdatekey').on('click', function () {
        Dml.fun.showDialog('#updatekeyDialog', '#jsupdatekeyTips');
    });
    $('#jsupdatekeyBtn').click(function () {
        var verify = verifyDialogSubmit(
            [
                {id: '#jsupdatekeyValue', tips: Dml.Msg.erPwd, errorTips: Dml.Msg.erPwd, regName: 'pwd', require: true},
                {
                    id: '#jsRefreshCode #id_captcha_1',
                    tips: Dml.Msg.epVerifyCode,
                    errorTips: Dml.Msg.erVerifyCode,
                    regName: 'verifyCode',
                    require: true
                }
            ]
        );
        if (!verify) {
            return;
        }
        $.ajax({
            cache: false,
            type: "POST",
            dataType: 'json',
            url: "/users/update_key/",
            data: {
                "captcha_1": $('#id_captcha_1').val(),
                "captcha_0": $('#id_captcha_0').val(),
                "value": $('#jsupdatekeyValue').val(),
                "one": true,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            },
            beforeSend: function (XMLHttpRequest) {
                $('#jsupdatekeyBtn').val("发送中...");
                $('#jsupdatekeyBtn').attr('disabled', true);
            },
            async: true,
            success: function (data) {
                console.log(data.captcha)
                if (data.captcha) {
                    Dml.fun.showValidateError($('#jsRefreshCode #id_captcha_1'), data.captcha);
                } else if (data.__all__) {
                    Dml.fun.showValidateError($("#jsRefreshCode #id_captcha_1"), data.__all__);
                } else if (data.msg == 'ok') {
                    var requestData = JSON.stringify({
                        "value": $('#jsupdatekeyValue').val(),
                        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                    });
                    var url = "/users/update_value/";
                    var xhr = new XMLHttpRequest();
                    xhr.open('post', url, true);        // 也可以使用POST方式，根据接口
                    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;charset=utf-8");
                    xhr.responseType = "blob";    // 返回类型blob
                    // 定义请求完成的处理函数，请求前也可以增加加载框/禁用下载按钮逻辑
                    xhr.onload = function () {
                        // 请求完成
                        if (xhr.status === 200) {
                            var blob = this.response;
                            var reader = new FileReader();
                            reader.readAsDataURL(blob);    // 转换为base64，可以直接放入a的href
                            reader.onload = function (e) {
                                // 转换完成，创建一个a标签用于下载
                                var a = document.createElement('a');
                                a.download = 'newaccount.json';
                                a.href = e.target.result;
                                $("body").append(a);    // 修复firefox中无法触发click
                                a.click();
                                $(a).remove();
                                window.parent.location.reload();

                            }
                        }


                    };
                    xhr.send('value=' + $('#jsupdatekeyValue').val());
                } else if (data.msg) {
                    Dml.fun.showValidateError($("#jsupdatekeyValue"), data.msg);
                }
            },
            complete: function (XMLHttpRequest) {
                $('#jsupdatekeyBtn').val("提交");
                $('#jsupdatekeyBtn').removeAttr("disabled");

            }
        });
    });
});
$(function () {
    //个人资料修改密码
    $('#jsUserResetPwd').on('click', function () {
        Dml.fun.showDialog('#jsResetDialog', '#jsResetPwdTips');
    });
    $('#jsResetPwdBtn').click(function () {
        var verify = verifyDialogSubmit(
            [
                {id: '#pwd', tips: Dml.Msg.epResetPwd, errorTips: Dml.Msg.erPwd, regName: 'pwd', require: true},
                {id: '#repwd', tips: Dml.Msg.epResetPwd, errorTips: Dml.Msg.erPwd, regName: 'pwd', require: true}
            ]
        );
        if (!verify) {
            return;
        }
        $.ajax({
            cache: false,
            type: "POST",
            dataType: 'json',
            url: "/users/update/pwd/",
            data: $('#jsResetPwdForm').serialize(),
            async: true,
            beforeSend: function (XMLHttpRequest) {
                $('#jsResetPwdBtn').val("发送中...");
                $('#jsResetPwdBtn').attr('disabled', true);
            },
            success: function (data) {
                if (data.password1) {
                    Dml.fun.showValidateError($("#pwd"), data.password1);
                } else if (data.password2) {
                    Dml.fun.showValidateError($("#repwd"), data.password2);
                } else if (data.__all__) {
                    Dml.fun.showValidateError($("#repwd"), data.__all__);
                } else if (data.status == "success") {
                    Dml.fun.showTipsDialog({
                        title: '提交成功',
                        h2: '修改密码成功，请重新登录!',
                    });
                    Dml.fun.winReload();
                } else if (data.msg) {
                    Dml.fun.showValidateError($("#pwd"), data.msg);
                    Dml.fun.showValidateError($("#repwd"), data.msg);
                }
            },

            complete: function (XMLHttpRequest) {
                $('#jsResetPwdBtn').val("提交");
                $('#jsResetPwdBtn').removeAttr("disabled");
            }
        });
    });

    //个人资料头像
    $('.js-img-up').uploadPreview({
        Img: ".js-img-show", Width: 94, Height: 94, Callback: function () {
            $('#jsAvatarForm').submit();
        }
    });

    $('#jsChangeEmailCodeBtn').on('click', function () {
        sendCodeChangeEmail($(this));
    });
    $('#jsChangeEmailBtn').on('click', function () {
        changeEmailSubmit($(this));
    });
    $('#jsChangePhoneBtn').on('click', function () {
        changePhoneSubmit($(this));
    });
    $('#jsChangePhoneCodeBtn').on('click', function () {
        sendCodeChangePhone($(this));
    });
    $('.changeemai_btn').on('click', function () {
        Dml.fun.showDialog('#jsChangePhoneDialog', '#jsChangePhoneTips', 'jsChangeEmailTips');
    });

    //input获得焦点样式
    $('.perinform input[type=text]').focus(function () {
        $(this).parent('li').addClass('focus');
    });
    $('.perinform input[type=text]').blur(function () {
        $(this).parent('li').removeClass('focus');
    });

    laydate({
        elem: '#birth_day',
        format: 'YYYY-MM-DD',
        max: laydate.now()
    });

    verify(
        [
            {id: '#nick_name', tips: Dml.Msg.epNickName, require: true}
        ]
    );

    //保存个人资料
    $('#jsEditUserBtn').on('click', function () {
        var _self = $(this),
            $jsEditUserForm = $('#jsEditUserForm')
        verify = verifySubmit(
            [
                {id: '#nick_name', tips: Dml.Msg.epNickName, require: true},
                {id: '#birth_day', tips: Dml.Msg.epBirthday, require: true},
                {id: '#address', tips: Dml.Msg.epAddress, require: true},
                {id: '#publickey', tips: Dml.Msg.epPublickey, require: true},
                {id: '#mobile', tips: Dml.Msg.epPhone, require: true},
            ]
        );
        if (!verify) {
            return;
        }
        $.ajax({
            cache: false,
            type: 'post',
            dataType: 'json',
            url: "/users/info/",
            data: $jsEditUserForm.serialize(),
            async: true,
            beforeSend: function (XMLHttpRequest) {
                _self.val("保存中...");
                _self.attr('disabled', true);
            },
            success: function (data) {
                if (data.nick_name) {
                    _showValidateError($('#nick_name'), data.nick_name);
                } else if (data.birthday) {
                    _showValidateError($('#birth_day'), data.birthday);
                } else if (data.address) {
                    _showValidateError($('#address'), data.address);
                } else if (data.status == "fail") {
                    // Dml.fun.showTipsDialog({
                    //     title: '保存失败',
                    //     h2: data.msg
                    // });
                    alert(data.msg);
                    return
                } else if (data.status == "success") {
                    // Dml.fun.showTipsDialog({
                    //     title: '保存成功',
                    //     h2: '个人信息修改成功！'
                    // });
                    alert('保存成功');
                    setTimeout(function () {
                        window.location.href = window.location.href;
                    }, 1500);
                }
            },
            complete: function (XMLHttpRequest) {
                _self.val("保存");
                _self.removeAttr("disabled");
            }
        });
    });


})
;
$(function () {
    //成为版权发布者
    $('#jsproductorkey').on('click', function () {
        Dml.fun.showDialog('#jsproductorkeybox', '#jsproductorkeyboxtips');
    });
    $('#jsproductorkeyBtn').click(function () {
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
            alert('请切换网到http://5777')

            return;
        }
        web3 = new Web3(web3.currentProvider);
        var MyContract = new web3.eth.Contract(abi, addresss);
        MyContract.methods.vaildProducer(true).send({from: ethereum.selectedAddress, value: web3.utils.toWei('1000', 'ether')})
            .on('transactionHash', function (hash) {
            })
            .on('receipt', function (receipt) {
                alert('恭喜您成为版权发布者，后台正在处理请求，请稍等');
                window.location.reload();
            })
            .on('confirmation', function (confirmationNumber, receipt) {

            })
            .on('error', function (error, receipt) {

            })

    });
})
$(function () {
    //退出版权发布者
    $('#jsproductorexitkey').on('click', function () {
        Dml.fun.showDialog('#jsproductorkeyexitbox', '#jsproductorkeyexitboxtips');
    });
    $('#jsproductorkeyexitBtn').click(function () {
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
            alert('请切换网到http://5777')

            return;
        }
        web3 = new Web3(web3.currentProvider);
        var MyContract = new web3.eth.Contract(abi, addresss);
        MyContract.methods.vaildProducer(false).send({from: ethereum.selectedAddress})
            .on('transactionHash', function (hash) {
            })
            .on('receipt', function (receipt) {
                alert('您的押金已退回，后台正在处理请求，请稍等');
                window.location.reload();
            })
            .on('confirmation', function (confirmationNumber, receipt) {

            })
            .on('error', function (error, receipt) {

            })

    });
})
// var demofileInput = document.getElementById('jsproductorkey');
// demofileInput.addEventListener('click', function () {
//     $.ajax({
//         cache: false,
//         type: 'post',
//         url: "/users/becomeproduct/",
//         data: formdata,
//         async: true,
//         processData: false,    // 不处理数据
//         contentType: false,    // 不设置内容类型
//         success: function (data) {
//             console.log(data)
//             if (data.status == 'success') {
//                 alert('文件上传成功，ipfshash为' + data.fileHash["Hash"])
//                 return;
//             } else if (data.errormsg) {
//                 alert(data.errormsg)
//                 return;
//             }
//         }
//     });
// });

