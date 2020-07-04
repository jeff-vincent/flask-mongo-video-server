index_view = """
        <div style="background-color: #707bb2; margin: 15px; border-radius: 5px; padding: 15px; width: 180px">
        <form action="/stream" method="post">
            <p><input type=text name=filename placeholder=" filename...">
            <p><input type=submit value="Play">
        </form>
        <form action="/get-current-users-files" method="get">
            <p><input type=submit value="Your Video Library">
        </form>
        <form action="/get-public-files" method="get">
            <p><input type=submit value="Public Videos">
        </form>
        </div>
        <b style="margin-left:25px">Add to your video library: </b>
        <form style="margin-left:30px" action="/upload" method="post" enctype="multipart/form-data">
            <p><input type=file name=file value="Pick a Movie">
            <p><input type=checkbox name=public> Make public</br>
            <p><input type=submit value="Upload">
        </form>
        <div style="background-color: #707bb2; margin: 15px; border-radius: 5px; padding: 15px; width: 180px">
        <b>Sign Up:</b>
        <form action="/signup" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value="Sign-up">
        </form>
        <b>Login:</b>
        <form action="/login" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value="Login">
        </form>
        <form action="/logout" method="get">
            <p><input type=submit value="Logout">
        </form>
        </div>
        """