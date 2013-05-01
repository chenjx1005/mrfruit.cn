	//出现窗口
	var status = 0;
	var i = 0;
	var c1 = 0;
	var c2 = 0;
	var c3 = 0;
	var c4 = 0;
	var c5 = 0;
	
	//var k1 = 0;
	//var k3 = 0;
	//var k5 = 0;
	var totalcost = c1 + c2 + c3 + c4 + c5; 
	var date,d1,d2,d3,d4,d5;

	
	function blanktozero(){
					var id = 1;
					$("#list tbody tr.f").each(function() {
						var iqc20 = parseInt($("td.quantity input", this).val());
						iqc20 = isNaN(iqc20) ? 0 : iqc20;
						$("td.quantity input", this).val(parseInt(iqc20));
						id ++;
            		});
	} 
	
	function updatelist(day){
			var rec = String("#Rec"+day+" tr");
			$(rec).each(function(index, element) {
                var q = parseInt($("td.RecQ",this).text());
				q = isNaN(q)? 0 : q;
				if(q != 0){
					var i = String($("td.RecI",this).text());
					var c = String($("td.RecC",this).text());
					$("<tr class='baslist'><td>"+i+"</td><td>x</td><td>"+String(q)+"</td><td>"+c+"元"+"</td></tr>").insertBefore("td#bas"+day+" div.orderlist tfoot");
				}
            });
		}
		
	
	function loadPopup(){
		function loadtable(day){  
			 		var id = 1;
					$("#list tbody tr.f").each(function() {
               			var ii = String("table#Rec"+day+" tr.Recf"+id+" td.RecI");
						var ip = String("table#Rec"+day+" tr.Recf"+id+" td.RecP");
						var iq = String("table#Rec"+day+" tr.Recf"+id+" td.RecQ");
						var ic = String("table#Rec"+day+" tr.Recf"+id+" td.RecC");
						
						var iqc = parseInt($(iq).text());
						var icc = parseFloat($(ic).text());
						iqc = isNaN(iqc) ? 0 : iqc;
						icc = isNaN(icc) ? 0 : icc;
						$("td.item",this).text($(ii).text());
						$("td.price",this).text($(ip).text());
						$("td.quantity input", this).val(parseInt(iqc));
						$("td.cost",this).text(String(icc + "元"));
						id ++;
            		});
		}  
		  
		if(status==0){ 
		
			//读出已有数据////////////////////圣诞节快乐！！！！！！
			switch(i) {
				case 1://星期一
					$("th#date").text("已选日期："+ d1);
					//调出表格数据
					var day = String("Mon");
					loadtable(day);
					$("#Total").text("合计" + String(c1) + "元");
					$("form#dif").attr("action","{{ url_for('add1')}}");
					break;
				case 2://星期2
					$("th#date").text("已选日期："+ d2);
					//调出表格数据
					var day = String("Tue");
					loadtable(day);
					$("#Total").text("合计" + String(c2) + "元");
					$("form#dif").attr("action","{{ url_for('add2')}}");
					break;
				case 3://星期三
					$("th#date").text("已选日期："+d3);
					//调出表格数据
					var day = String("Wed");
					loadtable(day);
					$("#Total").text("合计" + String(c3) + "元");
					$("form#dif").attr("action","{{ url_for('add3')}}");
					break;
				case 4://星期4
					$("th#date").text("已选日期："+d4);
					//调出表格数据
					var day = String("Thur");
					loadtable(day);
					$("#Total").text("合计" + String(c4) + "元");
					$("form#dif").attr("action","{{ url_for('add4')}}");
					break;
				case 5://星期五
					$("th#date").text("已选日期："+d5);
					//调出表格数据
					var day = String("Fri");
					loadtable(day);
					$("#Total").text("合计" + String(c5) + "元");
					$("form#dif").attr("action","{{ url_for('add5')}}");
					break;
			}
		
		
			//显示  
			$("#backgroundPopup").css({   
				"opacity": "0.7"  
			});   
			$("#backgroundPopup").fadeIn("slow");   
			$("#window").fadeIn("slow");   
			status = 1; 
		}   
	}
	 
 
	function disablePopup(j){   
		function savetable(day){
					var id = 1;
					$("#list tbody tr.f").each(function() {
						var iqc = parseInt($("td.quantity input", this).val());
						var icc = parseFloat($("td.cost",this).text().replace("元",""));
						iqc = isNaN(iqc) ? 0 : iqc;
						icc = isNaN(icc) ? 0 : icc;
						var iq = String("table#Rec"+day+" tr.Recf"+id+" td.RecQ");
						var ic = String("table#Rec"+day+" tr.Recf"+id+" td.RecC");
						$(iq).text(String(iqc));
						$(ic).text(icc);
						id ++;
            		});
		}
		
		
		function removelist(day){
			var ol = String("#bas"+day+" div.orderlist tr");
			$(ol).replaceWith("");
		}
		
		
		
		
		
		if(status==1 && j == 1){
			//保存进表格//更新篮子//插入list
			switch(i) {
				case 1://星期一
					var day = String("Mon");
					savetable(day);
					var img= String("#bas"+day+" img.basket");
					var list= String("#bas"+day+" div.orderdiv");
					
					if(c1 > 0){
						$(img).replaceWith("<img class='basket' src='./static/images/basketfull.png'>");
						removelist(day);
						$(list).css("display","block");
						
						$("button#add"+day).html("修改水果");
						updatelist(day);
					} else if(c1 == 0){
								$(img).replaceWith("<img class='basket' src='./static/images/basket.png'>");
								removelist(day);
								$(list).css("display","none");
								$("button#add"+day).html("增加水果");//这里!!!!!!!!!!!!!!!!!!!!!!
							}
					break;
				case 2://星期2
					var day = String("Tue");
					savetable(day);
					var img= String("#bas"+day+" img.basket");
					var list= String("#bas"+day+" div.orderdiv");
					
					if(c2 > 0){
						$(img).replaceWith("<img class='basket' src='./static/images/basketfull.png'>");
						removelist(day);
						$(list).css("display","block");
						
						$("button#add"+day).html("修改水果");
						updatelist(day);
					} else if(c2 == 0){
								$(img).replaceWith("<img class='basket' src='./static/images/basket.png'>");
								removelist(day);
								$(list).css("display","none");
								$("button#add"+day).html("增加水果");//这里!!!!!!!!!!!!!!!!!!!!!!
							}
					break;
				case 3://星期三
					day = String("Wed");
					savetable(day);
					var img= String("#bas"+day+" img.basket");
					var list= String("#bas"+day+" div.orderdiv");
					
					if(c3 > 0){
						$(img).replaceWith("<img class='basket' src='./static/images/basketfull.png'>");
						removelist(day);
						$(list).css("display","block");
						$("button#add"+day).html("修改水果");
						updatelist(day);
					} else if(c3 == 0){
								$(img).replaceWith("<img class='basket' src='./static/images/basket.png'>");
								removelist(day);
								$(list).css("display","none");
								$("button#add"+day).html("增加水果");
							}
					break;
				case 4://星期4
					var day = String("Thur");
					savetable(day);
					var img= String("#bas"+day+" img.basket");
					var list= String("#bas"+day+" div.orderdiv");
					
					if(c4 > 0){
						$(img).replaceWith("<img class='basket' src='./static/images/basketfull.png'>");
						removelist(day);
						$(list).css("display","block");
						
						$("button#add"+day).html("修改水果");
						updatelist(day);
					} else if(c4 == 0){
								$(img).replaceWith("<img class='basket' src='./static/images/basket.png'>");
								removelist(day);
								$(list).css("display","none");
								$("button#add"+day).html("增加水果");//这里!!!!!!!!!!!!!!!!!!!!!!
							}
					break;
				case 5://星期五
					day = String("Fri");
					savetable(day);
					var img= String("#bas"+day+" img.basket");
					var list= String("#bas"+day+" div.orderdiv");
					
					if(c5 > 0){
						$(img).replaceWith("<img class='basket' src='./static/images/basketfull.png'>");
						
						removelist(day);
						$(list).css("display","block");
						$("button#add"+day).html("修改水果");
						updatelist(day);
					} else if(c5 == 0){
								$(img).replaceWith("<img class='basket' src='./static/images/basket.png'>");
								removelist(day);
								$(list).css("display","none");
								$("button#add"+day).html("增加水果");
							}
					break;
				}
			
			//重新计算总计
			c1 = isNaN(c1)? 0 : c1;
			c2 = isNaN(c2)? 0 : c2;
			c3 = isNaN(c3)? 0 : c3;
			c4 = isNaN(c4)? 0 : c4;
			c5 = isNaN(c5)? 0 : c5;
			totalcost = c1+c3+c5;
			$("#totalall").text("总计"+totalcost+"元");
			
			
			//消失   
			$("#backgroundPopup").fadeOut("slow");   
			$("#window").fadeOut("slow");   
			status = 0;   
		}
	}  

	
	function caltotal(){
			var totalc = 0;
			$("#list tbody tr").each(function() {
                var price = parseFloat($("td.price",this).text().replace("元",""));
				price = isNaN(price) ? 0 : price;
				var quantity = parseInt($("td.quantity input", this).val());
				var cost = quantity * price;
				cost = isNaN(cost) ? 0 : cost;
				$("td.cost",this).text(cost + "元"); 
				totalc += cost;
            });
			$("#Total").text("合计" + String(totalc) + "元");
			switch(i){
				case 1:
					c1 = totalc;
					$("#RecMon tfoot.total td").text(c1);
					break;
				case 2:
					c1 = totalc;
					$("#RecTue tfoot.total td").text(c2);
					break;
				case 3:
					c3 = totalc;
					$("#RecWed tfoot.total td").text(c3);
					break;
				case 4:
					c1 = totalc;
					$("#RecThur tfoot.total td").text(c4);
					break;
				case 5:
				    c5 = totalc;
					$("#RecFri tfoot.total td").text(c5);
					break;
			}
	}
	
	
	

	$(document).ready(function(){  
		c1 = parseFloat($("table#RecMon tfoot.total td").text());
		c2 = parseFloat($("table#RecTue tfoot.total td").text());
		c3 = parseFloat($("table#RecWed tfoot.total td").text());
		c4 = parseFloat($("table#RecThur tfoot.total td").text());
		c5 = parseFloat($("table#RecFri tfoot.total td").text());
		c1 = isNaN(c1) ? 0 : c1;
		c2 = isNaN(c2) ? 0 : c2;
		c3 = isNaN(c3) ? 0 : c3;
		c4 = isNaN(c4) ? 0 : c4;
		c5 = isNaN(c5) ? 0 : c5;
		
		
		
		date = new Date();
		var d = date.getDay();
		var h = date.getHours();
		var dch = 0;
		switch(d){
			case 0:
				dch = "日";
				break;
			case 1:
				dch = "一";
				break;
			case 2:
				dch = "二";
				break;
			case 3:
				dch = "三";
				break;
			case 4:
				dch = "四";
				break;
			case 5:
				dch = "五";
				break;
			case 6:
				dch = "六";
				break;
		} 
		var now = String("" + date.getFullYear() + "年" + (date.getMonth()+1) + "月" + date.getDate() + "日");
		var now2 = String("" + "周"+dch);
		$("#now").html(now);
		$("#now2").html(now2);
		if(d == 0) {//ri周12345
			d1=String("本周一");
			d2=String("本周二");
			d3=String("本周三");
			d4=String("本周四");
			d5=String("本周五");
		}
		if(d == 1) {//下周一、本周2345
			d1=String("下周一");
			d2=String("本周二");
			d3=String("本周三");
			d4=String("本周四");
			d5=String("本周五");
		}
		if(d == 2) {//下周12、本周345
			d1=String("下周一");
			d2=String("下周二");
			d3=String("本周三");
			d4=String("本周四");
			d5=String("本周五");
		}
		if(d == 3) {//下周123、本周45
			d1=String("下周一");
			d2=String("下周二");
			d3=String("下周三");
			d4=String("本周四");
			d5=String("本周五");
		}
		if(d == 4) {//下周1234、本周5
			d1=String("下周一");
			d2=String("下周二");
			d3=String("下周三");
			d4=String("下周四");
			d5=String("本周五");
		}
		if((d == 5) || (d == 6)) {//下周12345
			d1=String("下周一");
			d2=String("下周二");
			d3=String("下周三");
			d4=String("下周四");
			d5=String("下周五");
		}
		
		$("#basMon .weekday").text(d1);
		$("#basTue .weekday").text(d2);
		$("#basWed .weekday").text(d3);
		$("#basThur .weekday").text(d4);
		$("#basFri .weekday").text(d5);
		
		if(c1 > 0){
			$("#basMon img.basket").replaceWith("<img class='basket' src='./static/images/basketfull.png'>");
			$("#basMon div.orderdiv").css("display","block");
			$("button#addMon").html("修改水果");
		}
		if(c2 > 0){
			$("#basTue img.basket").replaceWith("<img class='basket' src='./static/images/basketfull.png'>");
			$("#basTue div.orderdiv").css("display","block");
			$("button#addTue").html("修改水果");
		}
		if(c3 > 0){
			$("#basWed img.basket").replaceWith("<img class='basket' src='./static/images/basketfull.png'>");
			$("#basWed div.orderdiv").css("display","block");
			$("button#addWed").html("修改水果");
		}
		if(c4 > 0){
			$("#basThur img.basket").replaceWith("<img class='basket' src='./static/images/basketfull.png'>");
			$("#basThur div.orderdiv").css("display","block");
			$("button#addThur").html("修改水果");
		}
		if(c5 > 0){
			$("#basFri img.basket").replaceWith("<img class='basket' src='./static/images/basketfull.png'>");
			$("#basFri div.orderdiv").css("display","block");
			$("button#addFri").html("修改水果");
		}
		updatelist("Mon");
		updatelist("Tue");
		updatelist("Wed");
		updatelist("Thur");
		updatelist("Fri");
			c1 = isNaN(c1)? 0 : c1;
			c2 = isNaN(c2)? 0 : c2;
			c3 = isNaN(c3)? 0 : c3;
			c4 = isNaN(c4)? 0 : c4;
			c5 = isNaN(c5)? 0 : c5;
			totalcost = c1+c2+c3+c4+c5;
			$("#totalall").text("总计"+totalcost+"元");
		
		 
		$("#addMon").click(function(){ 
			i = 1;  
			loadPopup();
		});
		
		$("#addTue").click(function(){ 
			i = 2;  
			loadPopup();
		});
		
		$("#addWed").click(function(){   
			i = 3;
			loadPopup();
		});
		
		
		$("#addThur").click(function(){ 
			i = 4;  
			loadPopup();
		});
		
		$("#addFri").click(function(){   
			i = 5;
			loadPopup();
		});
		
		$("#pointsbtn").click(function(){
			//显示  
			$("#backgroundPopup").css({   
				"opacity": "0.7"  
			});   
			$("#backgroundPopup").fadeIn("slow");   
			$("#explain").fadeIn("slow");   
			status = 1; 
			
		});
		
		$(".close").click(function(){
			//消失   
			$("#backgroundPopup").fadeOut("slow");   
			$("#window").fadeOut("slow"); 
			$("#explain").fadeOut("slow");   
			status = 0; 
		});

		$("#sub").click(function(){ 
			blanktozero();  
			disablePopup(1);  
			i = 0;//初始化i 
		});   

		$("#backgroundPopup").click(function(){   
			disablePopup(0);   
		});   

		$(document).keypress(function(e){   
			if(e.keyCode==27 && status==1){   
				disablePopup(0);   
			}   
		});  
		
		
		
		// 表格好看
		$("#cal tbody tr:nth-child(even)").addClass("alt");
		$("#cal tbody tr table tr").addClass("alt2");
		
		
		
		//计算
		$("td.quantity input").change(function(){
			caltotal();
			
		});
		
		$("button#sure").click(function(){
			if(totalcost == 0){
				alert("你还没有填写订单哦~");
			}else{
				$("button.add").css("display","none");
				$("button#logout").css("display","none");
				$("button#tochange").css("display","none");
				$("button#sure").css("display","none");
				$("table#cal th#cheers").text("祝贺你订购成功！可以等着吃水果了~").css("text-shadow","none").css("font-size","20px");
				
			}
			
		
		});
		
		$("td.quantity input").bind("click",function(){
			$(this).select();
		});
		
		
	});

 