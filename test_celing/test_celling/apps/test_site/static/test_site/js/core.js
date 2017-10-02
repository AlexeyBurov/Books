
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

$(document).on('submit', 'form[action="add_order"]',function () {
    var data = $(this).serialize();
    if($('input[name="dealer_id"]').val() === undefined){
        $('#error-message').html('<span>Выберите дилера</span>').fadeIn(2000,function () {
            $(this).fadeOut(600);
        })

    }else {
        $.ajax({
            type: 'POST',
            url: 'add_order',
            data: data,
            success: function (data) {
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
    $('input[name="dealer_id"]').val(dealer_id);
});


$(document).on('click', '.dealer-pdp', function(){
    let id = $(this).data('num');
    $.ajax({
        url: 'get_dealer_info',
        type: 'get',
        data:{dealer_id: id},
        success: function(data){
            console.log(data);
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
            console.log(data);
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
            console.log(result);
            let colors = JSON.parse(result.material_group.colors);
            let select = $('#material_color');
            select.html('');
            let select_materials = $('#material_select');
            select_materials.html('');
            for(let material of result.materials){
                select_materials.append($("<option></option>")
                    .attr("value",material.id)
                    .text(material.name+' '+material.celling_width));
            }
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
            console.log(dealer_info);
            $('#edit-dealer-tmpl').modal('show');
        }
    });
});


$(document).on('click', '.dealer-view',function () {
    let dealer_id = $(this).data('num');
    $.ajax({
        url: 'get_dealer_info',
        type: 'get',
        data:{dealer_id: dealer_id},
        success: function(data){
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
                    "data": 'celling_id'
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