#pyspeare
by [Huntrr](https://github.com/Huntrr),
based on [Spl](https://github.com/drsam94/Spl) by [drsam94](https://github.com/drsam94)

##Overview
pyspeare is an extension of [Sam Donow's splc.py Shakespeare to C translator](https://github.com/drsam94/Spl) that's been expanded to translate Shakespeare Language code to Python code. The Shakespeare Programming Language, [SPL](http://shakespearelang.sourceforge.net/report/shakespeare/), was originally invented by Kalle Hasselstrom and Jon Aslund, and neither Sam nor I take any credit for 
inventing the language. The original base for this code is also by Sam Donow, and my additions simply change the output to Python (it was, originally, C), attempt to clean up the code, and implement several missing features of the language.

This software is free to edit or use, though Sam Donow wouldn't mind credit if you do happen to use it.
> (c) **Sam Donow** 2013 

> sad3@williams.edu 

> drsam94@gmail.com.

===

I, also, wouldn't be too averse to credit if you happen to find a use for this project. 
> (c) **Hunter Lightman** 2014 

> git.huntrr@gmail.com


##Progress
This compiler implements most features of the Shakespeare Programming language described at http://shakespearelang.sourceforge.net/report/shakespeare/

The following features have yet to be implemented:
* Stacks (declared, but not yet used) ('Remember me', 'Remember yourself' are pushes, and 'recall your ...', 'recall my ...' are pops)
* Multiple-word nouns in cases where using just the last word would generate any confusion
* NOT conditionals ('not as good as' or 'not bettan than' etc)

===

Additionally, one feature—not in the original language spec—is implemented but is a work in progress:

In the original language spec, goto statements take the form "let us proceed to scene III", "let us return to act I",
etc. As this is both awkward and non-Shakesperian, this code allows you to use the name of an act or scene (not case,
punctuation, or whitespace sensitive) in place of a this awkward structure. Therefore, if you had
    Act I: The Forest.

Then the sentence "let us return to the forest" is equivalent to "let us return to act I".

Like standard gotos, you can not jump to a scene within an act other than the one you are currently in.


##Usage

To use spl, simply run

    $ ./spl [Input File]
    $ ./a.out

or, even more simply

    python splp.py [Input File] > [Output File]

The spl script should work in any bash terminal, on Windows, the explicit python method should work if you have
all of the right programs installed. I may at some time get around to writing a .bat script for Windows users.

####Depenencies:
Python (2.X or 3.X)
