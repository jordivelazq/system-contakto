var is_usuario_contacto = true;
$(document).ready(function(){
	$('input, textarea').not('#sidebar input, #sidebar textarea').prop('readonly', true);
	$('select, :checkbox, :radio').not('#sidebar select, #sidebar :checkbox, #sidebar :radio').prop('disabled', 'disabled');
});