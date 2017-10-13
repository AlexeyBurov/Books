
$(document).on('click','#send_file',function (){
    var form_data = new FormData();
    form_data.append('csrfmiddlewaretoken',$('input[name="csrfmiddlewaretoken"]').val());
    form_data.append('file',$('input[type="file"]')[0].files[0]);
    $.ajax({
        type: 'POST',
        url:'save_file',
        data: form_data,
        processData: false,
        contentType: false,
        success: function(data){
            $('#order_file_form').hide();
            $('#for_add_order_form').html(data);
        }
    });

    return false;

});

$(document).on('submit','form[action="add_material_api"]', function(){
    let data = $(this).serialize();
    $.ajax({
        url: 'add_material_api',
        type: 'POST',
        data:data,
        success: function (data) {
            window.location.replace('/materials');
        }
    });
    return false;
});

$(document).on('submit', 'form[action="add_order"]',function () {
    var data = $(this).serialize();
    if($('#order_dealer_id').val() === undefined){
        $('#error-message').html('<span>Выберите дилера</span>').fadeIn(2000,function () {
            $(this).fadeOut(600);
        })

    }else {
        $.ajax({
            type: 'POST',
            url: 'add_order',
            data: data,
            success: function (data) {
                console.log(data);
                alert(data);
                window.location.href = './orders'
            }
        });
    }
    return false;
});

$(document).on('submit', 'form[action="add_dealer"]',function () {
    var data = $(this).serialize();
    $.ajax({
        type: 'POST',
        url:'add_dealer',
        data: data,
        success: function(data){
            window.location.href = './dealers';

        }
    });
    return false;
});

$(document).on('change', '#material_select', function(){
    let material_id = $(this).val();
    $('input[name="material_id"]').val(material_id);
});

$(document).on('change', '#dealer_select', function(){
    let dealer_id = $(this).val();
    $('#order_dealer_id').val(dealer_id);
});
$(document).ready(function() {
    $('#order_dealer_id').val($("#dealer_select option:first").val());
    $('#material_id').val($("#material_select option:first").val());
});
$(document).on('click', '.dealer-pdp', function(){
    let id = $(this).data('num');
    $.ajax({
        url: 'get_dealer_info',
        type: 'get',
        data:{dealer_id: id},
        success: function(data){
            $('#modal_dealer_name').html(data[0].fields.dealer_name);
            $('form[action="dealer_update"] > .modal-body > input[name="dealer_id"]').val(data[0].pk);
            $('form[action="dealer_update"] > .modal-body > input[name="dealer_name"]').val(data[0].fields.dealer_name);
            $('form[action="dealer_update"] > .modal-body > input[name="dealer_email"]').val(data[0].fields.dealer_email);
            $('form[action="dealer_update"] > .modal-body > input[name="dealer_phone"]').val(data[0].fields.dealer_phone);
            $('form[action="dealer_update"] > .modal-body > input[name="dealer_firm_name"]').val(data[0].fields.dealer_firm_name);
            $('form[action="dealer_update"] > .modal-body > input[name="dealer_unp"]').val(data[0].fields.dealer_unp);
            $('form[action="dealer_update"] > .modal-body > input[name="dealer_address"]').val(data[0].fields.dealer_address);
            $('form[action="dealer_update"] > .modal-body  #dealer_amount').html(data[0].fields.dealer_amount);
            $('#dealer-pdp-page').modal('show');
        }
    });


});


$(document).on('click', '.dealer-payment', function(){
   let btn_with_info = $(this);
   let dealer_id = btn_with_info.data('num');
   let name = btn_with_info.data('label');
   let modal_id = btn_with_info.data('target');
   $('#payment_dealer_id').val(dealer_id);
   $('#paymentModalLabel').html('Добавить платёж '+name);
});

$(document).on('submit', 'form[action="dealer_payment"]', function(){
    let data = $(this).serialize();
    $.ajax({
        url: 'dealer_payment',
        type: 'post',
        data:data,
        success: function(data){
            $('#payment-dealer-tmpl').modal('hide');
            $('#dealers-table').DataTable().ajax.reload();
        }
    });
    return false
});

$(document).on('submit','form[action="add_color"]',function () {
    let data = $(this).serialize();
    $.ajax({
        url: 'add_color_api',
        type: 'post',
        data:data,
        success: function(data){
            window.location.replace('/material_colors');
        }
    });
    return false;
});

$(document).on('change','#material_group',function () {
    let material_group_id = this.value;
    $.ajax({
        url:'material_group_info',
        data:{material_group_id: material_group_id},
        success(data){
            let result = JSON.parse(data);
            let colors = JSON.parse(result.material_group.colors);
            let select = $('#material_color');
            select.html('');
            let select_materials = $('#material_select');
            select_materials.html('');
            select_materials.append($("<option>Выберите материал</option>"));
            for(let material of result.materials){
                select_materials.append($("<option></option>")
                    .attr("value",material.id)
                    .text(material.name+' '+material.celling_width));
            }
                select.append('<option>Выберите цвет</option>')
            for(let color of colors){
                select.append($("<option></option>")
                    .attr("value",color.pk)
                    .text(color.fields.name));
            }

        }
    })
});

$(document).on('click', '.dealer-delete', function () {
   let dealer_id = $(this).data('num');
   $.ajax({
       url: 'delete_dealer',
       type: 'post',
       data: {dealer_id: dealer_id,csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()},
       success: function (data) {
           $('#dealers-table').DataTable().ajax.reload();
       }
   });
});

$(document).on('click','.dealer-edit', function(){
    let dealer_id = $(this).data('num');
    $.ajax({
        url: 'get_dealer_info',
        type: 'get',
        data:{dealer_id: dealer_id},
        success: function(data){
            let dealer_info = JSON.parse(data.dealer);
            if(dealer_info.for_remove){
                $('input[name="for_remove"]').attr('checked','checked');
            }else{
                 $('input[name="for_remove"]').removeAttr('checked');
            }
            $('#edit_dealer_id').val(dealer_info.id);
            $('#dealer_add_discount').data('num',dealer_info.id);
            $('#view_add_discount').data('num', dealer_info.id);
            $('input[name="dealer_name"]').val(dealer_info.dealer_name);
            $('input[name="dealer_phone"]').val(dealer_info.dealer_phone);
            $('input[name="dealer_email"]').val(dealer_info.dealer_email);
            $('input[name="dealer_address"]').val(dealer_info.dealer_address);
            $('input[name="dealer_firm"]').val(dealer_info.dealer_firm_name);
            $('input[name="dealer_unp"]').val(dealer_info.dealer_unp);
            $('input[name="dealer_amount"]').val(dealer_info.dealer_amount);
            $('input[name="dealer_max_depozit"]').val(dealer_info.max_depozit);
            $('#edit-dealer-tmpl').modal('show');
        }
    });
});

$(document).on('click','.dealer-discount', function () {
    let dealer_id = $(this).data('num');
    $('#add_discount-tmpl').modal('show');
    $('#discount_dealer_id').val(dealer_id);
    return false;
});

$(document).on('submit', 'form[action="add_discount"]', function () {
    let data = $(this).serialize();
    $.ajax({
        url: 'add_discount',
        type: 'post',
        data: data,
        success: function(data){
            $('#add_discount-tmpl').modal('hide');
        }

    });
    return false;
});

$(document).on('click','.dealer-discounts', function () {
    let dealer_id = $(this).data('num');
    let discount_view = $('#discount_view');
    $.ajax({
       url:'get_discounts_for_dealer',
       data:{dealer_id:dealer_id},
       success: function (data) {
           let discounts = JSON.parse(data);
           let discount_view = $('#discount_view');
           discount_view.html('');
           for (let discount of discounts){
               discount_view.append(
                $('<form class="discount" action="edit_discount" style="width:100%; display: -webkit-inline-box;margin-top:5px;margin-bottom: 5px"></form>').
                    append($('<input type="hidden" name="csrfmiddlewaretoken">').val($('input[name="csrfmiddlewaretoken"]').val())).
                    append('<input name="discount_id" type="hidden" value="'+discount.id+'">').
                        append('<label style="margin-right:15px;margin-bottom:0;margin-top:5px;vertical-align: middle" for="discount_price">'+discount.material.name+'</label>').
                            append('<input class="form-control" name="discount_price" id="discount_price" value="'+discount.discount+'" style="width:70%;clear: both">')
                                .append('<p style="margin-left:10px"><button type="submit" class="btn btn-success btn-xs discount" style="display: inline-block"><span class="glyphicon glyphicon-plus"></span></button></p>'));
           }
           $('#discounts-tmpl').modal('show');

       }
    });

    return false;
});

$(document).on('click','.discount',function(){
    let data = $(this).parent().parent().serialize();
    $.ajax({
        url: 'edit_discount',
        type: 'post',
        data: data,
        success: function (data){
            console.log(data);
        }
    });
    return false;
});

$(document).on('click', '.dealer-view',function () {
    let dealer_id = $(this).data('num');
    $.ajax({
        url: 'get_dealer_info',
        type: 'get',
        data:{dealer_id: dealer_id},
        success: function(data){
            $('#for_dealers_orders').html('<table id="dealers-orders-table">'+
                        '<thead>'+
                            '<td>id</td>'+
                            '<td>Матреиал</td>'+
                            '<td>Площадь потолка</td>'+
                            '<td>Периметр потолка</td>'+
                            '<td>Периметр гарпуна</td>'+
                            '<td>Периметр кривых</td>'+
                            '<td>Статус заказа</td>'+
                            '<td>Стоймость</td>'+
                        '</thead>'+
                        '<tfoot>'+
                            '<td>id</td>'+
                            '<td>Матреиал</td>'+
                            '<td>Площадь потолка</td>'+
                            '<td>Периметр потолка</td>'+
                            '<td>Периметр гарпуна</td>'+
                            '<td>Периметр кривых</td>'+
                            '<td>Статус заказа</td>'+
                            '<td>Стоймость</td>'+
                        '</tfoot>'+
                    '</table>');
            let dealer_info = JSON.parse(data.dealer);
            $('#viewModalLabel').html(dealer_info.dealer_name);
            $('#view_dialer_id').html(dealer_info.id);
            $('#view_dialer_name').html(dealer_info.dealer_name);
            $('#view_dialer_phone').html(dealer_info.dealer_phone);
            $('#view_dialer_email').html(dealer_info.dealer_email);
            $('#view_dialer_firm').html(dealer_info.dealer_firm_name);
            $('#view_dialer_address').html(dealer_info.dealer_address);
            $('#view_dialer_unp').html(dealer_info.dealer_unp);
            $('#view_dialer_amount').html(dealer_info.dealer_amount);
            $('#view-dealer-tmpl').modal('show');
            $('#dealers-orders-table').DataTable({
                data: data.orders,
                "columns": [{
                    "data": 'id'
                }, {
                    "data": function (row, type, val, meta) {
                        return row.celling.name
                    }
                }, {
                    "data": 's_celling'
                }, {
                    "data": 'p_celling'
                }, {
                    "data": 'p_garpun'
                }, {
                    "data": 'p_curve'
                }, {
                    "data": 'order_status'
                }, {
                    "data": 'celling_price'
                }]
            })
        }
    });
    return true;
});


$(document).on('submit', 'form[action="add_material_group"]', function(){
    let data = $(this).serialize();
    $.ajax({
        url: 'add_material_group_api',
        type: 'POST',
        data: data,
        success: function(data){
            window.location.replace('/material_groups');
        }
    });
    return false;
});

$(document).on('submit','form[action="dealer_edit"]', function(){
    let data = $(this).serialize();
    $.ajax({
        url: 'dealer_edit_api',
        type: 'POST',
        data: data,
        success: function (data) {
            $('#edit-dealer-tmpl').modal('hide');
            $('#dealers-table').DataTable().ajax.reload();

        }
    });
    return false;
});

$(document).on('click', '.color-delete', function () {
    let data = $(this).data('num');
    $.ajax({
       url: 'delete_color',
       type: 'post',
       data: {'color_id': data, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()},
        success: function(result){
            $('#colors-table').DataTable().ajax.reload();
        }

    });
});

$(document).on('click', '.group-delete', function () {
    let material_group = $(this).data('num');
    $.ajax({
        url: 'delete_material_group',
        type: 'post',
        data: {'material_group': material_group, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()},
        success: function (result){
            $('#materials_group_table').DataTable().ajax.reload();
        }
    });

});
$(document).on('click', '.group-edit', function () {
    let material_group = $(this).data('num');
    $.ajax({
        url: 'material_group_info',
        type: 'get',
        data: {material_group_id:material_group},
        success: function(result){
            let data = JSON.parse(result);
            let colors = JSON.parse(data.material_group.colors);
            let selected_colors = colors.map(function(val){
                return val.pk.toString();
            });
            $('#edit_material_group_id').val(data.material_group.id);
            $('input[name="material_group_name"]').val(data.material_group.name);
            $('input[name="default_price"]').val(data.material_group.default_price);


            $('#materials_group_edit_tmpl').modal('show');
            $('select[name="colors"]').val(selected_colors);
        }
    })
});


$(document).on('click', '.material-delete', function(){
    let material_id = $(this).data('num');
    $.ajax({
        url: 'delete_material',
        type: 'post',
        data: {'material_id': material_id, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()},
        success: function (result){
            $('#materials_table').DataTable().ajax.reload();
        }
    });
    return false;
});

$(document).on('click', '.material-edit', function(){
    let material_id = $(this).data('num');
    $.ajax({
        url: 'get_material_json',
        data: {material_id:material_id},
        success: function(result){
            let data = JSON.parse(result);
            $('#edit_material_id').val(data.id);
            $('input[name="material_name"]').val(data.name);
            $('input[name="celling_width"]').val(data.celling_width);
            $('input[name="material_price"]').val(data.price);
            $('input[name="count_meters_pagon"]').val(data.count_meters_pagon);
            $('select[name="material_group"]').val(data.material_group.id);
            $('#materials_edit_tmpl').modal('show');
        }
    });

    return false;
});

$(document).on('submit', 'form[action="edit_material"]', function(){
    let data = $(this).serialize();
    $.ajax({
        url: 'edit_material',
        type: 'post',
        data: data,
        success: function(result){
            $('#materials_edit_tmpl').modal('hide');
            $('#materials_table').DataTable().ajax.reload();
        }
    });
    return false;
});

$(document).on('submit', 'form[action="edit_material_group"]', function(){
    let data = $(this).serialize();
    $.ajax({
        url: 'edit_material_group',
        type: 'post',
        data: data,
        success: function(result){
            $('#materials_group_table').DataTable().ajax.reload();
            $('#materials_group_edit_tmpl').modal('hide');

        }
    });
    return false;
});

$(document).on('click', '.order-delete', function(){
    let order_id = $(this).data('num');
    $.ajax({
        url: 'delete_order',
        type: 'post',
        data: {order_id: order_id, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()},
        success: function(result){
            console.log(result);

            $('#orders-table').DataTable().ajax.reload();
        }
    });
    return false;
});

$(document).on('click', '.order-edit', function(){
   let order_id = $(this).data('num');
   $.ajax({
       url: 'order_info',
       data: {order_id: order_id},
       success: function(result){
           let data = JSON.parse(result);
           $('#material_group').val()
           $('#order_edit_tmpl').modal('show');
           console.log(data);
       }
   });

});