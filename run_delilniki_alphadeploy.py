__author__ = 'Lesko'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.
from app import app
print "#################  ", "Alpha deploy", "  #################"
app.run(host="192.168.1.52", port=8005, debug=True)