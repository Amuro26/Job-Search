// JavaScript Document

$("#type2").on("click",function(){
	$("#type1").addClass("off").removeClass("on");
	$("#type2").addClass("on").removeClass("off");
	$("#1login").hide();
	$("#2login").show();
})
$("#type1").on("click",function(){
	$("#type2").addClass("off").removeClass("on");
	$("#type1").addClass("on").removeClass("off");
	$("#2login").hide();
	$("#1login").show();
})