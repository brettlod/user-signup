
import webapp2
import re


page_header = """
<!DOCTYPE html>
<html>
<head>
    <h2>Signup</h2>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

page_footer = """
</body>
</html>
"""

signup_form="""
        <form method="post">
        <table>
            <tr>
                <td class="label">
                    Username
                </td>
                <td>
                    <input type="text" name="username" value="%(username)s" required>
                </td><td>
                <span class="error">%(error_username)s</span>
                </td>
            </tr>
            <tr>
            <td class="label">
                Password
            </td>
            <td>
                <input type="password" value = "" name="password" required>
            </td><td>
            <span class="error">%(error_password)s</span>
            </td></tr>

            <tr>
                <td class="label">
                Verify Password
            </td>
            <td>
                <input type="password" value = "" name="verify" required>
            </td><td>
            <span class="error">%(error_verify)s</span>
            </td></tr>
            <tr>
            <td class="label">
                Email (optional)
            </td>
            <td>
                <input type="email" name="email" value="%(email)s">
            </td><td>
            <span class = "error">%(error_email)s</span>
            </td></tr>
            </table>

        <input type="submit">
        </form>
        """


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class Signup(webapp2.RequestHandler):
    def get(self, error_username="", error_password="", error_verify="", error_email="", username="", email=""):
        self.response.write(page_header + signup_form % {"error_username":error_username,
                                                        "error_password":error_password,
                                                        "error_verify":error_verify,
                                                        "error_email":error_email,
                                                        "username":username,
                                                        "email":email
                                                        } + page_footer)


    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')


        if not valid_username(username):
            error_username = "That's not a valid username."
            have_error = True
        else:
            error_username = ""

        if not valid_password(password):
            error_password = "That wasn't a valid password."
            have_error = True
        else:
            error_password = ""

        if password != verify:
            error_verify = "Your passwords didn't match."
            have_error = True
        else:
            error_verify = ""

        if not valid_email(email):
            error_email = "That's not a valid email."
            have_error = True
        else:
            error_email = ""

        if have_error:
            self.response.write(page_header+signup_form % {"error_username":error_username,
                                                            "error_password":error_password,
                                                            "error_verify":error_verify,
                                                            "error_email":error_email,
                                                            "username":username,
                                                            "email":email
                                                            } + page_footer)
        else:
            self.redirect('/welcome?username=' + username)



class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        welcome = "<h2>Welcome, " + username + "!</h2>"

        if valid_username(username):
            self.response.write(welcome)
        else:
            self.redirect(signup)


app = webapp2.WSGIApplication([
    ('/signup', Signup),
    ('/', Signup),
    ('/welcome', Welcome)],
    debug=True)
