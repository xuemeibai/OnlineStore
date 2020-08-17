$(document).ready(function()
{
    var num = $('#num').html()
    var favorite = []
    for (var i=1; i <= num; i++){
        favorite[i-1] = parseInt($('#favorite'+i).html());
        if (favorite[i-1]){
            $('#'+i).attr("rel","unlike");
            $('#'+i).css("background-position","right");
        }
        else{
            $('#'+i).attr("rel","like");
            $('#'+i).css("background-position","left");
        }
    }
    $('body').on("click",'.heart',function()
    {
        $(this).css("background-position","")
        var D=$(this).attr("rel");
        var label=$(this).attr("id");
        var item_id=$('#img'+label).html();
        if(D === 'like') {      
            $(this).addClass("heartAnimation").attr("rel","unlike"); 
            $(this).css("background-position","right");
            $('#favorite'+label).html(1);
            $.ajax({
                url: "/add_to_favorite_home?item_id="+item_id,
                type: "GET",
                dataType : "json",
            });
            //$("#add"+label+" a")[0].click();
        }
        else{
            $(this).removeClass("heartAnimation").attr("rel","like");
            $(this).css("background-position","left");
            $('#favorite'+label).html(0);
            $.ajax({
                url: "/delete_from_favorite_home?item_id="+item_id,
                type: "GET",
                dataType : "json",
            });
            //$("#delete"+label+" a")[0].click();
        }
    });
});