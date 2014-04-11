#pyspeare
===

See [here](http://shakespearelang.sourceforge.net/report/shakespeare/) for original documentation.

===

pyspeare is an extension of Sam Donow's splc.py Shakespeare to C translator that translates Shakespeare Language code to Python. 
The Shakespeare Programming Language, SPL, was originally invented by Kalle Hasselstrom and Jon Aslund, I take no credit for 
inventing the language nor do I take any credit for the original SPL to C translator.

This software is free to edit or use, though Sam Donow wouldn't mind credit if you do happen to use it.
(c) Sam Donow 2013
sad3@williams.edu
drsam94@gmail.com.

I, also, wouldn't be too averse to credit if you happen to find a use for this project.
(c) Hunter Lightman 2014
me@hunterlightman.com

=== 

This compiler implements most features of the Shakespeare Programming language described at
http://shakespearelang.sourceforge.net/report/shakespeare/

The list of implemented features is as follows: (note, this list is inaccurate for the ->Python version)
- Character based variable (variables need be named after Shakespeare characters)
- Acts for dividing sections of code
- Scenes to serve as labels
- Stage manipulation (entering and exiting various characters via Enter, Exit, and Exuent)
- Support for noun-adjective based constants
- Variable assignment with "you" and "you are as <adjective> as"
- Natural language math ("the difference between the square of the sum of ..."
- Output ("open your heart" for numbers, "speak your mind" for ASCII output)
- Input ("listen to your heart" and "open your mind")
- Goto statements (returning to acts or scenes)
- Conditionals ("is X nicer than Y" vs "is X uglier than Y" followed by "if so" or "if not")

The following features have yet to be implemented:
- Stacks (because who needs data structures in Shakespeare, really?)
- Multiple-word nouns in cases where using just the last word would generate any confusion
- NOT conditionals (necessary?)

=== 

The following feature not in the original language spec is implemented but is a work in progress:

In the original language spec, goto statements take the form "let us proceed to scene III", "let us return to act I",
etc. As this is both awkward and non-Shakesperian, I have made it so that you can use the name of an act or scene (not case,
punctuation, or whitespace sensitive) in place of a this awkward structure. Therefore, if you had
Act I: The Forest.

Then the sentence "let us return to the forest" is equivalent to "let us return to act I".

Like standard gotos, you can not jump to a scene within an act other than the one you are currently in.

===

To use spl, simply run

$ ./spl [Input File]
$ ./a.out

The spl script should work in any bash terminal, on Windows, the explicit python method should work if you have
all of the right programs installed. I may at some time get around to writing a .bat script for Windows users.

Depenencies:
Python (2.X or 3.X)
