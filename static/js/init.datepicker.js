$(function() {
        var date = $("#calendar-widget").val();
		$("#calendar-widget").datepicker();
		$('#calendar-widget').datepicker('option', {dateFormat: 'yy-mm-dd'});
		$("#calendar-widget").datepicker('setDate',date);
	});