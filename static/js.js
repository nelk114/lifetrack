function showReg(){document.getElementById("user_form").style.display="block";}
function tickBox(e){
	var cb=e.target;dt=cb.parentElement.id;var hb=cb.parentElement.parentElement.parentElement.id;var ls=cb.parentElement.parentElement.parentElement.parentElement.id;
	csrf=document.getElementById("csrf").firstChild.value;
	post="dt="+encodeURIComponent(dt)+"&hb="+encodeURIComponent(hb)+"&ls="+encodeURIComponent(ls);
	cb.disabled=true
	var xhr=new XMLHttpRequest();
	xhr.onreadystatechange=function(){if(this.readyState==4){cb.disabled=false;if(this.status==200)alert(xhr.responseText)}};
	xhr.open("POST","/occur/");
	xhr.setRequestHeader("X-CSRFToken",csrf);
	xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	xhr.send(post);
	}
