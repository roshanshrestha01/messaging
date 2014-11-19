
$('#id_scheduled_time_0').datetimepicker({
	timepicker:false,
	format:'m/d/Y',
	minDate:'-2/01/1970',
});
	
$('#id_date').datetimepicker({
	timepicker:false,
	format:'m/d/Y',
	minDate:'-2/01/1970',
});

$('#id_scheduled_time_1').datetimepicker({
	datepicker:false,
	format:'H:i',
	minTime: 0
});

$(document).ready(function(){
	$('#id_user_receivers').selectize({
		plugins: ['remove_button']
	});

$('#id_group_receivers').selectize({
	plugins: ['remove_button']
	});
});	

Toggle = function(){
	var self = this;
	self.tog = ko.observable(false);
	self.change_button_value = ko.observable('Submit')
	self.usr_receiver = ko.observableArray()
	self.test = ko.observable()
	self.grp_receiver = ko.observableArray()
	// self.button_enable = ko.computed(function() {
	// 	return self.usr_receiver().length > 0;
	// });
	self.submit_save = function(data,event){
		if(self.tog()==true){
			self.change_button_value('Save');
			console.log(event.target.checked); // log out the current state
   			console.log("1");
   			return true;
		} else {
			self.change_button_value('Submit');
			console.log(event.target.checked); // log out the current state
       			console.log("1");
       			return true; 
			}
		};
	};

	toggle = new Toggle();
	ko.applyBindings(toggle);

