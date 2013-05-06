/*
(function ($) {
	$.fn.ls_crop=function (callback,options) {
		callback(this,options)
	} 
	
}(jQuery));
*/
(function ($) {
	$.fn.bindPopover=function (popoverContent,placement) {
		var fieldItem=$(this);
		if(!placement){
             placement='right'
         }
         popid=fieldItem.attr('id')+"_popover";   
         pc="<div id='"+popid+"'>"+popoverContent+"</div>";
         fieldItem.popover({'content':pc,'delay':{show: 500, hide: 100},'container':'body','html':true,'placement':placement});
                             
         var popover=fieldItem.popover('show');
         //fieldItem.bind('click',function(){fieldItem.popover('hide');});
         $('#'+popid).bind('click',function(){
             fieldItem.popover('hide');
         });
         fieldItem.bind('click',function(){
         	$(this).popover('hide');
         });
	} 
	$.fn.alertid=function () {
		alert($(this).attr('id'));
	} 
	
}(jQuery));