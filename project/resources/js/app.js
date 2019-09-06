angular.module('listCandidatosFilters', []).filter('setClass', function() {
    return function(current_id) {
        return (typeof candidato_seleccionado_id != 'undefined' && candidato_seleccionado_id == current_id) ? ' active' : '';
    };
});

var contacktoApp = angular.module('contacktoApp', ['listCandidatosFilters']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

controllers = {};

contacktoApp.controller('CandidatoCTRL', function($scope) {
    /* Jquery fix por issue con datepicker+angular */
    $('#id_origen-fecha').datepicker({
        format: 'dd/mm/yyyy'
    }).on('changeDate', function(ev) {
        set_edad();
    });

    $('#id_origen-fecha').change(function() {
        set_edad();
    });

    function set_edad() {
        var fecha_nac = $('#id_origen-fecha').val();
        if (fecha_nac) {
            var bits = fecha_nac.split('/');
            var edad = calculateAge(bits[1], bits[0], bits[2]);
            $('#id_candidato-edad').val(edad);
        }
    }
    /* end fix */

    $scope.existencia = false;
    $scope.compania = '';
    $scope.compania_nombre_trayectoria = '';

    $scope.save = function() {
        $('#msg').html('');
        $('#action').val('1');
        $('#form_candidato_crear').submit();
    }

    $scope.unset_compania_id = function() {
        $('#id_compania').val('');
    }

    $scope.unset_candidato_existente = function() {
        $scope.nss = '';
        $scope.curp = '';
        $scope.id_candidato = '';
    }

    $scope.validate_candidate = function() {
      if (!$scope.investigacion_id) {
        // valid nss has 11 characters
        // valid has curp 16 characters
        if (($scope.nss && $scope.nss.length > 8) || ($scope.curp && $scope.curp.length > 12)) {
            var data = {
                'nss': $scope.nss,
                'curp': $scope.curp,
                'investigacion_id': $scope.investigacion_id
            };
            $scope.id_candidato = "";
            $.post("/candidato/existencia/", data, 'json').done(function(data) {
                if (typeof data.status != 'undefined' && data.status) {
                    $scope.candidatos_existentes = data.candidatos;
                    $scope.$apply();
                    $('#existenciaCandidato').modal();
                }
            });
        }
      }
    }

    $scope.contacto_data = [];

    $scope.getContactsFromCompany = function() {

        var url = '/empresa/' + $scope.compania + '/get_contactos';
        if (typeof($scope.investigacion_id) != 'undefined') {
            url += '/' + $scope.investigacion_id;
        }
        $.get(url).done(function(data) {
            if (typeof data.status != 'undefined' && data.status) {
                $scope.contacto_data = data.contactos;
                $scope.$apply();
                $('#id_investigacion-contacto').val($scope.contacto)
            }
        });
    }

    $scope.init = function() {
        $scope.nss = $('#id_candidato-nss').val();
        $scope.curp = $('#id_candidato-curp').val();
        $scope.contacto = $('#contacto_id').val();
        $scope.empresas_select_modal = [];
        $scope.investigacion_id = $('#investigacion_id').val();

        if (empresas_select !== '') {
            $scope.empresas_select_modal = empresas_select;
        }

        if (compania_instancia_id !== '') {
            $scope.compania = compania_instancia_id;
            $scope.compania_nombre = compania_instancia_nombre;
            $scope.getContactsFromCompany();
        }
    }

    $scope.open_empresa_modal = function() {
        $('#selectEmpresaFormaModal').modal().on('shown.bs.modal', function() {
            $('#search-empresa-forma').focus();
        });
    };

    $scope.set_empresa = function(empresa_id, empresa_nombre) {
        $scope.compania = empresa_id;
        $scope.compania_nombre = empresa_nombre;
        $scope.getContactsFromCompany();
        $('#selectEmpresaFormaModal').modal('hide');
    };

    $scope.init();
});

contacktoApp.controller('CandidatoNuevaInvCTRL', function($scope) {
    $scope.existencia = false;
    $scope.compania = '';
    $scope.compania_nombre_trayectoria = '';

    $scope.save = function() {
        $('#msg').html('');
        $('#action').val('1');
        $('#form_candidato_crear').submit();
    }

    $scope.unset_compania_id = function() {
        $('#id_compania').val('');
    }

    $scope.unset_candidato_existente = function() {
        $scope.nss = '';
        $scope.curp = '';
        $scope.id_candidato = '';
    }

    $scope.validate_candidate = function() {
        var data = {
            'nss': $scope.nss,
            'curp': $scope.curp
        };
        if (data.curp >= 18) {
            $scope.id_candidato = "";
            $.post("/candidato/existencia/", data, 'json').done(function(data) {
                if (typeof data.status != 'undefined' && data.status) {
                    $scope.candidatos_existentes = data.candidatos;
                    $scope.$apply();
                    $('#existenciaCandidato').modal();
                }
            });
        }
    }

    $scope.contacto_data = [];

    $scope.getContactsFromCompany = function() {
        $.get("/empresa/" + $scope.compania + "/get_contactos").done(function(data) {
            if (typeof data.status != 'undefined' && data.status) {
                $scope.contacto_data = data.contactos;
                $scope.$apply();
                $('#id_investigacion-contacto').val($scope.contacto)
            }
        });
    }

    $scope.init = function() {
        $scope.nss = $('#id_candidato-nss').val();
        $scope.curp = $('#id_candidato-curp').val();
        $scope.contacto = $('#contacto_id').val();
        $scope.empresas_select_modal = [];
        if (empresas_select_forma !== '') {
            $scope.empresas_select_modal = empresas_select_forma;
        }

        if (compania_instancia_id !== '') {
            $scope.compania = compania_instancia_id;
            $scope.compania_nombre = compania_instancia_nombre;
            $scope.getContactsFromCompany();
        }

    }

    $scope.open_empresa_modal = function() {
        $('#selectEmpresaFormaModal').modal().on('shown.bs.modal', function() {
            $('#search-empresa-forma').focus();
        });
    };

    $scope.set_empresa = function(empresa_id, empresa_nombre) {
        $scope.compania = empresa_id;
        $scope.compania_nombre = empresa_nombre;
        $scope.getContactsFromCompany();
        $('#selectEmpresaFormaModal').modal('hide');
    };

    $scope.init();
});

contacktoApp.controller('SelectEmpresaCTRL', function($scope) {
    $scope.empresas_select_modal = [];

    if (empresas_select !== '') {
        $scope.empresas_select_modal = empresas_select;
    }

    $scope.set_empresa = function(empresa_id, empresa_nombre) {
        var scope = angular.element($("#sidebar")).scope();
        scope.compania_id = empresa_id;
        scope.compania_nombre = empresa_nombre;
        $('#selectEmpresaModal').modal('hide');
        $('#sidebar').scope().contacto_id = '';
        $('#sidebar').scope().setEmpresaContactos();
    };

    $scope.reset_compania = function() {
        var scope = angular.element($("#sidebar")).scope();
        scope.compania_id = '';
        scope.compania_nombre = '';
        $('#selectEmpresaModal').modal('hide');
    }
});

contacktoApp.controller('formaConEmpresaCTRL', function($scope) {
    $scope.compania = '';
    $scope.compania_nombre_trayectoria = '';
    $scope.empresas_select_modal = [];
    if (empresas_select_forma !== '') {
        $scope.empresas_select_modal = empresas_select_forma;
    }

    $scope.open_empresa_modal = function() {
        $('#selectEmpresaFormaModal').modal().on('shown.bs.modal', function() {
            $('#search-empresa-forma').focus();
        });
    };

    $scope.set_empresa = function(empresa_id, empresa_nombre) {
        $scope.compania_trayectoria = empresa_id;
        $scope.compania_nombre_trayectoria = empresa_nombre;
        $('#selectEmpresaFormaModal').modal('hide');
    };

    $scope.init = function() {
        if ($('#empresa_id').val()) {
            $scope.set_empresa($('#empresa_id').val(), $('#empresa_nombre').val())
        }
    }

    $scope.init();
});

contacktoApp.controller('TrayectoriaCTRL', function($scope) {
    $scope.empresas_select_modal = [];

    if (empresas_select_forma !== '') {
        $scope.empresas_select_modal = empresas_select_forma;
    }

    $scope.open_empresa_modal = function() {
        $('#selectEmpresaFormaModal').modal().on('shown.bs.modal', function() {
            $('#search-empresa-forma').focus();
        });
    };

    $scope.set_empresa = function(empresa_id, empresa_nombre) {
        if (confirm('Seguro que deseas cambiar la empresa?')) {
            $scope.compania_trayectoria = empresa_id;
            $scope.compania_nombre_trayectoria = empresa_nombre;
            if ($("#form_trayectoria_editar")) {
                $scope.$apply();
                $("#form_trayectoria_editar").submit();
            }
        }
        $('#selectEmpresaFormaModal').modal('hide');
    };

    $scope.init = function() {
        $scope.compcompania_trayectoriaania = '';
        $scope.compania_nombre_trayectoria = '';

        if (trayectoria_compania_instancia_id !== '') {
            $scope.compania_trayectoria = trayectoria_compania_instancia_id;
            $scope.compania_nombre_trayectoria = trayectoria_compania_instancia_nombre;
        }

    };

    $scope.onClickEditarDatosEmpresa = function($event) {
        if (!confirm('Presiona OK para dejar esta ventana, \nNota:si no has guardado los últimos cambios presiona cancel')) {
            $event.preventDefault();
        }
    };

    $scope.init();
});

contacktoApp.controller('ReporteCTRL', function($scope) {

    $scope.send_email_reporte = function() {
        var user = $scope.getUserById($('#sidebar').scope().empresa_contactos, $('#empresa_contacto').val());
        $('#msg_enviar_reporte').html('').removeClass();
        if (user.fields.email.length) {
            var data = $('#sidebar').scope().get_filtros()
            data['tipo'] = 1;
            $('#panel_enviar_reporte').append(ajaxloader)
            $.post("/api/reporte/enviar_correo", data, 'json').done(function(data) {
                $('#panel_enviar_reporte').find('img').remove();
                if (data.status) {
                    $('#msg_enviar_reporte').removeClass().addClass('alert alert-success').html('Tu correo ha sido enviado.');
                } else {
                    $('#msg_enviar_reporte').removeClass().addClass('alert alert-danger').html('Tu correo no pudo ser enviado, favor de contactar a tu administrador');
                }
            });
        } else {
            if (confirm('Este usuario no tiene correo, Presiona OK para asignarle uno o CANCEL para regresar')) {
                var compania_id = $('#sidebar').scope().compania_id;
                window.location.replace('/empresa/' + compania_id + '/contacto/' + $('#empresa_contacto').val() + '/editar');
            }
        }
    };

    $scope.getUserById = function(data, user_id) {
        for (var i = 0; i < data.length; i++) {
            if (data[i].pk == user_id) {
                return data[i]
            }
        }
        return '';
    }
});

contacktoApp.controller('CobranzaCTRL', function($scope) {
    var cobranza_list = [];
    $scope.selection = [];
    $scope.select_all = false;
    $scope.montos = [];
    $scope.sum_montos = 0;

    $scope.update_sum_montos = function() {
        $scope.sum_montos = 0;
        setTimeout(function() {
            $('.monto_activo').each(function(index) {
                var m = parseFloat($(this).html());
                $scope.sum_montos += m;
                if ((index + 1) == $('.monto_activo').length) {
                    $('#cobranza-table').scope().$apply();
                }
            });
        }, 600);
    }

    $scope.toggleSelection = function(factura_id) {
        var index = $scope.selection.indexOf(factura_id);
        if (index > -1) {
            $scope.selection.splice(index, 1);
        } else {
            $scope.selection.push(factura_id);
        }
        $scope.update_sum_montos()
    };

    $scope.toggleSelectAll = function($event) {
        var action = ($event.target.checked ? 'add' : 'remove');
        if (action == 'remove') {
            $scope.selection = [];
        } else if (action == 'add') {
            $scope.selection = cobranza_list;
        }
        $scope.update_sum_montos();
    }

    $scope.init = function() {
        $('input.active[type="checkbox"]').each(function() {
            cobranza_list.push($(this).val());
        });

        $scope.update_sum_montos();
    }

    $("#cobranza-form").submit(function(event) {
        var selection_json = JSON.stringify($scope.selection);
        $('#selection_json').val($scope.selection);
        // event.preventDefault();
    });

    $scope.init();
});
