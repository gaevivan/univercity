$(document).ready(function(){
        $(".btn-pauseall").click(function(){
            $.post('/pause-all');
        })
        $(".btn-A").click(
            function(){
                var value=prompt("Значение","5");
                if (value.search('^[0-9]+$') != -1){
			        $.post('/newsign', {type: 'Analog', value: value});
                } else { 
                    alert('Вводите только цифры!'); 
                }
            }
        )
        $(".btn-D").click(function(){
            var value=prompt("Значение","1111000011110000");
            if (value.search('^[0-1]+$') != -1){
			    $.post('/newsign', {type: 'Digital', value: value});} else { alert('Вводите только 0 и 1!'); }       
        })
        $(".btn-addall").click(function(){
            $.post('/add-all');
        })
        $(".btn-add").click(function(){
            $.post('/add-one', {id: $(this).attr("id").replace(/[a-z]*/g,'')});
        })
        $(".btn-pause").click(function(){
            pause_one();
            $.post('/pause-one', {id: $(this).attr("id").replace(/[a-z]*/g,'')}); 
            $("#signs-line"+$(this).attr("id").replace(/[a-z]*/g,'')).remove();
        })
        $(".btn-del").click(function(){
            $.post('/delete-one', {id: $(this).attr("id").replace(/[a-z]*/g,'')});
        	$("#line"+$(this).attr("id").replace(/[a-z]*/g,'')).remove();
            $("#signs-line"+$(this).attr("id").replace(/[a-z]*/g,'')).remove();
        })
    }
