/**
 * Created by PyCharm.
 * User: chapson
 * Date: 21.09.11
 * Time: 0:57
 * To change this template use File | Settings | File Templates.
 */
jQuery(function() {
    $('.block-edit_order_item').each(function() {
        var _this = jQuery(this);
        var quantity_block = $('.block-edit_order_item__quantity', this),
            delete_block = $('.block-edit_order_item__delete', this);
        var edit_form = $('form', quantity_block),
            delete_form = $('form', delete_block);
        edit_form.submit(function(){
            var url = $(this).attr('action');
            $.ajax({url: url,
                dataType: 'json',
                type: 'post',
                data: edit_form.serialize(),
                success: function(data){}
            })
            return false;
        })
        $('input[type=text]', edit_form).keyup(function(){
            var value = $(this).val() - 0;
            if(value > 0){
                edit_form.submit()
            }
        })
        $('input[type=submit]', edit_form).hide()
        delete_form.submit(function(){
            var url = $(this).attr('action');
            $.ajax({url: url,
                dataType: 'json',
                type: 'post',
                data: edit_form.serialize(),
                success: function(data){ _this.hide('slow'); }
            })
            return false;
        })
    })
});