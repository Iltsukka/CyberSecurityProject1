LINK TO THE REPO: https://github.com/Iltsukka/CyberSecurityProject1
installation instructions if needed

## FLAW 1: SENSITIVE DATA EXPOSURE

exact source link pinpointing flaw 1...

The first flaw is about sensitive data exposure. The application stores user passwords as plain text data when critical information like password should be hashed and salted for security purposes.

The fix is a one-liner. Django comes with a default method .set_password(‘your password’) that works with the Django authentication. Storing the password using that method it is correctly hashed and safe. In case of future data breaches atleast the password wont be plain text and usually hashed passwords are harder to brute-force solve.

FLAW 2:
exact source link pinpointing flaw 2...

description of flaw 2...

how to fix it...

...

FLAW 5:

exact source link pinpointing flaw 5...

description of flaw 5...

how to fix it...
