const defaultLimit = 100;

$(document).ready(function(){


	$('#fecha_inicio, #fecha_final, #id_date_from, #id_date_to').datepicker({
		format: 'dd/mm/yy'
	}).on('changeDate', function(ev) {
		$(this).datepicker('hide');
	});

	$('#filters_accordion').on('show.bs.collapse', function () {
 		$('#filter-icon').attr('class','pull-right glyphicon glyphicon-chevron-up');
	}).on('hidden.bs.collapse', function () {
 		$('#filter-icon').attr('class','pull-right glyphicon glyphicon-chevron-down')
	});
});

function getDate(field) {
    const value = $(`#${field}`).val() || ''
    const regex = /^\d{2}\/\d{2}\/\d{2}$/
    return regex.test(value) ?  value : ''
}

/* Search CANDIDATOS */
contacktoApp.controller('SearchCandidatoCTRL', function($scope){
    $scope.candidatos = [];    

    $scope.open_empresa_modal = function(){
        $('#selectEmpresaModal').modal().on('shown.bs.modal', function(){
            $('#search-empresa').focus();
        });
    }

    $scope.get_filtros = function(){
        return {
            'nombre' : $scope.search_nombre,
            'compania_id' : $scope.compania_id,
            'compania_nombre' : $scope.compania_nombre,
            'agente_id' : $scope.agente_select ? $scope.agente_select : '',
            'status_id' : $scope.status_select,
            'limit_select' : $scope.limit_select,
            'fecha_inicio' : $scope.fecha_inicio,
            'fecha_final' : $scope.fecha_final
        }
    };

    $scope.set_filtros = function(filtros_json){
        var defaultStatus = 3;

        $scope.search_nombre = typeof filtros_json.nombre !== 'undefined' ? filtros_json.nombre : '';
        $scope.compania_id = typeof filtros_json.compania_id !== 'undefined' ? filtros_json.compania_id : '';
        $scope.compania_nombre = typeof filtros_json.compania_nombre !== 'undefined' ? filtros_json.compania_nombre : '';
        $scope.agente_select = typeof filtros_json.agente_id !== 'undefined' ? filtros_json.agente_id : '';
        $scope.status_select = typeof filtros_json.status_id !== 'undefined' ? filtros_json.status_id : defaultStatus;
        $scope.limit_select = typeof filtros_json.limit_select !== 'undefined' ? filtros_json.limit_select : defaultLimit;
        $scope.fecha_inicio = '';
        $scope.fecha_final = '';
        if (typeof filtros_json.fecha_inicio !== 'undefined'){
            /* Jquery Fix por AngularJS issue */ 
            $('#fecha_inicio').val(filtros_json.fecha_inicio)
        }
        if (typeof filtros_json.fecha_final !== 'undefined'){
            /* Jquery Fix por AngularJS issue */ 
            $('#fecha_final').val(filtros_json.fecha_final)              
        }
    };

    $scope.search = async function(){
        
        var fechaIni = '01/01/24';
        var fechaFin = '31/12/24';

        $scope.fecha_inicio = fechaIni;
        $scope.fecha_final = fechaFin;


    	var data = $scope.get_filtros();
        $('#lista-candidatos-sidebar').hide();
        $('#search-msg').html('').removeClass();
        $('#search-status').addClass('loading-ajax');

        const candidatos = await getCandidatos(data)
        $('#search-status').removeClass('loading-ajax');

        if (candidatos.length) {
            $scope.candidatos = candidatos;                                                
            $scope.$apply();
            $('#lista-candidatos-sidebar').show();                        
        } else {
            $('#search-msg').addClass('alert alert-warning').html('0 resultados, favor de intentar con otros filtros');    
        }
    };      
    
    //Esta se carga al inicio
    $scope.search_init = async function(){

        var fechaInicio = '01/01/24';
        var fechaFinal = '31/12/24';

        $scope.fecha_inicio = fechaInicio;
        $scope.fecha_final = fechaFinal;

    	var data = $scope.get_filtros();
        $('#lista-candidatos-sidebar').hide();
        $('#search-msg').html('').removeClass();
        $('#search-status').addClass('loading-ajax');

        const candidatos = await getCandidatos(data)
        $('#search-status').removeClass('loading-ajax');

        if (candidatos.length) {
            $scope.candidatos = candidatos;                                                
            $scope.$apply();
            $('#lista-candidatos-sidebar').show();                        
        } else {
            $('#search-msg').addClass('alert alert-warning').html('0 resultados, favor de intentar con otros filtros');    
        }
    };   

    $scope.load_candidato = function(id_cand){
        var url_op = '/editar'
        if (typeof is_usuario_contacto != 'undefined'){
            if (is_usuario_contacto){
                var url_op = '/ver';
            }
        }
    	window.location.replace('/candidato/investigacion/' + id_cand + url_op);
    };

    $scope.init = function(){
        $scope.set_filtros(filtros_json);
		//$scope.search();
        $scope.search_init();
    };

    $scope.limpiar_filtros = function(){
        $scope.search_nombre = '';
        $scope.compania_id = '';
        $scope.compania_nombre = '';                  
        $scope.agente_select = '';
        $scope.status_select = '0';
        $scope.limit_select = defaultLimit;
        $scope.fecha_inicio = '';
        $scope.fecha_final = '';
        $('#fecha_inicio').val('');
        $('#fecha_final').val('');
        $.post("/candidato/reset_filtros/");
    };

    $scope.init();
});

/* Search AGENTES */
contacktoApp.controller('SearchAgenteCTRL', function($scope){
    $scope.candidatos = [];
    $scope.refresh = false;
    $scope.compania_id = '';

    $scope.open_empresa_modal = function(){
            $('#selectEmpresaModal').modal().on('shown.bs.modal', function(){
                $('#search-empresa').focus();
            });
    }

     $scope.get_filtros = function(){
        return {
            'compania_id' : $scope.compania_id ? $scope.compania_id : '',
            'compania_nombre' : $scope.compania_nombre ? $scope.compania_nombre + '' : '',
            'agente_id' : $scope.agente_radio ? $scope.agente_radio : '',
            'status_id' : typeof $scope.status_select ? $scope.status_select : '',
            'fecha_inicio' : typeof $scope.fecha_inicio !== 'undefined' ? $scope.fecha_inicio : '',
            'fecha_final' : typeof $scope.fecha_final !== 'undefined' ? $scope.fecha_final : '',
        }
    };

    $scope.set_filtros = function(filtros_json){
        if (typeof filtros_json.compania_id !== 'undefined'){
            $scope.compania_id = filtros_json.compania_id;
        }
        if (typeof filtros_json.compania_nombre !== 'undefined'){
            $scope.compania_nombre = filtros_json.compania_nombre;
        }
        if (typeof filtros_json.agente_id !== 'undefined'){
            $scope.agente_radio = filtros_json.agente_id;
        }
        if (typeof filtros_json.status_id !== 'undefined'){
            $scope.status_select = filtros_json.status_id;
            if(filtros_json.status_id == ''){
                $scope.status_select = '0';
            } 
        }
        if (typeof filtros_json.fecha_inicio !== 'undefined'){
            /* Jquery Fix por AngularJS issue */
            $('#fecha_inicio').val(filtros_json.fecha_inicio)
        }
        if (typeof filtros_json.fecha_final !== 'undefined'){
            /* Jquery Fix por AngularJS issue */
            $('#fecha_final').val(filtros_json.fecha_final)
        }
    };

    $scope.validate_search = function (){
        if($scope.agente_radio){
            $scope.refresh = true;
            $scope.search();
        } else {
            showMSG('msg-search', 'Selecciona un agente.', 'alert alert-warning');
        }
    };

    $scope.search = function(){
        
        $scope.fecha_inicio = getDate('fecha_inicio')
        $scope.fecha_final = getDate('fecha_final')

        var data = $scope.get_filtros();
        $.post( "/agente/search_agentes", data , 'json').done(function( data ) {
            if (typeof data.status != 'undefined' && data.status){
                if ($scope.refresh) { 
                    window.location.replace('/agentes');
                }
           }
       });
    };

    $scope.limpiar_filtros = function(){
            $scope.compania_id = '';
            $scope.compania_nombre = '';
            $scope.agente_radio = '';
            $scope.status_select = '0';
            $('#fecha_inicio').val('');
            $('#fecha_final').val('');
            $.post("/agente/reset_filtros/");
    };

    $scope.select_agente_radio = function(val){
        $scope.agente_radio = val;
    };

    $scope.init = function(){
        $scope.status_select = '0';
        if (filtros_json !== ''){
            $scope.set_filtros(filtros_json);
        }
        $scope.search();
    };

    $scope.init();
   
});

/* Search EMPRESAS */
contacktoApp.controller('SearchEmpresaCTRL', function($scope){
    $scope.candidatos = [];
    $scope.compania_id = '';

    $scope.open_empresa_modal = function(){
            $('#selectEmpresaModal').modal().on('shown.bs.modal', function(){
                $('#search-empresa').focus();
            });
    }

    $scope.get_filtros = function(){
        return {
            'compania_nombre' : $scope.compania_nombre ? $scope.compania_nombre + '' : '',
            'es_cliente' : $scope.es_cliente ? $scope.es_cliente : '',
            'limit_select' : $scope.limit_select,
        }
    };

    $scope.set_filtros = function(filtros_json){
        if (typeof filtros_json.compania_nombre !== 'undefined'){
            $scope.compania_nombre = filtros_json.compania_nombre;
        }
        if (typeof filtros_json.es_cliente !== 'undefined' && filtros_json.es_cliente == 'true'){
            $scope.es_cliente = true;
        }
        $scope.limit_select = typeof filtros_json.limit_select !== 'undefined' ? filtros_json.limit_select : defaultLimit;
    };

    $scope.search = function(){
        var data = $scope.get_filtros();
        $.post( "/empresa/search_empresas/", data , 'json').done(function( data ) {
            if (typeof data.status != 'undefined' && data.status){
                    window.location.replace('/empresas');
           }
       });
    };

    $scope.init = function(){
        if (filtros_json !== ''){
            $scope.set_filtros(filtros_json);
        }
    };

    $scope.limpiar_filtros = function(){
            $scope.compania_nombre = '';
            $scope.es_cliente = '';
            $scope.limit_select = defaultLimit;
            $.post("/empresa/reset_filtros/");
        };

    $scope.init();
   
});

/* Search COBRANZA */
contacktoApp.controller('SearchCobranzaCTRL', function($scope){
    $scope.candidatos = [];
    $scope.compania_id = '';
    $scope.contacto_id = '';
    $scope.factura_folio_ng = '';
    $scope.empresa_contactos = [];
    $scope.agente_select = ''
    $scope.folio = ''

    $scope.open_empresa_modal = function(){
             $('#selectEmpresaModal').modal().on('shown.bs.modal', function(){
                $('#search-empresa').focus();
            });
    }

    $scope.get_filtros = function(){
        return {
            'compania_id' : $scope.compania_id ? $scope.compania_id : '',
            'compania_nombre' : $scope.compania_nombre ? $scope.compania_nombre + '' : '',
            'contacto_id' : $scope.contacto_id ? $scope.contacto_id : '',
            'factura_folio' : $scope.factura_folio_ng ? $scope.factura_folio_ng : '',
            'status_id' : typeof $scope.status_select ? $scope.status_select : '',
            'agente_select': $scope.agente_select ? $scope.agente_select : '',
            'fecha_inicio' : $scope.fecha_inicio ? $scope.fecha_inicio : '',
            'fecha_final' : $scope.fecha_final ? $scope.fecha_final : '',
            'folio' : $scope.folio ? $scope.folio : '',
        }
    };

    $scope.set_filtros = function(filtros_json){
        if (typeof filtros_json.compania_id !== 'undefined'){
            $scope.compania_id = filtros_json.compania_id;
        }
        if (typeof filtros_json.compania_nombre !== 'undefined'){
            $scope.compania_nombre = filtros_json.compania_nombre;
        }
        if (typeof filtros_json.contacto_id !== 'undefined'){
            $scope.contacto_id = filtros_json.contacto_id;
        }
        if (typeof filtros_json.factura_folio !== 'undefined'){
            $scope.factura_folio_ng = filtros_json.factura_folio;
        }
        if (typeof filtros_json.status_id !== 'undefined'){
            $scope.status_select = filtros_json.status_id;
            if(filtros_json.status_id == ''){
                $scope.status_select = '0';
            } 
        }
        if (typeof filtros_json.agente_select !== 'undefined') {
            $scope.agente_select = filtros_json.agente_select;
        }
        if (filtros_json.fecha_inicio){
            $('#fecha_inicio').val(filtros_json.fecha_inicio);
        }
        if (filtros_json.fecha_final){
            $('#fecha_final').val(filtros_json.fecha_final);
        }

        if (typeof filtros_json.folio !== 'undefined'){
            $scope.folio = filtros_json.folio;
        }
    };

    $scope.search = function(){
        $scope.fecha_inicio = getDate('fecha_inicio')
        $scope.fecha_final = getDate('fecha_final')

        var data = $scope.get_filtros();
        $.post( "/cobranza/search_cobranza/", data , 'json').done(function( data ) {
            if (typeof data.status != 'undefined' && data.status){
                window.location.replace('/cobranza/');
           }
       });
    };

    $scope.init = function(){
        $scope.status_select = '0';
        if (filtros_json !== ''){
            $scope.set_filtros(filtros_json);
            $scope.fecha_inicio = $('#fecha_inicio').val();
            $scope.fecha_final = $('#fecha_final').val();
            if($scope.compania_id.length && parseInt($scope.compania_id)){
                $scope.setEmpresaContactos()
            }
        }
    };

    $scope.limpiar_filtros = function(){
            $scope.compania_id = '';
            $scope.compania_nombre = '';
            $scope.contacto_id = '';
            $scope.factura_folio_ng = '';
            $scope.empresa_contacto = '';
            $scope.status_select = '0';
            $scope.agente_select = ''
            $scope.folio = ''
            $('#fecha_inicio').val('');
            $('#fecha_final').val('');
            $.post("/cobranza/reset_filtros/");
        };

    $scope.setEmpresaContactos = function(){
        $.get( "/api/empresa/" + $scope.compania_id + "/get_contactos", 'json').done(function( data ) {
            $('#panel_empresa_contacto').find('img').attr({'style':''}).remove();
            $scope.empresa_contactos = data;
            $scope.$apply();
        });
    }

    $scope.selectContacto = function(){
        $scope.contacto_id = $scope.empresa_contacto + '';
    }

    $scope.init();
   
});

/* Search REPORTE */
contacktoApp.controller('SearchReportesCTRL', function($scope){
    $scope.candidatos = [];
    $scope.compania_id = '';
    $scope.empresa_contactos = [];
    $scope.contactos_selected = '';
    $scope.nombre = ''
    $scope.limit_select = 50;

    $scope.open_empresa_modal = function(){
            $('#selectEmpresaModal').modal().on('shown.bs.modal', function(){
                $('#search-empresa').focus();
            });
    }

     $scope.get_filtros = function(){
        return {
            'nombre' : $scope.nombre,
            'compania_id' : $scope.compania_id ? $scope.compania_id : '',
            'compania_nombre' : $scope.compania_nombre ? $scope.compania_nombre + '' : '',
            'agente_id' : $scope.agente_select ? $scope.agente_select : '',
            'contactos_selected' : $scope.contactos_selected ? $scope.contactos_selected + '' : '',
            'status_id' : typeof $scope.status_select ? $scope.status_select : '',
            'status_laboral_id' : typeof $scope.status_laboral_select ? $scope.status_laboral_select : '',
            'fecha_inicio' : typeof $scope.fecha_inicio !== 'undefined' ? $scope.fecha_inicio : '',
            'fecha_final' : typeof $scope.fecha_final !== 'undefined' ? $scope.fecha_final : '',
            'limit_select' : $scope.limit_select ? $scope.limit_select : 50,
        }
    };

    $scope.set_filtros = function(filtros_json){
        if (typeof filtros_json.nombre !== 'undefined'){
            $scope.nombre = filtros_json.nombre;
        }
        if (typeof filtros_json.compania_id !== 'undefined'){
            $scope.compania_id = filtros_json.compania_id;
        }
        if (typeof filtros_json.contactos_selected !== 'undefined'){
            $scope.contactos_selected = filtros_json.contactos_selected;
        }
        if (typeof filtros_json.compania_nombre !== 'undefined'){
            $scope.compania_nombre = filtros_json.compania_nombre;
        }
        if (typeof filtros_json.status_id !== 'undefined'){
            $scope.status_select = filtros_json.status_id; 
        }
        if (typeof filtros_json.status_laboral_id !== 'undefined'){
            $scope.status_laboral_select = filtros_json.status_laboral_id; 
        }
        if (typeof filtros_json.fecha_inicio !== 'undefined'){
            $('#fecha_inicio').val(filtros_json.fecha_inicio);
        }
        if (typeof filtros_json.fecha_final !== 'undefined'){
            $('#fecha_final').val(filtros_json.fecha_final);
        }
        if (typeof filtros_json.limit_select !== 'undefined'){
            $scope.limit_select = filtros_json.limit_select; 
        }

        $scope.agente_select = typeof filtros_json.agente_id !== 'undefined' ? filtros_json.agente_id : '';
    };

    $scope.search = function(){
        $scope.fecha_inicio = getDate('fecha_inicio')
        $scope.fecha_final =  getDate('fecha_final')

        var data = $scope.get_filtros();
        $.post( "/estatus/search_reportes/", data , 'json').done(function( data ) {
            if (typeof data.status != 'undefined' && data.status){
                window.location.replace('/estatus');
           }
       });
    };

    $scope.init = function(){
        $scope.status_select = '';
        $scope.status_laboral_select = '';
        $scope.contactos_selected = ''
        $scope.limit_select = 50;

        if (filtros_json !== ''){
            $scope.set_filtros(filtros_json);
            $scope.fecha_inicio = ($('#fecha_inicio').val());
            $scope.fecha_final = ($('#fecha_final').val());
            if($scope.compania_id.length && parseInt($scope.compania_id)){
                $scope.setEmpresaContactos(true)
            }
        }
    };

    $scope.limpiar_filtros = function(){
        $scope.nombre = ''
        $scope.compania_id = '';
        $scope.compania_nombre = '';
        $scope.agente_select = '';
        $scope.contactos_selected = '';
        $scope.status_select = '';
        $scope.status_laboral_select = '';
        $scope.limit_select = 50;
        $('#fecha_inicio').val('');
        $('#fecha_final').val('');
        $.post("/estatus/reset_filtros/");
    };

    $scope.setEmpresaContactos = function(is_init){
        if(!is_init){
            $scope.contactos_selected = '';
        }        
        $('#panel_empresa_contacto').append($(ajaxloader).css({'position': 'absolute', 'top': '9px', 'right': '20px'}));
        $.get( "/api/empresa/" + $scope.compania_id + "/get_contactos", 'json').done(function( data ) {
            $('#panel_empresa_contacto').find('img').attr({'style':''}).remove();
            $scope.empresa_contactos = data;
            $scope.$apply();
        });
    }

    $scope.init();
   
});

/* Search BITACORA */
contacktoApp.controller('SearchBitacoraCTRL', function($scope){
    $scope.candidatos = [];
    $scope.get_filtros = function(){
        return {
            'agente_id' : $scope.agente_select ? $scope.agente_select : '',
            'fecha_inicio' : typeof $scope.fecha_inicio !== 'undefined' ? $scope.fecha_inicio : '',
            'fecha_final' : typeof $scope.fecha_final !== 'undefined' ? $scope.fecha_final : '',
        }
    };

    $scope.set_filtros = function(filtros_json){
        if (typeof filtros_json.agente_id !== 'undefined'){
            $scope.agente_select = filtros_json.agente_id;
        }
        if (typeof filtros_json.fecha_inicio !== 'undefined'){
            /* Jquery Fix por AngularJS issue */
            $('#fecha_inicio').val(filtros_json.fecha_inicio);
        }
        if (typeof filtros_json.fecha_final !== 'undefined'){
            /* Jquery Fix por AngularJS issue */
            $('#fecha_final').val(filtros_json.fecha_final);
        }
    };

    $scope.search = function(){
        $scope.fecha_inicio = getDate('fecha_inicio')
        $scope.fecha_final = getDate('fecha_final')

        var data = $scope.get_filtros();
        $.post( "/bitacora/search_bitacora/", data , 'json').done(function( data ) {
            if (typeof data.status != 'undefined' && data.status){
                window.location.replace('/bitacora');
           }
       });
    };

    $scope.init = function(){
        if (filtros_json !== ''){
            $scope.set_filtros(filtros_json);
            $scope.fecha_inicio = ($('#fecha_inicio').val());
            $scope.fecha_final = ($('#fecha_final').val());
        }
    };

    $scope.limpiar_filtros = function(){
            $scope.agente_select = '';
            $('#fecha_inicio').val('')
            $('#fecha_final').val('')
            $.post("/bitacora/reset_filtros/");
        };

    $scope.init();
   
});
