$(document).ready(function(){
	$('#fecha_inicio, #fecha_final').datepicker({
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

    $scope.search = function(){
    	/* Jquery Fix por AngularJS issue */
    	$scope.fecha_inicio = ($('#fecha_inicio').val());
		$scope.fecha_final = ($('#fecha_final').val());
        /* Jquery Fix END */
    	var data = $scope.get_filtros();
        $('#lista-candidatos-sidebar').hide();
        $('#search-msg').html('').removeClass();
        $('#search-status').addClass('loading-ajax');
		$.post( "/candidato/search_candidatos/", data , 'json').done(function( data ) {
            $('#search-status').removeClass('loading-ajax');
			if (typeof data.status != 'undefined' && data.status){
                if(data.candidatos.length){
                    $scope.candidatos = data.candidatos;                                                
                    $scope.$apply();
                    $('#lista-candidatos-sidebar').show();                        
                }else{
                    $('#search-msg').addClass('alert alert-warning').html('0 resultados, favor de intentar con otros filtros');    
                }
				
            }                
	   });
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
		$scope.search();
    };

    $scope.limpiar_filtros = function(){
        $scope.search_nombre = '';
        $scope.compania_id = '';
        $scope.compania_nombre = '';                  
        $scope.agente_select = '';
        $scope.status_select = '0';
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
        /* Jquery Fix por AngularJS issue */
        $scope.fecha_inicio = ($('#fecha_inicio').val());
        $scope.fecha_final = ($('#fecha_final').val());
        var data = $scope.get_filtros();
        $.post( "/agente/search_agentes/", data , 'json').done(function( data ) {
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
        }
    };

    $scope.set_filtros = function(filtros_json){
        if (typeof filtros_json.compania_nombre !== 'undefined'){
            $scope.compania_nombre = filtros_json.compania_nombre;
        }
        if (typeof filtros_json.es_cliente !== 'undefined' && filtros_json.es_cliente == 'true'){
            $scope.es_cliente = true;
        }
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
    };

    $scope.search = function(){
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
            if($scope.compania_id.length && parseInt($scope.compania_id)){
                $scope.setEmpresaContactos()
            }
        }
        $scope.setFacturaFolios();
    };

    $scope.limpiar_filtros = function(){
            $scope.compania_id = '';
            $scope.compania_nombre = '';
            $scope.contacto_id = '';
            $scope.factura_folio_ng = '';
            $scope.folios_facturas = [];
            $scope.empresa_contacto = '';
            $scope.status_select = '0';
            $.post("/cobranza/reset_filtros/");
            $scope.setFacturaFolios();
        };

    $scope.setEmpresaContactos = function(){
        $.get( "/api/empresa/" + $scope.compania_id + "/get_contactos", 'json').done(function( data ) {
            $('#panel_empresa_contacto').find('img').attr({'style':''}).remove();
            $scope.empresa_contactos = data;
            $scope.$apply();
        });
        $scope.setFacturaFolios();
    }

    $scope.selectContacto = function(){
        $scope.contacto_id = $scope.empresa_contacto + '';
        $scope.setFacturaFolios();
    }

    $scope.setFacturaFolios = function(){
        var url = "/cobranza/get_facturas"
        if ($scope.compania_id.length && parseInt($scope.compania_id)){
            url += '/compania/' + $scope.compania_id;
        }   
        if ($scope.contacto_id.length && parseInt($scope.contacto_id)){
            url += '/contacto/' + $scope.contacto_id;
        }
        $.get( url, 'json').done(function( data ) {
            $('#panel_empresa_contacto').find('img').attr({'style':''}).remove();
            $scope.folios_facturas = data.facturas ? data.facturas : '';
            if (!($scope.folios_facturas.indexOf($scope.factura_folio_ng.toString()) > -1) && $scope.factura_folio_ng.toString() != 'por-facturar' ){
                $scope.factura_folio_ng = '';
            }
           
            $scope.$apply();
            
        });
    }
    $scope.init();
   
});

/* Search REPORTE */
contacktoApp.controller('SearchReportesCTRL', function($scope){
    $scope.candidatos = [];
    $scope.compania_id = '';
    $scope.empresa_contactos = [];
    $scope.empresa_contacto = '';
    $scope.search_nombre = ''

    $scope.open_empresa_modal = function(){
            $('#selectEmpresaModal').modal().on('shown.bs.modal', function(){
                $('#search-empresa').focus();
            });
    }

     $scope.get_filtros = function(){
        return {
            'nombre' : $scope.search_nombre,
            'compania_id' : $scope.compania_id ? $scope.compania_id : '',
            'compania_nombre' : $scope.compania_nombre ? $scope.compania_nombre + '' : '',
            'contacto_id' : $scope.empresa_contacto ? $scope.empresa_contacto + '' : '',
            'status_id' : typeof $scope.status_select ? $scope.status_select : '',
            'fecha_inicio' : typeof $scope.fecha_inicio !== 'undefined' ? $scope.fecha_inicio : '',
            'fecha_final' : typeof $scope.fecha_final !== 'undefined' ? $scope.fecha_final : '',
        }
    };

    $scope.set_filtros = function(filtros_json){
        if (typeof filtros_json.search_nombre !== 'undefined'){
            $scope.search_nombre = filtros_json.search_nombre;
        }
        if (typeof filtros_json.compania_id !== 'undefined'){
            $scope.compania_id = filtros_json.compania_id;
        }
        if (typeof filtros_json.contacto_id !== 'undefined'){
            $scope.empresa_contacto = filtros_json.contacto_id;
        }
        if (typeof filtros_json.compania_nombre !== 'undefined'){
            $scope.compania_nombre = filtros_json.compania_nombre;
        }
        if (typeof filtros_json.status_id !== 'undefined'){
            $scope.status_select = filtros_json.status_id;
            if(filtros_json.status_id == ''){
                $scope.status_select = '0';
            } 
        }
        if (typeof filtros_json.fecha_inicio !== 'undefined'){
            $('#fecha_inicio').val(filtros_json.fecha_inicio);
        }
        if (typeof filtros_json.fecha_final !== 'undefined'){
            $('#fecha_final').val(filtros_json.fecha_final);
        }
    };

    $scope.search = function(){
        $scope.fecha_inicio = ($('#fecha_inicio').val());
        $scope.fecha_final = ($('#fecha_final').val());
        var data = $scope.get_filtros();

        $.post( "/estatus/search_reportes/", data , 'json').done(function( data ) {
            if (typeof data.status != 'undefined' && data.status){
                window.location.replace('/estatus');
           }
       });
    };

    $scope.init = function(){
        $scope.status_select = '0';
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
            $scope.compania_id = '';
            $scope.compania_nombre = '';
            $scope.empresa_contacto = '';
            $scope.status_select = '0';
            $('#fecha_inicio').val('');
            $('#fecha_final').val('');
            $.post("/estatus/reset_filtros/");
        };

    $scope.setEmpresaContactos = function(is_init){
        if(!is_init){
            $scope.empresa_contacto = '';
        }        
        $('#panel_empresa_contacto').append($(ajaxloader).css({'position': 'absolute', 'top': '9px', 'right': '20px'}));
        $.get( "/api/empresa/" + $scope.compania_id + "/get_contactos", 'json').done(function( data ) {
            $('#panel_empresa_contacto').find('img').attr({'style':''}).remove();
            $scope.empresa_contactos = data;
            $scope.$apply();
            $scope.isSameContact();
        });
    }

    $scope.isSameContact = function(){
        $('#msg_enviar_reporte').html('').removeClass();
        if( typeof filtros_json['contacto_id'] != 'undefined' && filtros_json['contacto_id'] == $('#empresa_contacto').val() ){
            $('#panel_enviar_reporte').show();
        }
        else{
            $('#panel_enviar_reporte').hide();
        }
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
        /* Jquery Fix por AngularJS issue */
        $scope.fecha_inicio = ($('#fecha_inicio').val());
        $scope.fecha_final = ($('#fecha_final').val());
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
