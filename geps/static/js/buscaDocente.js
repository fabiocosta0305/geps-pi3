<script type="text/javascript">
    jQuery(document).ready(function(){
        var dados = jQuery( this ).serialize();
	    jQuery.ajax({
	        type: "POST",
            url: "",
	        cache: false,
	        data: dados,
	        success: function( data ) {
	            $("#results").empty();
                var result  = data.split('\\//');
                for(var i=0;i<result.length;i++){
                    var dados  = result[i];
                }
            }
        });
        return false;
    });
    $(document).ready(function() {
        $("#b1").click(function(){
            alert("OK!");
            $("#nome-docente").html('You clicked the button');
        });
    });

    $(function () {
        $('#nome-docente1').on('change', function () {
            var matricula = $(this).val();
            var tagIdNomeFuncionario = $('#funcionario_nome');
            var nomeFuncionario = '<p></p>';
            $.ajax({
                url: '/get_funcionario_name',
                type: 'GET',
                data: {
                    'matricula': matricula
                },
            }).fail(function(jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).done(function (data) {
                if(!data.hasOwnProperty('error')){
                    console.log(data);
                    nomeFuncionario += data['nomeDoSeuObjetoDeFuncionarios'][0]['nomeDoCampoQuePossuioNomeDoFuncionario'];
                }
            }).always( function(data){
                tagIdNomeFuncionario.html(nomeFuncionario);
            });
        });
    });
</script>