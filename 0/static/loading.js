function check_ajax(){
    try{ // for Firefox Opera Chrome and Sofaris
        ajaxReq = new XMLHttpRequest();
    }catch(e){
        try{ // for IE
            ajaxReq = new ActiveXObject("Msxml2.XMLHTTP");
        }catch(e){
            try{
                ajaxReq = new ActiveXObject("Microsoft.XMLHTTP");
            }catch(e){
                alert("您的浏览器不支持Ajax,请更换浏览器后重试!");
                return false;
             }
        }
    }
}
function loading(){
    alert("loading");
    var ajaxReq;
    var message = "bsid="+document.getElementById("bsid").value;
    try{ // for Firefox Opera Chrome and Sofaris
        ajaxReq = new XMLHttpRequest();
    alert("xmlHttpRequest");
    }catch(e){
        try{ // for IE
            ajaxReq = new ActiveXObject("Msxml2.XMLHTTP");
        }catch(e){
            try{
                ajaxReq = new ActiveXObject("Microsoft.XMLHTTP");
            }catch(e){
                alert("您的浏览器不支持Ajax,请更换浏览器后重试!");
             }
        }
    }
    alert("loading2");
    ajaxReq.open("GET","index.py?"+message);
    //ajaxReq.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    ajaxReq.send();
    ajaxReq.onreadystatechange=function(){
        if(ajaxReq.readyState == 4){
            if(ajaxReq.responseText.toString().indexOf("0") == 4){
                alert(ajaxReq.responseText.toString());
            }else{
                alert(ajaxReq.responseText.toString());
            }
        }
    }
  }
