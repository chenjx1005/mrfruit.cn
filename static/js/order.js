			var fnum = 40;//水果数量
			var mark = 0;
			
			function init()
			{
				
				
				var myDate = new Date();
				var flag = myDate.getDay();//time
	
				
				//初始化各个poptable里面的项目
				var popi;
				for(popi = 1; popi <= 5; popi++){
					var popfi;
					for(popfi = 1; popfi <=fnum; popfi++){
						$("#pop"+popi+"_table tr.edit_f"+popfi+" td.item").text($("#record #Recdate"+popi+" .Recf"+popfi+" .RecI").text());
						$("#pop"+popi+"_table tr.edit_f"+popfi+" td.price").text($("#record #Recdate"+popi+" .Recf"+popfi+" .RecP").text());
						$("#pop"+popi+"_table tr.edit_f"+popfi+" td.quantity input").val($("#record #Recdate"+popi+" .Recf"+popfi+" .RecQ").text());
						$("#pop"+popi+"_table tr.edit_f"+popfi+" td.cost").text($("#record #Recdate"+popi+" .Recf"+popfi+" .RecC").text());
					}
				}
				
				//隐藏pop
				hidAllPop();
				
				
				//计算时间
				var i=0;
				//if(flag==0) flag=7;
				for(i = 1;i<=flag;i++)
				{
					var day=$("#date"+i+"1").text();
					$("#date"+i+"1").text("下"+day);
				}
				for(i = flag+1;i<=5;i++)
				{
					var day=$("#date"+i+"1").text();
					$("#date"+i+"1").text("本"+day);
				}
				$("#date12").text((flag>=1)?calcDate(8-flag):calcDate(1-flag));
				$("#date22").text((flag>=2)?calcDate(9-flag):calcDate(2-flag));
				$("#date32").text((flag>=3)?calcDate(10-flag):calcDate(3-flag));
				$("#date42").text((flag>=4)?calcDate(11-flag):calcDate(4-flag));
				$("#date52").text((flag>=5)?calcDate(12-flag):calcDate(5-flag));
			}
			
			
			function hidAllPop()
			{
				var hidpopi;
				for(hidpopi = 1; hidpopi <= 5; hidpopi++){
					$("#pop"+hidpopi).css("visibility","hidden");
				}
			}
			
			//时间函数
			function calcDate(num)
			{
				var myDate = new Date();
				var x = myDate.getMonth();
				var y = myDate.getDate();
				x = x + 1;
				y = y + num;
				if(y<1)
				{
					x--;
					if(x == 0 ) x=12;
					switch(x){
						case 1:y = 31 + y;
						break;
						case 2:y = 28 + y +(myDate.getYear()%4)?0:1;
						break;
						case 3:y = 31 + y;
						break;
						case 4:y = 30 + y;
						break;
						case 5:y = 31 + y;
						break;
						case 6:y = 30 + y;
						break;
						case 7:y = 31 + y;
						break;
						case 8:y = 31 + y;
						break;
						case 9:y = 30 + y;
						break;
						case 10:y = 31 + y;
						break;
						case 11:y = 30 + y;
						break;
						case 12:y = 31 + y;
						break;
					}
				}
				switch(x)
				{
					case 1:y=(y>31)?(x++-x+y-31):y;
					break;
					case 2:y = (y>28+(myDate.getYear()%4)?0:1)?(x++-x+y-28-(myDate.getYear()%4)?0:1):y;
					break;
					case 3:y=(y>31)?(x++-x+y-31):y;
					break;
					case 4:y=(y>30)?(x++-x+y-30):y;
					break;
					case 5:y =(y>31)?(x++-x+y-31):y;
					break;
					case 6:y = (y>30)?(x++-x+y-30):y;
					break;
					case 7:y = (y>31)?(x++-x+y-31):y;
					break;
					case 8:y = (y>31)?(x++-x+y-31):y;
					break;
					case 9:y = (y>30)?(x++-x+y-30):y;
					break;
					case 10:y = (y>31)?(x++-x+y-31):y;
					break;
					case 11:y = (y>30)?(x++-x+y-30):y;
					break;
					case 12:y = (y>31)?(x++-x+y-31):y;
					break;
				}
				
				return x+'/'+y;
			}
			
			//点击框子时候的函数
			function clickOn(id)
			{
				
				//先把所有都变成灰
				defocusPic("date1");
				defocusPic("date2");
				defocusPic("date3");
				defocusPic("date4");
				defocusPic("date5");
				
				//按哪个把哪个激活
				focusPic(id);
				
				//把所有都藏起来
				hidAllPop();
				
				//点到的亮起来
				visPop(id);
			}
			
			function visPop(id)
			{
				var popid;
				switch(id){
					case "date1":
						popid = "pop1";
						mark = 1;
						break;
					case "date2":
						popid = "pop2";
						mark = 2;
						break;
					case "date3":
						popid = "pop3";
						mark = 3;
						break;
					case "date4":
						popid = "pop4";
						mark = 4;
						break;
					case "date5":
						popid = "pop5";
						mark = 5;
						break;
				}
				$("div#"+popid).css("visibility","visible");
				
			}
			
			function focusPic(id)
			{
				var c=$("#Rec"+id+" .total").text();
				c = isNaN(c) ? 0 : c;
				if(c == 0){
					$("#"+id).replaceWith("<img id="+id+" src='../static/images/blank_basket_focus.png' \>");
				}else{
					$("#"+id).replaceWith("<img id="+id+" src='../static/images/full_basket_focus.png' \>");}
			}
			
			function defocusPic(id)
			{
				var c=$("#Rec"+id+" .total").text();
				c = isNaN(c) ? 0 : c;
				if(c == 0){
					$("#"+id).replaceWith("<img id="+id+" src='../static/images/blank_basket_notfocus.png' \>");
				}else{
					$("#"+id).replaceWith("<img id="+id+" src='../static/images/full_basket_notfocus.png' \>");}
			}
			
			
			
			
			
			
			
			
			function addToBascket(fid,num)
			{
				if(mark)
				{
					AddOne(mark,fid);
				}
				
			}
			
			
			function AddOne(id,fid){
				var addQ = parseInt($("#Recdate"+id+" tr.Rec"+fid+" td.RecQ").text());
				addQ = isNaN(addQ) ? 0 : addQ;
				if(addQ == 0){
					$("<tr class='edit_"+fid+"'><td class='item'>"+$("#Recdate"+id+" tr.Rec"+fid+" td.RecI").text()+"</td><td class='quantity'><a onclick=MinusOne('"+id+"','"+fid+"')>-</a><input name='"+id+fid+"' onchange=CalChange('"+id+"','"+fid+"') class='fruit_quantity' onkeyup='this.value=this.value.replace(/\D/g,'')' onafterpaste='this.value=this.value.replace(/\D/g,'')' type=text /><a onclick=AddOne('"+id+"','"+fid+"')>+</a></td><td class='price'>x"+$("#Recdate"+id+" tr.Rec"+fid+" td.RecP").text()+"</td><td class='cost'></td><tr>").insertBefore("#pop"+id+"_table tfoot");
				}
				addQ ++;
				$("#Recdate"+id+" tr.Rec"+fid+" td.RecQ").text(addQ);
				$("#pop"+id+"_table .edit_"+fid+" input").val(addQ);
				CalCost(id, fid);
				focusPic("date"+id);
				//AddAllAmount(id);
			}
			
			function MinusOne(id,fid){
				var minusQ = parseInt($("#Recdate"+id+" tr.Rec"+fid+" td.RecQ").text());
				minusQ = isNaN(minusQ) ? 0 : minusQ;
				if(minusQ == 1){
					$("#pop"+id+"_table .edit_"+fid).css("display","none");
				}
				minusQ --;
				$("#Recdate"+id+" tr.Rec"+fid+" td.RecQ").text(minusQ);
				$("#pop"+id+"_table .edit_"+fid+" input").val(minusQ);
				CalCost(id, fid);
				//AddAllAmount(id)
			}
			
			function CalCost(id, fid){
				var q = parseInt($("#Recdate"+id+" tr.Rec"+fid+" td.RecQ").text());
				q = isNaN(q)? 0: q;
				var p = parseFloat($("#Recdate"+id+" tr.Rec"+fid+" td.RecP").text());
				p = isNaN(p)? 0: p;
				var c;
				c = Math.round(q * p *10) / 10;
				$("#Recdate"+id+" tr.Rec"+fid+" td.RecC").text(c);
				$("#pop"+id+"_table .edit_"+fid+" .cost").text(c+"元");
				CalTotal(id);
			}
			
			function CalTotal(id)
			{
				var i;
				var total = 0;
				for(i = 0; i <= fnum; i++){
					c = parseFloat($("#Recdate"+id+" tr.Recf"+i+" td.RecC").text());
					c = isNaN(c)? 0: c; 
					total += c;
				}
				total = Math.round(total*10) / 10;
				$("#Recdate"+id+" tfoot td").text(total);
				$("#pop"+id+"_table tfoot td").text("总计："+total+"元");
			}
			
			function CalChange(id, fid)
			{
				$("#Recdate"+id+" tr.Rec"+fid+" td.RecQ").text($("#pop"+id+"_table .edit_"+fid+" input").val());
				CalCost(id, fid);
				CalTotal(id);
			}
			