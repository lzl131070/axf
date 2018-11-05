$(function () {
    // 滚动条处理
    $('.market').width(innerWidth)


    typeIndex = $.cookie('typeIndex')
    console.log(typeIndex)
    if(typeIndex){
        $('.type-slider .type-item').
        eq(typeIndex).addClass('active')
    } else {
        $('.type-slider .type-item:first').addClass('active')
    }

    $('.type-item').click(function () {
        $.cookie('typeIndex', $(this).index(),{exprires:3, path:'/'})
    })

        // categoryBt.onclick = function () {
        //     // document.getElementsByClassName('bounce-view').style.display = 'block'
        // }
        var a=0

        $('#categoryBt').click(function () {
                // a=0?a=0:a=1;
                a==0?categoryshow():categoryhide();

        })
        function categoryshow() {

             $('.bounce-view.category-view').show()
            a=1
            $('#categoryBt i').removeClass('glyphicon-triangle-top').addClass('glyphicon-triangle-bottom')
            sorthide()
        }
         function categoryhide() {
             $('.bounce-view.category-view').hide()
            $('#categoryBt i').removeClass('glyphicon-triangle-bottom').addClass('glyphicon-triangle-top')

             a=0
        }
        b=0
        $('#sortBt').click(function () {
            b==0?sortshow():sorthide()
        })
        function sortshow() {
            $('.bounce-view.sort-view').show()
            b=1
            $('#sortBt i').removeClass('glyphicon-triangle-top').addClass('glyphicon-triangle-bottom')

            categoryhide()
        }
        function sorthide() {
            $('.bounce-view.sort-view').hide()
            b=0
            $('#sortBt i').removeClass('glyphicon-triangle-bottom').addClass('glyphicon-triangle-top')

        }

        // sorti=$('#sortBt i')
        // $('.bounce-view.sort-view .bounce-wrapper a').click(function () {
        //     $.cookie('sorttext',$(this).text(),{exprires: 3,path: '/'})
        // })
        // sorttext = $.cookie('sorttext')
        // if (sorttext){
        //     $('#sortBt span').text(sorttext)
        // }
        // var $cati =
        $('.bounce-view.category-view .bounce-wrapper a').click(function () {
            $.cookie('cattext',$(this).html(),{exprires: 1,path:'/'})
        })
        var catsort = $.cookie('cattext')
        if(catsort){
            var $new = '<span>'+catsort+'<i class="glyphicon glyphicon-triangle-top"></i></span>'
            // $new.html(catsort)
            // console.log($new)
            $('#categoryBt').html($new);
            // $.cookie('cattext','全部分类',{exprires:-1})
        }
        $('.type-item a').click(function () {
            $.cookie('cattext','全部分类',{exprires:1,path:'/'})
            $.cookie('sortbt','综合排序',{exprires: 1,path:'/'})
        })
        // else {
        //     var $new = '<span>'+'全部分类'+'<i class="glyphicon glyphicon-triangle-top"></i></span>'
        //     $('#categoryBt').html($new)
        // }


        var sortbt = $.cookie('sortbt')
        $('.bounce-view.sort-view .bounce-wrapper a').click(function () {
            $.cookie('sortbt',$(this).html(),{exprires: 1,path:'/'})
        })
        if(sortbt){
             var $sort = '<span>'+sortbt+'<i class="glyphicon glyphicon-triangle-top"></i></span>'
            $('#sortBt').html($sort)
        }
        // 购物车


        // 减操作
        $('.bt-wrapper .glyphicon.glyphicon-minus').click(function () {
            var a=$(this).next().html();
            a = parseInt(a)
            if(a!=0){
                $(this).next().html(a-1)
            }
        })
        $('.bt-wrapper .glyphicon.glyphicon-plus').click(function () {
            var a=$(this).prev().html();
            a = parseInt(a)

            $(this).prev().html(a+1)

        })
})