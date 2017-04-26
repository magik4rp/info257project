$(document).ready(function() {
	$(".button").each(function(index) {
   		$(this).delay(400*index).fadeTo(300, 1, function() {
			console.log("Completed!");
		});
   	});
   	$(".button").click(function() {
   		$(".inner").fadeTo(200, 0, function(){
   			$(this).empty();
   		});
   	});
   	$(".tab").click(function() {
   		$(".form.active").removeClass("active");
   		$(this).parent().addClass("active");
   	})
}); 
