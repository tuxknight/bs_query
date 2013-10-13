<?php
	$username=$_POST['username'];
	$passwd=$_POST['passwd'];
        if (isset($_POST['email'])){
            $email=$_POST['email'];
        }else
        {
            $email="";
        }
	echo $username;
        $failed="注册失败，请您刷新页面后重试。";
        $done="恭喜您，注册成功<br/>你现在可以下载客户端使用PyProxy代理服务了";

       $query="INSERT INTO user_info(username,password,email,flag) VALUES('".$username."','".$passwd."','".$email."',"."'1')";

       
              $conn=mysql_connect("localhost","root","chufuyuan");
              mysql_select_db("test",$conn);
              $i=mysql_query($query);
              if (!$i){
                  echo $failed;
              }else{
                  echo $done;
              }
              mysql_close($conn);
              

     
?>