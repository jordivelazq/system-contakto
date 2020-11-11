/*
	Author: Mint IT Media
*/
var folder = '/';

$(document).ready(function () {
  var page = get_currentpage();

  if (page.indexOf('exito') != -1) {
    showMSG('msg', 'Tu operación se realizó con éxito', 'alert alert-success text-center');
  } else if (page.indexOf('error') != -1) {
    showMSG('msg', 'Tu operación no pudo ser realizada, favor de intentar de nuevo', 'alert alert-danger');
  }

  $('#navigation_tabs a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
  });

  $('input, select').keypress(function (event) {
    if (event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

  $('#id_investigacion-fecha_recibido, #id_fecha_entrevista, #id_trayectoria-periodo_alta, #id_trayectoria-periodo_baja, #id_deudas-0-fecha_otorgamiento, #id_deudas-1-fecha_otorgamiento, #id_entrevista-fecha_entrevista, #id_investigacion-fecha_entrega').each(function () {
    if (typeof $(this) != 'undefined') {
      $(this).datepicker({
        format: 'dd/mm/yyyy'
      })
    }
  });

  if ($('.datepicker').length) {
    $('.datepicker').each(function () {
      if (typeof $(this).split != 'undefined') {
        $(this).datepicker({
          format: 'dd/mm/yyyy'
        });
      }
    })
  };

  $('#id_hora_entrevista').timepicker({
    'timeFormat': 'G:i'
  });

  $('.timepicker').timepicker({
    'timeFormat': 'G:i'
  });

  $('.phone').keyup(function () {
    this.value = this.value.replace(/[^0-9\.]/g, '');
  });

  $('.btn_eliminar').click(function () {
    if (confirm('Seguro que deseas eliminar?')) {
      return true;
    }
    return false;
  })

  $('.btn_quitar_factura').click(function () {
    if (confirm('Seguro que deseas quitar el # de factura?')) {
      return true;
    }
    return false;
  })

  $('.btn_agregrar_factura').click(function () {
    if (confirm('Seguro que deseas agregar el # de factura?')) {
      return true;
    }
    return false;
  })

  $('.missing-form-control input[type=text], .missing-form-control input[type=number]').addClass('form-control');

  $(document).delegate('*[data-toggle="lightbox"]', 'click', function (event) {
    event.preventDefault();
    $(this).ekkoLightbox();
  });

  formatCurrencyFields();

  $('.fixed-submenu button').click((event) => {
    const {
      name
    } = event.target

    $('.save-type').remove()
    $('#form_candidato_crear').append(`<input name="${name}" type="hidden" class="save-type" />`)
    $('#form_candidato_crear').submit()
  })

  autoSave()
  askBeforeMoveInsideInvestigation()
  newClientContact()
  autoSaveFiles()
  saveCompany()
  statusListners()

  initDynamicForms()
  initFactura()
});

function get_currentpage() {
  var loc = window.location;
  var loc_ref_sinfiltros = loc.href.indexOf('?') > -1 ? loc.href.substring(0, loc.href.indexOf('?')) : loc.href
  p = loc_ref_sinfiltros.substring(loc.href.indexOf(loc.host) + loc.host.length + folder.length);
  if (p == '') p = '/investigaciones';
  return p;
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
  crossDomain: false, // obviates need for sameOrigin test
  beforeSend: function (xhr, settings) {
    var csrftoken = getCookie('csrftoken');
    if (!csrfSafeMethod(settings.type)) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

function showMSG(id, msg, custom_class) {
  $('#' + id).css({
    'opacity': '0',
    'position': 'absolute',
    'z-index': '10',
    'width': '100%'
  }).removeClass().addClass(custom_class).text(msg).animate({
    opacity: 1
  }, 500, function () {
    removeMSG(id);
  });
}

function removeMSG(id) {
  setTimeout(function () {
    $('#' + id).animate({
        opacity: 0
      },
      1000,
      function () {
        $('#' + id).removeClass().text('').css({
          'position': 'initial',
          'z-index': 'initial',
          'width': 'initial'
        });
      });
  }, 3000);
}

/*
 * Function to calculate Age based in date of birth.
 * extracted from: http://www.romcartridge.com/2010/01/javascript-function-to-calculate-age.html
 * @param {integer} birthMonth
 * @param {integer} birthDay
 * @param {integer} birthYear
 * @return {integer} age
 */
function calculateAge(birthMonth, birthDay, birthYear) {
  todayDate = new Date();
  todayYear = todayDate.getFullYear();
  todayMonth = todayDate.getMonth();
  todayDay = todayDate.getDate();
  age = todayYear - birthYear;

  if (todayMonth < birthMonth - 1) {
    age--;
  }

  if (birthMonth - 1 == todayMonth && todayDay < birthDay) {
    age--;
  }
  return age;
}

/*
	function to give money format $XX,XXX.XX to all fields with custom_money_format class, that class is assigned in the BE
*/
function formatCurrencyFields() {
  var fields = $('.custom_money_format');
  fields.map(function (index) {
    // clean the value from DB and get a "real" number 
    var value = fields[index].value.match(/[\d,]+(\.[\d]+)*/gi) ? fields[index].value.match(/[\d,]+(\.[\d]+)*/gi).toString().replace(/,/g, '') : null;
    if (value) {
      // if value passes our regext then we call customFormatMoney to show number on the rirght format
      fields[index].value = customFormatMoney(value, 2, '.', ',');
    }
  })
}

/*
	function got it from: http://stackoverflow.com/questions/2116558/fastest-method-to-replace-all-instances-of-a-character-in-a-string
	adapt 'n' parameter to receive value to format
	@n {integer} n value to format
	@c {integer} c point fixed number, helps to know how many decimels to show
	@d {char} d fixed symbol to show
	@t {char} t thousand symbol
	@return {string} format value
*/
customFormatMoney = function (n, c, d, t) {
  var c = isNaN(c = Math.abs(c)) ? 2 : c,
    d = d == undefined ? "." : d,
    t = t == undefined ? "," : t,
    s = n < 0 ? "-" : "",
    i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "",
    j = (j = i.length) > 3 ? j % 3 : 0;
  return '$' + s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
};


function autoSave() {
  if ($('.btn-primary[name=guardar]').length) {
    const limit = 5
    setInterval(() => {
      if (confirm(`han pasado ${limit} minutos, quieres guardar los cambios?`)) {
        $('.btn-primary[name=guardar]').click()
      }
    }, 1000 * 60 * limit)
  }
}

function askBeforeMoveInsideInvestigation() {
  if ($('.investigacion-menu').length) {
    $('.investigacion-menu a').click((event) => {
      if ($('.btn-primary[name=guardar]').length) {
        if (confirm('Deseas guardar los cambios efectuados?')) {
          event.preventDefault()
          $('form').append(`<input type="hidden" name="redirect" value="${event.target.pathname}" />`)
          $('.btn-primary[name=guardar]').click()
        }
      }
    })
  }
}

function newClientContact(event) {
  if ($('.new-client-contact').length) {

    $('.new-client-contact').click(event => {
      if (event.originalEvent.target.pathname === "/empresa//contacto/nuevo") {
        event.preventDefault()

        const empresaId = $('#id_investigacion-compania').val()
        if (empresaId) {
          window.location = `/empresa/${empresaId}/contacto/nuevo`
        } else {
          alert('Hay que eligir empresa primero.')
        }
      }
    })

  }
}

function autoSaveFiles() {
  if ($('#form_attachments').length) {
    $('#form_attachments input[type=file]').change(saveFile)
  }
}

function saveFile(event) {
  const data = new FormData($('#form_attachments').get(0));

  $.ajax({
    url: $('#form_attachments').attr('action'),
    type: $('#form_attachments').attr('method'),
    data: data,
    processData: false,
    contentType: false,
    success: () => location.reload()
  });
}

function saveCompany() {
  if ($('#empresa_nueva_cta').length) {
    $('#empresa_nueva_cta').click(() => {
      $('#empresa_nueva_form').removeClass('hide')
      $('#save_company_msg').text('')
      $('#save_company').removeAttr("disabled");
    })

    if ($('#search-empresa-forma').length) {
      $('#search-empresa-forma').on('input', function() {
        if (this.value.length > 2) {
          $('#empresa_nueva_cta').removeAttr("disabled");
        } else {
          $('#empresa_nueva_cta').attr("disabled", "disabled");
        }
      });
    }
  }

  if ($('#save_company_cancel').length) {
    $('#save_company_cancel').click(() => {
      $('#empresa_nueva_form').addClass('hide')
    })
  }

  if ($('#save_company').length) {
    $('#save_company').click(() => {
      $('#save_company_msg').text('')
      const data = {}

      $('#new_company :input[type=text]').toArray().reduce((values, field) => {
        if ($(field).val()) {
          values[field.name] = $(field).val();
        }

        return values
      }, data);

      $('#new_company :input[type=checkbox]').toArray().reduce((values, field) => {
        if ($(field).val()) {
          values[field.name] = $(field).prop('checked')
        }

        return values
      }, data);

      if (Object.keys(data).length != 5) {
        $('#save_company_msg').text('Favor de llenar todos los campos.')
        return
      }

      $('#save_company').attr('disabled', 'disabled')

      $.ajax({
        type: 'POST',
        url: '/empresa/nueva/',
        data,
        success: (response) => {
          if (response.status) {
            $('#id_investigacion-compania').val(response.company.id)
            $('#id_investigacion-compania-nombre').attr('placeholder', response.company.name)
            $('#contacto_id').val(response.contacto.id)
            $('#id_investigacion-contacto').append(`<option value="${response.contacto.id}" selected>${response.contacto.name}</option>`)
            $('#selectEmpresaFormaModal').modal('hide');
          } else {
            $('#save_company').attr('disabled', false)
            $('#save_company_msg').text(response.msg)
          }
        },
        dataType: 'json'
      });
    })
  }
}

function statusListners() {
  if ($('#status_checkbox').length) {
    $('#status_checkbox').on("click", () => {

      $('.table-estatus tbody input[type=checkbox]').each((index, item) => {
        $(item).prop("checked", !$(item).prop("checked"));
      });

    })
  }
}

function setDynamicFormCTA(ctaSelector, limit) {
  if ($(ctaSelector).length) {
    $(ctaSelector).click(function () {
      var form_idx = parseInt($('#id_form-TOTAL_FORMS').val() || 0);

      if (form_idx < limit) {
        $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx).replace('#', form_idx + 1));
        $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
      }
    });
  }
}


function initDynamicForms() {
  setDynamicFormCTA('#add_more_demandas', 5)
}

function setFacturaData(xmlDoc) {
  const data = xmlDoc.getElementsByTagName('cfdi:Comprobante')[0].attributes
  const factura = xmlDoc.getElementsByTagName('cfdi:Receptor')[0].attributes

  $('#id_folio').val(data.Folio.value)
  $('#id_subtotal').val(data.SubTotal.value)
  $('#id_total').val(data.Total.value)
  $('#id_fecha').val(data.Fecha.value.split('T')[0])
  $('#id_rfc').val(factura.Rfc.value)
  $('#id_nombre').val(factura.Nombre.value)
}

function onChangeFacturaHandler() {
  var file = document.getElementById("factura").files[0];

  if (file) {
    var reader = new FileReader();
    reader.readAsText(file, "UTF-8");
    reader.onload = function (evt) {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(evt.target.result, "text/xml");

      setFacturaData(xmlDoc)
    }

    reader.onerror = function (evt) {
      alert("error reading file");
    }
  }
}

function initFactura() {
  if ($('#factura').length) {
    $('#factura').change(onChangeFacturaHandler);
  }
}

function deepEqual(object1, object2) {
  const keys1 = Object.keys(object1);
  const keys2 = Object.keys(object2);

  if (keys1.length !== keys2.length) {
    return false;
  }

  for (const key of keys1) {
    const val1 = object1[key];
    const val2 = object2[key];
    const areObjects = isObject(val1) && isObject(val2);
    if (
      areObjects && !deepEqual(val1, val2) ||
      !areObjects && val1 !== val2
    ) {
      return false;
    }
  }

  return true;
}

function isObject(object) {
  return object != null && typeof object === 'object';
}

function areFiltersEqual(filters) {
  if (typeof(Storage) !== "undefined") {
    const filtersSaved = JSON.parse(sessionStorage.getItem("filters") || '{}');
    return deepEqual(filters, filtersSaved)
  }

  return false
}

function getCandidatos(filtros) {
  if (typeof(Storage) !== "undefined" && areFiltersEqual(filtros)) {
    const candidatos = JSON.parse(sessionStorage.getItem("candidatos") || '[]');
    if (candidatos.length) {
      return candidatos
    }
  }

  return new Promise(resolve => {
    $.post( "/candidato/search_candidatos/", filtros , 'json')
      .done(function( data ) {
        if (typeof data.status != 'undefined' && data.status){
          resolve(data.candidatos)

          if (typeof(Storage) !== "undefined") {
            sessionStorage.setItem("candidatos", JSON.stringify(data.candidatos))
            sessionStorage.setItem("filters", JSON.stringify(filtros))
          }
        } else {
          resolve([])
        }
      });
  })
}
