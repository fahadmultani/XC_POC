ko.validation.init({
  		errorElementClass: "wrong-field",
  		decorateElement: true,
  		errorClass: 'wrong-field'
	}, true);

var ViewModel = function() 
{
	$("#startdate_datepicker").datepicker({
	            format: 'yyyy/mm/dd',
	            startDate: '1d'
	        }).attr("autocomplete", "off");
	var self = this;
	self.title = ko.observable().extend({required: true});
	self.description = ko.observable().extend({required: true});
	self.targetDate = ko.observable().extend({required: true});
	self.clientPriority = ko.observable().extend(
		{
    	required: 
    	{
   	 		message: "This field is required.",
      	},
     	min: 
     	{
     		message: "Priority can't be less than 1.",
      		params: 1,
    	}
		});
	self.selectClient = ko.observable('').extend({required: true});
	self.productArea = ko.observable('').extend({required: true});

	self.errors = ko.validation.group(self);
 	self.submit = function() 
 	{
  		self.errors.showAllMessages();
  		if (self.errors().length === 0) 
  		{
			var data = {
				  			"title": self.title(),
			  				"description": self.description(),
			  				"targetDate": self.targetDate(),
			  				"clientPriority": self.clientPriority(),
			  				"selectClient": self.selectClient(),
			  				"productArea": self.productArea()
  						}
	  		///////  Ajax Call  //////
	  		$.ajax({
	  			url: "./index",
	  			data: JSON.stringify(data),
	  			type: 'POST',
	  			dataType: 'json',
	  			contentType: 'application/json',
	  			success: function(response){
	  				window.location = "/";
	  			},
	  			error: function(error){}
	  		});  	
  		}
  	}
}
//////  Apply Knockout Bindings  ///////
ko.applyBindings(new ViewModel());
