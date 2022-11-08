jQuery(document).ready(function ($) {

    $('#content-payment').on('show.bs.collapse', function () {
        $("#content-pontos").collapse("hide")
    })
    
    $('#content-pontos').on('show.bs.collapse', function () {
        $("#content-payment").collapse("hide")
    })
    
})

$(".btn-pgto").click(function(event){
    let value = $(this).data('value')
    let input_type_value = "." + $(this).data('pagto-type')
    console.log(input_type_value)
    $(input_type_value).val(value)
})