<form id="query" name="query" method="post" action="index.py" onsubmit="loading()">
  <table width="366" border="0" bordercolor="#F0F0F0" align="center" cellpadding="10px">
    <tr>
      <td width="120">用户名</td>
      <td width="200">
        <input type="text" name="username" />

      </td>
    </tr>
    <tr>
      <td>密码(至少6个字符)</td>
      <td><input type="password" name="passwd"  /></td>
    </tr>
    <tr>
      <td>确认密码</td>
      <td>
        <input type="password" name="passwd_confirm"  />
      </td>
    </tr>
    <tr>
      <td height="34">Email（选填）</td>
      <td>
        <input type="text" name="email"  />
      </td>
    </tr>
    <tr>
      <td>
        <input type="submit" name="Submit" value="提交" />
      </td>
      <td>
        <input type="reset" name="Reset"  value="重置" />
      </td>
    </tr>
  </table>  
  </form>
