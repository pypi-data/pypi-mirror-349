# Pygments GDScript Lexer
This lexer was made to fill in the holes [pygments/lexers/gdscript.py](https://github.com/pygments/pygments/blob/master/pygments/lexers/gdscript.py) left.
A pull request is in the works, but for us, the long wait for the dependency chain is not worth it.
As such, this is the home of the "better lexer" for use in the [GMLWiki](https://github.com/GodotModding/gmlwiki) until further notice.

To test the highlighting independantly; because let's be real rebuilding the GMLWiki to test it would be overkill.
You may run [test.py](https://github.com/GodotModding/pygments-gdscript/test.py), which will export a `test.html`.
Note that you **must** install `pygments` through pip to run the test.
