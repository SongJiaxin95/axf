function MarketType(typeid) {
    $.ajax({
        type:"get",
        url:'/axf/markettype/',
        data:{'typeid': typeid},
        dataType:'json',
        success:function(msg){
            var goods = JSON.parse(msg.goods);
            var childtypenames = msg.childtypenames;
            $('#show_goods').empty();
            $('#all_types_container>div').empty();
            for(var i = 0; i < goods.length;i++){
                var s1 = '<li><a href="#"><img src="'+goods[i].fields.productimg+'"><div class="shoppingInfo"><h6>'+goods[i].fields.productlongname+'</h6><p class="detailTag"><span>精选</span><span>热销中</span></p><p class="unit"></p><p class="price"><span>¥'+goods[i].fields.price+'</span><s>¥'+goods[i].fields.marketprice+'</s></p></div></a><section><button onclick="subShop('+goods[i].pk+')">-</button><span id="num_'+goods[i].pk+'">0</span><button onclick="addShop('+goods[i].pk+')" >+</button></section></li>'
                $('#show_goods').append(s1)
            }
            for(var i = 0; i < childtypenames.length;i++){
                var s2 = '<a onclick="Market_ChildType_Order('+typeid+','+childtypenames[i][1]+',1)"><span id="childtype_'+childtypenames[i][1]+'">'+childtypenames[i][0]+'</span></a>'
                $('#all_types_container>div').append(s2)
            }
            var orderall = $('#sort_container>div>a');
            for(var i = 1; i < 5;i++) {
                orderall.eq(i-1).attr('onclick', 'Market_ChildType_Order(' + typeid + ',0,' + i + ')')
            }
            $('.yellowSlide').remove();
            $('#typeid_'+typeid).append('<span class="yellowSlide"></span>')
            $('#sort_rule>span').html('综合排序<span id="sort_rule_logo" class="glyphicon glyphicon-chevron-down"></span>')
            $('#all_types>span').html('全部类型<span id="all_type_logo" class="glyphicon glyphicon-chevron-down"></span>')
        },
        error:function (msg) {
            alert('请求错误')
        }
    });
}

function Market_ChildType_Order(typeid,childcid,order) {
    $.ajax({
        type:"get",
        url:'/axf/market_childtype_order/',
        data:{'typeid': typeid,'childcid':childcid,'order':order},
        dataType:'json',
        success:function(msg){
            var goods = JSON.parse(msg.goods);
            $('#show_goods').empty();
            for(var i = 0; i < goods.length;i++){
                var s1 = '<li><a href="#"><img src="'+goods[i].fields.productimg+'"><div class="shoppingInfo"><h6>'+goods[i].fields.productlongname+'</h6><p class="detailTag"><span>精选</span><span>热销中</span></p><p class="unit"></p><p class="price"><span>¥'+goods[i].fields.price+'</span><s>¥'+goods[i].fields.marketprice+'</s></p></div></a><section><button onclick="subShop('+goods[i].pk+')">-</button><span id="num_'+goods[i].pk+'">0</span><button onclick="addShop('+goods[i].pk+')" >+</button></section></li>'
                $('#show_goods').append(s1)
            }
            var childtypeall = $('#all_types_container>div>a');
            var onclickstr = '';
            for(var i = 0; i < childtypeall.length;i++){
                if (i == 0) {
                    onclickstr = childtypeall.eq(i).attr('onclick');
                    childtypeall.eq(i).attr('onclick',onclickstr.substr(0,32)+order+')')
                }else {
                    onclickstr = childtypeall.eq(i).attr('onclick');
                    childtypeall.eq(i).attr('onclick', onclickstr.substr(0, 37) + order + ')')
                }
            }
            var orderall = $('#sort_container>div>a');
            for(var i = 1; i < 5;i++) {
                orderall.eq(i-1).attr('onclick', 'Market_ChildType_Order(' + typeid + ','+childcid+','+i+')')
            }
            $('#sort_rule>span').html($('#order_'+order).html()+'<span id="sort_rule_logo" class="glyphicon glyphicon-chevron-down"></span>')
            $('#all_types>span').html($('#childtype_'+childcid).html()+'<span id="all_type_logo" class="glyphicon glyphicon-chevron-down"></span>')
        },
        error:function (msg) {
            alert('请求错误')
        }
    });
}

function addShop(goods_id){
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type:"post",
        url:'/axf/addgoods/',
        data:{'goods_id': goods_id},
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function(msg){
            $('#num_'+goods_id).html(msg.c_num);
            $('#totalprice').html('总价:'+msg.total);
            if(!($('#changeselect_'+goods_id+'>span').html())){
                cartchangeselect(goods_id)
            }
        },
        error:function (msg) {
            alert('请求错误')
        }
    });
}

function subShop(goods_id){
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type:"post",
        url:'/axf/subgoods/',
        data:{'goods_id':goods_id},
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function(msg){
            $('#num_'+goods_id).html(msg.c_num);
            $('#totalprice').html('总价:'+msg.total)
        },
        error:function (msg) {
            alert('请求错误')
        }
    });
}
function cartchangeselect(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type:"post",
        url:'/axf/changecartselect/',
        data:{'goods_id':goods_id},
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function(msg){
            if(msg.is_select){
                s = '<span>√</span>'
            }
            else{
                s = '<span></span>'
            }
            $('#changeselect_'+goods_id).html(s);
            $('#totalprice').html('总价:'+msg.total);
            is_selectAll()
        },
        error:function (msg) {
            alert('请求错误')
        }
    })
}

function selectAll(){
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var is_selectall = $('#all_select>span>span').html();
    $.ajax({
        type:"post",
        url:'/axf/changecartselectall/',
        data:{'is_selectall':is_selectall},
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function(msg){
            $('#totalprice').html('总价:'+msg.total);
            if(is_selectall=='√'){
                $('#all_select>span').html('<span></span>');
                var is_select_spans = $('.single-select');
                for(var i = 0;i < is_select_spans.length;i++){
                    is_select_spans.eq(i).html('<span></span>')
                }
            }
            else {
                $('#all_select>span').html('<span>√</span>');
                var is_select_spans = $('.single-select');
                for(var i = 0;i < is_select_spans.length;i++){
                    is_select_spans.eq(i).html('<span>√</span>')
                }
            }
        },
        error:function (msg) {
            alert('请求错误')
        }
    });
}

function is_selectAll() {
    var flag = true;
    var is_select_spans = $('.single-select>span');
    for(var i=0;i < is_select_spans.length;i++){
        if(!is_select_spans.eq(i).html()){
            flag = false
        }
    }
    if(is_select_spans.length == 0){
        flag = false
    }
    if(flag){
        $('#all_select>span').html('<span>√</span>')
    }
    else {
        $('#all_select>span').html('<span></span>')
    }
}
$(function () {
    is_selectAll()
})
