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
        $failed="ע��ʧ�ܣ�����ˢ��ҳ������ԡ�";
        $done="��ϲ����ע��ɹ�<br/>�����ڿ������ؿͻ���ʹ��PyProxy����������";

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