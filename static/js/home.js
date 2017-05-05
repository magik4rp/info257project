$(document).ready(function() {
	var data = {universities: 
					{admission: {min: 0, max: 100},
					tuition: {instate: false, max: 100000},
					size: {max: 100000}},
				majors: 
					{salary: {min: 0, max: 300000},
					size: {max: 100000}},
				careers:
					{salary: {min: 0, max: 300000}}};

	$(".button").each(function(index) {
   		$(this).delay(400*index).fadeTo(300, 1, function() {
		});
   	});
   	$(".button").click(function() {
   		$(".buttons").fadeTo(300, 0, function(){
   			$(this).empty();
   		});
   		var id = $(this).attr("id");
   		window.setTimeout(function() {
   			$(".form#" + id).addClass("active");
   			$(".forms").css("display", "block").fadeTo(400, 1, function() {
   				console.log("coming alive!");
   			});
   		}, 300);
   	});
   	$(".tab").click(function() {
   		$(".form.active").removeClass("active");
   		$(this).parent().addClass("active");
   	})
   	$(function() {
	    $( "#admission-rate" ).slider({
	      range: true,
	      min: 0,
	      max: 100,
	      values: [ 0, 100 ],
	      slide: function( event, ui ) {
	      	$("#admission-rate .ui-slider-handle:eq( 0 )").text(ui.values[0] + "%");
	      	$("#admission-rate .ui-slider-handle:eq( 1 )").text(ui.values[1] + "%");
	      	data.universities.admission.min = ui.values[0];
	      	data.universities.admission.max = ui.values[1];
	      	$("#admission-min").val(ui.values[0]);
	      	$("#admission-max").val(ui.values[1]);
	      }
	    });
	  $("#admission-rate .ui-slider-handle:eq( 0 )").text("0%");
	  $("#admission-rate .ui-slider-handle:eq( 1 )").text("100%");
	  } );
   	$("#tuition .radio-button").click(function() {
   		$("#tuition .radio-button").each(function() {
   			$(this).removeClass("active");
   		});
   		$(this).toggleClass("active");
   		if ($(this).hasClass("active")) {
   			data.universities.tuition.max = parseInt($(this).attr("id"));
   		} else {
   			data.universities.tuition.max = 100000;
   		}
   	});
   	$("#size .radio-button").click(function() {
   		$("#size .radio-button").each(function() {
   			$(this).removeClass("active");
   		});
   		$(this).toggleClass("active");
   		if ($(this).hasClass("active")) {
   			data.universities.size.max = parseInt($(this).attr("id"));
   		} else {
   			data.universities.size.max = 100000;
   		}
   	});
   	$("#instate .radio-button").click(function() {
   		$("#instate .radio-button").each(function() {
   			$(this).removeClass("active");
   		});
   		$(this).toggleClass("active");
   		if ($(this).hasClass("active")) {
   			if ($(this).attr("id") == "in") {
   				data.universities.tuition.instate = true;
   			} else {
   				data.universities.tuition.instate = false;
   			}
   		} else {
   			data.universities.tuition.instate = null;
   		}
   	});
   	$(function() {
	    $( "#average-salary" ).slider({
	      range: true,
	      min: 0,
	      max: 300000,
	      values: [ 0, 300000 ],
	      slide: function( event, ui ) {
	      	$("#average-salary .ui-slider-handle:eq( 0 )").text("$" + ui.values[0]);
	      	$("#average-salary .ui-slider-handle:eq( 1 )").text("$" + ui.values[1]);
	      	data.majors.salary.min = ui.values[0];
	      	data.majors.salary.max = ui.values[1];
	      	$("#majors #salary-min").val(ui.values[0]);
	      	$("#majors #salary-max").val(ui.values[1]);
	      }
	    });
	  $("#average-salary .ui-slider-handle:eq( 0 )").text("$0");
	  $("#average-salary .ui-slider-handle:eq( 1 )").text("$300000");
	  } );
   	$("#majors #size .radio-button").click(function() {
   		$("#majors #size .radio-button").each(function() {
   			$(this).removeClass("active");
   		});
   		$(this).toggleClass("active");
   		if ($(this).hasClass("active")) {
   			data.majors.size.max = parseInt($(this).attr("id"));
   		} else {
   			data.majors.size.max = 100000;
   		}
   	});
   	$("select#state").change(function() {
   		var id = $(this).val();
   		console.log("You clicked the option with id " + id);
   		$("input#state").val($(this).val());
   		console.log("The state input value is now " + $("input#state").val());
   	});
   	$(function() {
	    $( "#careers-salary" ).slider({
	      range: true,
	      min: 0,
	      max: 300000,
	      values: [ 0, 300000 ],
	      slide: function( event, ui ) {
	      	$("#careers-salary .ui-slider-handle:eq( 0 )").text("$" + ui.values[0]);
	      	$("#careers-salary .ui-slider-handle:eq( 1 )").text("$" + ui.values[1]);
	      	data.careers.salary.min = ui.values[0];
	      	data.careers.salary.max = ui.values[1];
	      	$("#careers #salary-min").val(ui.values[0]);
	      	$("#careers #salary-max").val(ui.values[1]);
	      }
	    });
	  $("#careers-salary .ui-slider-handle:eq( 0 )").text("$0");
	  $("#careers-salary .ui-slider-handle:eq( 1 )").text("$300000");
	  } );
   $(".submit").click(function() {
   		var category = $(this).attr("id");
   		var keyword = $("#" + category + " #keyword").val();
   		var values = data[category];
   		values.keyword = keyword;
   		values.category = category;
   		$.ajax({
            url: '/search',
            data: $("#" + category + " form").serialize(),
            // data: $("#" + category + " form").serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
   })
}); 
