import yagmail
yagmail.register('antgraves24', 'mustang23')
yag = yagmail.SMTP('antgraves24', 'mustang23')

to = 'antgraves23@gmail.com'
to2 = 'easterbunny@someone.com'
to3 = 'sky@pip-package.com'
subject = 'This is obviously the subject'
body = 'This is obviously the body'
html = '<a href="https://pypi.python.org/pypi/sky/">Click me!</a>'
img = '/local/file/bunny.png'
yag.send(to = to, subject = subject, contents = body)