function showReg(){document.getElementById("user_form").style.display="block";}
function tickBox(e){
	cb=e.target;dt=cb.parentElement.id;hb=cb.parentElement.parentElement.parentElement.id;ls=cb.parentElement.parentElement.parentElement.parentElement.id;
	csrf=document.getElementById("csrf").firstChild.value;
	post="dt="+encodeURIComponent(dt)+"&hb="+encodeURIComponent(hb)+"&ls="+encodeURIComponent(ls);
	//alert(post);
	var xhr=new XMLHttpRequest();
	xhr.onreadystatechange=function(){if(this.readyState==4&&this.status==200)alert(xhr.responseText)};
	xhr.open("POST","/occur/");
	xhr.setRequestHeader("X-CSRFToken",csrf);
	xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	xhr.send(post);
	}
