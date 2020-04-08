<!DOCTYPE html>
<html lang="ru">
<head>
	<meta charset="UTF-8">
	<title>Эмулятор сигналов</title>
	<link href="static/css/bootstrap.min.css" rel="stylesheet"> 
    <link href="static/css/style.css" rel="stylesheet">    
    <script type="text/javascript" src="static/js/jquery.min.js"></script>
    <script type="text/javascript">
        function srch(){
            var input = $("#search").val();
            $(".btn-D").removeClass("active");
            $(".btn-A").removeClass("active");
            if(input){
                $(".trs").hide();
                if($("."+input).length==0){
                    $(".trs").show();}
                $("."+input).show();
            }else{
            $(".trs").show();}
        }
        function changeD1(id){
            $.post("/new", {type: "Digital", value: "True", id: id});
            $("#"+id).load(location.href+" #"+id+">*","");
        }
        function changeD0(id){
            $.post("/new", {type: "Digital", value: "False", id: id});
            $("#"+id).load(location.href+" #"+id+">*","");
        }
        function changeA(id){
            $.post("/new", {type: "Analog", value: $("#input"+id).val(), id: id});
            $("#"+id).load(location.href+" #"+id+">*","");
        }
        function reset(){
            $.post("/reset");
            $(".table").load(location.href+" .table>*","");
        }
        function filterD(){
            if($("#search").val()){
                $("#search").val("");
                $(".trs").show();
                $(".Analog").toggle();
            }else{
            $(".Analog").toggle();}
            $(".btn-D").toggleClass("active");
            $(".Digital").show();
            $(".btn-A").removeClass("active");
        }
        function filterA(){
            if($("#search").val()){
                $("#search").val("");
                $(".trs").show();
                $(".Digital").toggle();
            }else{
            $(".Digital").toggle();}
            $(".btn-A").toggleClass("active");
            $(".Analog").show();
            $(".btn-D").removeClass("active");
        }
    </script>
</head>
<body>
    <div class="container-fluid" style="height:100%;">
	    <div class="row" style="margin-top:15px; width:100%;">
                <div class="input-group" style="margin-left:15px; width:100%;">
                    <input oninput="srch()" type="text" class="form-control" id="search" style="width:100%; margin-bottom:15px;" placeholder="Поиск" value=""></input>
                </div>
        </div>
        <div class="row" style="width:100%;">
            <div class="col-xs-3 col-md-2">
                <div class="btn-group-vertical" style="margin-top:3px; width:100%;">
                    <button onclick="filterA()" class="btn btn-default btn-block btn-A">Аналоговые</button>
                    <button onclick="filterD()" class="btn btn-default btn-block btn-D">Дискретные</button>
                </div>
                <button onclick="reset()" class="btn btn-danger btn-block btn-pauseall" style="margin-top:10px;">Сброс</button>
            </div>
            <div class="col-xs-9 col-md-10" style= "height:100%;">
                <table class="table table-hover table-condensed table-striped">
                    <thead>
                    <tr>
                        <th>Название</th>
                        <th>Текущее значение</th>
                        <th>Тип</th>
                        <th>Управление</th>
                    </tr>
                    </thead>
% for row in rows:
                    <tr id="{{row[0]}}" class="trs {{row[3]}} {{row[1]}} ">
                        <td>{{ row[1] }}</td>
                        <td>{{ row[2] }}</td>
	% if row[3] == "Analog":
                        <td><span class="label label-primary">{{ row[3] }}</span></td>
                        <td>
                            <div class="input-group" style="width:110px;">
                                <span class="input-group-btn">
                                    <button onclick="changeA({{row[0]}})" class="btn btn-primary btn-xs" style="color:white; width:25px; height:24px;">✔</button>
                                </span>
                                <input type="text" class="form-control" id="input{{row[0]}}" value="{{row[2]}}" style="width:100%; height:24px;"></input>
                            </div>
                        </td>
	% else:
                        <td><span class="label label-default">{{ row[3] }}</span></td>
                        <td>
        % if row[2] == "False":
                            <button onclick="changeD1({{row[0]}})" class="btn btn-success btn-xs">Включить</button>
        % else:
                            <button onclick="changeD0({{row[0]}})" class="btn btn-danger btn-xs">Выключить</button>
        % end
                        </td>
	% end
                    </tr>
% end
                </table>
            </div>
        </div>
    </div>
</body>
</html>
