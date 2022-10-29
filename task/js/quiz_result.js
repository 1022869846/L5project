$('.top .choices').click(function (e) { 
    console.log(this)
    $('.top .choices').siblings().removeClass('checked')
    $(this).addClass('checked');
});
$('.bottom .choices').click(function (e) { 
    console.log(this)
    $('.bottom .choices').siblings().removeClass('checked')
    $(this).addClass('checked');
});
$('.submit').on('mousedown',function(){
    $(this).addClass('click')
})
$('.submit').on('mouseup',function(){
    $(this).removeClass('click')
})