$(function () {
    $('.cart').width(innerWidth)
    if($('.goods .confirm-wrapper .glyphicon-ok').length == $('.goods').length){
        $('.bill-left .all').attr('isall','true')
        $('.bill-left .all span').removeClass('no').addClass('glyphicon glyphicon-ok')
    }

    // 总计
    total()

    // 商品 选中 状态
    $('.cart .confirm-wrapper').click(function () {
        var isid = $(this).attr('isid')
        var $that = $(this)

        $.get('/checkone/', {'isid':isid}, function (response) {
            console.log(response.isselect)
            if (response.status == 1){
                var isselect = response.isselect
                $that.attr('isselect', isselect)

                if (isselect){
                    $that.find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
                } else {    // 未选中
                    $that.find('span').addClass('no').removeClass('glyphicon glyphicon-ok')
                }
                if($('.goods .confirm-wrapper .glyphicon-ok').length == $('.goods').length){
        $('.bill-left .all').attr('isall','true')
        $('.bill-left .all span').removeClass('no').addClass('glyphicon glyphicon-ok')
    } else {
        $('.bill-left .all span').addClass('no').removeClass('glyphicon glyphicon-ok')
        $('.bill-left .all').attr('isall','false')


                }
                // 总计
                total()
            }
        })
    })

    // 全选/取消全选
    $('.cart .bill .all').click(function () {
        var isall = $(this).attr('isall');
        isall = (isall == 'false') ? true : false;
        $(this).attr('isall', isall);
        console.log(isall);
        // 自身状态

        if (isall){ // 全选
            $(this).find('span').removeClass('no').addClass('glyphicon glyphicon-ok');
        } else {    // 取消全选
            $(this).find('span').addClass('no').removeClass('glyphicon glyphicon-ok');
        };


        // 发起ajax请求
        $.get('/checkall/', {'isall':isall}, function (response) {

            if (response.status == 1){
                // 遍历
                $('.confirm-wrapper').each(function () {
                    $(this).attr('isselect', isall)
                    $(this).children().remove()
                    if (isall){ // 选中
                        $(this).append('<span class="glyphicon glyphicon-ok"></span>')
                    } else {    // 未选中
                        $(this).append('<span class="no"></span>')
                    }
                })

                // 总计
                total()
            }
        })
    })

    // 计算总数
    function total() {
        var sum = 0

        // 遍历
        $('.goods').each(function () {
            var $confirm = $(this).find('.confirm-wrapper')
            var $content = $(this).find('.content-wrapper')

            if ($confirm.find('.glyphicon-ok').length){
                var price = $content.find('.price').attr('str')
                var num = $content.find('.num').attr('str')
                sum += num * price
            }
        })

        $('.bill .total b').html(sum)
    }


    // 下单
    $('#generate-order').click(function () {
        $.get('/axf/generateorder/', function (response) {
            console.log(response)
            if (response['status'] == '1'){ // 订单详情(付款)
                var orderid = response['orderid']
                window.open('/axf/orderinfo/?orderid='+orderid, target='_self')
            }
        })
    })
})