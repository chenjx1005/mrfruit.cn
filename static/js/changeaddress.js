
	function change(){
		$("#tochangetb").css({
			"display":"none"
		});
		$("#changingtb").css({
			"display":"block"
		});
	}
	
	$(document).ready(function(){   
		$("#tochange").click(function(){   
			change();   
		});
	});
// JavaScript Document