var inject_binding = function (allBindings, key, value) {
    //https://github.com/knockout/knockout/pull/932#issuecomment-26547528
    return {
        has: function (bindingKey) {
            return (bindingKey == key) || allBindings.has(bindingKey);
        },
        get: function (bindingKey) {
            var binding = allBindings.get(bindingKey);
            if (bindingKey == key) {
                binding = binding ? [].concat(binding, value) : value;
            }
            return binding;
        }
    };
};

ko.bindingHandlers.selectize = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
        if (!allBindingsAccessor.has('optionsText'))
            allBindingsAccessor = inject_binding(allBindingsAccessor, 'optionsText', 'name');
        if (!allBindingsAccessor.has('optionsValue'))
            allBindingsAccessor = inject_binding(allBindingsAccessor, 'optionsValue', 'id');
        if (typeof allBindingsAccessor.get('optionsCaption') == 'undefined')
            allBindingsAccessor = inject_binding(allBindingsAccessor, 'optionsCaption', 'Choose...');

        ko.bindingHandlers.options.update(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext);

        var options = {
            valueField: allBindingsAccessor.get('optionsValue'),
            labelField: allBindingsAccessor.get('optionsText'),
            searchField: allBindingsAccessor.get('optionsText')
        }

        if (allBindingsAccessor.has('options')) {
            var passed_options = allBindingsAccessor.get('options')
            for (var attr_name in passed_options) {
                options[attr_name] = passed_options[attr_name];
            }
        }
        //remove plugin added in downloaded code
		// var $select = $(element).selectize({
 	// 			plugins: ['remove_button']
		// 		});
		// up to here remove code
        var $select = $(element).selectize(options)[0].selectize;

        if (typeof allBindingsAccessor.get('value') == 'function') {
            $select.addItem(allBindingsAccessor.get('value')());
            allBindingsAccessor.get('value').subscribe(function (new_val) {
                $select.addItem(new_val);
            })
        }

        if (typeof allBindingsAccessor.get('selectedOptions') == 'function') {
            allBindingsAccessor.get('selectedOptions').subscribe(function (new_val) {
                // Removing items which are not in new value
                var values = $select.getValue();
                var items_to_remove = [];
                for (var k in values) {
                    if (new_val.indexOf(values[k]) == -1) {
                        items_to_remove.push(values[k]);
                    }
                }

                for (var k in items_to_remove) {
                    $select.removeItem(items_to_remove[k]);
                }

                for (var k in new_val) {
                    $select.addItem(new_val[k]);
                }

            });
            var selected = allBindingsAccessor.get('selectedOptions')();
            for (var k in selected) {
                $select.addItem(selected[k]);
            }
        }


        if (typeof init_selectize == 'function') {
            init_selectize($select);
        }

        if (typeof valueAccessor().subscribe == 'function') {
            valueAccessor().subscribe(function (changes) {
                // To avoid having duplicate keys, all delete operations will go first
                var addedItems = new Array();
                changes.forEach(function (change) {
                    switch (change.status) {
                        case 'added':
                            addedItems.push(change.value);
                            break;
                        case 'deleted':
                            var itemId = change.value[options.valueField];
                            if (itemId != null) $select.removeOption(itemId);
                    }
                });
                addedItems.forEach(function (item) {
                    $select.addOption(item);
                });

            }, null, "arrayChange");
        }
		// Add new appended
		var name = $(element).attr("name");
		var add_name = "<p id='add_new_user'>Add " + name + "</p>";
		var dropdown = $(element).parent().find(".selectize-dropdown");
		var dropdown_content = $(element).parent().find(".selectize-dropdown-content");
		dropdown.append(add_name);
		// link to modal
		var modal_link = $(element).parent().find("#add_new_user");
		modal_link.attr("data-reveal-id", name);
		//add new link
		var select_input = $(element).parent().find(".selectize-input");

		$(select_input).click(function(){
			$(dropdown).css("display", "block");
		});


    },
    update: function (element, valueAccessor, allBindingsAccessor) {

        if (allBindingsAccessor.has('object')) {
            var optionsValue = allBindingsAccessor.get('optionsValue') || 'id';
            var value_accessor = valueAccessor();
            var selected_obj = $.grep(value_accessor(), function (i) {
                if (typeof i[optionsValue] == 'function')
                    var id = i[optionsValue];
                else
                    var id = i[optionsValue];
                return id == allBindingsAccessor.get('value')();
            })[0];

            if (selected_obj) {
                allBindingsAccessor.get('object')(selected_obj);
            }
        }
    }
};

	$('#group_submit').click(function(e){
		e.preventDefault();
		var group_json_data = JSON.stringify($('.validatedGroupForm').serializeJSON(), null, 2);
		$.ajax({
			url: "/group/",
			type: "POST",
			// async: false,
			contentType: "application/json",
			dataType: 'json',
			data: group_json_data,
			error: function(xhr, textStatus, errorThrown) {
 				alert(xhr.responseText);
     		},
     		success: function(data){
     			toggle.select_group.push([data]);
     		},
     		complete: function(data){
     			var $select = $('#id_group_receivers').selectize();
     			var selectize = $select[0].selectize;
     			selectize.addOption({value:data.responseJSON.id,text:data.responseJSON.name})
     			selectize.addItem(data.responseJSON.id);
     		}
		});
		$('#group_receivers').foundation('reveal', 'close');
		return false;
	});

	$('#user_submit').click(function(e){
		e.preventDefault();
		var user_json_data = JSON.stringify($('.validatedUserForm').serializeJSON(), null, 2);
		$.ajax({
			url :"/users/",
			type: "POST",
			contentType: "application/json",
			dataType: 'json',
			data: user_json_data,
			error: function(xhr, textStatus, errorThrown) {
 				alert(xhr.responseText);
     		},
     		success: function(data){
     			toggle.select_user.push([data]);
     		},
     		complete: function(data) {
     			var $select = $('#id_user_receivers').selectize();
     			var selectize = $select[0].selectize;
     			selectize.addOption({value:data.responseJSON.id,text:data.responseJSON.username})
     			selectize.addItem(data.responseJSON.id);

     		}
		});
		$('#user_receivers').foundation('reveal', 'close');
		return false;
	});	


	$('#id_scheduled_time').datetimepicker({
 		format:'m/d/Y H:i:s',
 		minDate:'-2/01/1970',
	});
	
	// $('#id_date').datetimepicker({
	// 	timepicker:false,
 // 		format:'m/d/Y',
 // 		minDate:'-2/01/1970',

	// });

	// $('#id_scheduled_time_1').datetimepicker({
	// 	datepicker:false,
	// 	format:'H:i',
	// 	minTime: 0
	// });
	
	validateUserVM = function(){
		var self = this;
		self.confirm_msg = ko.observable();
		self.password = ko.observable();
		self.confirm_password = ko.observable()
		self.submit_button = ko.computed(function(){
			if ( self.password() == self.confirm_password()){
				return true;
			} else {
				self.confirm_msg("Confirm your password to activate save")
				return false;
			}

		})
	};

	Toggle = function(){
		var self = this;
		validate_user = validateUserVM;
		self.tog = ko.observable(false);
		self.select_user = ko.observableArray();
		self.select_group = ko.observableArray();
		self.change_button_value = ko.observable('Submit')
		$.ajax({
			url: '/users/.json',
			type: 'GET',
			dataType: 'json',
			success: function(data){
				self.select_user(data);
			}
		});
		$.ajax({
			url: '/group/.json',
			type: 'GET',
			dataType: 'json',
			success: function(data){
				self.select_group(data);
			}
		});

		self.get_u_r = function(){
			if (typeof e_msg === 'undefined') {
				var data = null;
                return data;
			}
			else {
				obj = e_msg;
				return obj.user_receiver;
			};

		};
		self.get_g_r = function(){
			if (typeof e_msg === 'undefined') {
				var data =  null;
                return data;
			}
			else {
				obj = e_msg;
				return obj.group_receiver;
			};

		 };

		var q = self.get_u_r();
		var r = self.get_g_r();
		self.selected_item = ko.observableArray(q);
		self.selected_item1 = ko.observableArray(r);
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
			};
		};
	};

	toggle = new Toggle();
	ko.applyBindings(toggle);
