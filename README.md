WyliePy

Wylie transliteration port from JAVA version http://www.thlib.org/reference/transliteration/wyconverter.php

Use:
```py
warn = []
print (Wylie().fromWylie("sems can thams cad", warn))
print ('\n'.join(warn))

print (Wylie().toWylie(u"ཨོཾ་ཨཿཧཱུྂ་བཛྲ་གུ་རུ་པདྨ་སིདྡྷི་ཧཱུྂ༔"))
```
