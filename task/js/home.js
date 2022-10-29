$('.table').click(function () { 
    // console.log('输出边框颜色',$(this).css('border-color'),$(this).css('color'));
    $('.table').eq(0).removeClass('checked_default')
    $(this).css('background',$(this).css('color'));
    $(this).addClass('checked');
    $(this).siblings().removeClass('checked');
    $(this).siblings().css('background','');
});
// $('.choose_mood').click(function(){
//     // console.log('点击选择心情，出现盒子');
//     if($('.mood_box').attr('data-display') == 'false'){
//         $('.mood_box').css('display','flex');
//         $('.mood_box').attr('data-display','true')
//     }else{
//         $('.mood_box').css('display','none');
//         $('.mood_box').attr('data-display','false')
//     }
// })
$('.mood').click(function(){
    // console.log('选择状猿表情')
    $(this).addClass('checked_mood');
    $(this).siblings().removeClass('checked_mood')
})
$('.select').change(function (e) { 
    console.log('mood改变',$(this).val())
    $('.mood_show img').attr('src','../static/images/' + $(this).val());
});