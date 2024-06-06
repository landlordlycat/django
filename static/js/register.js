$(function () {
    function bindCaptcha() {
        $('#captcha-btn').click(function (e) {
        let $this = $(this)
        let email = $("input[name='email']").val()
        if (!email) {
            alert("Please enter your email address")
            return;
        }

        $.ajax({
            url: `/auth/captcha?email=${email}`,
            type: 'get',
            success: function (data) {
                if (data.success) {
                alert("验证码已发送到您的邮箱，请查收")
                }
            }
        })

        //
        $this.off('click')
        let countdown = 60
        let timer = setInterval(function () {
            if (countdown <= 0) {
                $this.text("获取验证码")
                clearInterval(timer)
                bindCaptcha()
            } else {
                countdown--
                $this.text("重新发送(" + countdown + ")")
            }
        }, 1000)
    })
    }

    bindCaptcha()
})