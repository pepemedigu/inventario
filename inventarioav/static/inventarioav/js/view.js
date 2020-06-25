$(document).ready(function(){
    $('.openModal').on('click',function(){
        modal_equipos_id = "#modal-body-create-equipo-" + $(this).attr('tipo-equipos');
        modal_id = "#modal-create-equipo-tipo-" + $(this).attr('tipo-equipos');
        var dataURL = $(this).attr('data-href');
        $(modal_equipos_id).load(dataURL,function(){
            $(modal_id).modal({show:true});
        });
    });
});