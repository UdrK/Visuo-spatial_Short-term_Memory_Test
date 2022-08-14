# Visuo-Spatial Short-Term Memory Test
Inspired by the [work](https://www.sciencedirect.com/science/article/pii/S096098220702088X) done by Dr. Tetsuro Matsuzawa et al. on the working memory capabilities of chimpanzees, I developed a similar memory test. [Here](https://www.youtube.com/watch?v=ktkjUjcZid0) is a video explaining Dr. Matsuzawa's findings and showcasing the astonishing capacity of chimpanzees to learn and remember the position of 9 Arabic numerals in an 8x5 grid in merely 0.5 seconds. For reference, when given 1.5 seconds, I average 4.11 numerals correctly remembered. I correctly remember, with 1.5 seconds, all 9 numerals 0.38% of the time. Ayumu, one of the chimpanzees working with Dr. Matsuzawa when given 0.5 seconds remembers all 9 numerals around 90% of the time.


![ayumu](https://user-images.githubusercontent.com/26527575/184551252-6999324c-b2ae-4bee-9da6-051d9c637e9f.gif)



# Tests
Different experimental settings are useful to test visuo-spatial short-term memory. The software developed allows for 2 main modes of testing:
- one in which the numerals are hidden after a set amount of time
- one in which the numerals are hidden after the first numeral has been clicked

3 more modes of testing are:
- one in which the grid is covered in white squares from the start

TODO:

- one in which the grid is covered in white squares once the subject engages the test
- one in which only the squares corresponding to the numerals are rendered

Similarly to the tests developed by Dr. Matsuzawa, the test is initiated when a circular button is pressed and the feedback regarding the result of the test is given through sound: two descending tones will be played when a test is failed and three ascending tones will be played when the test is passed.

The results of each test are saved in a human-friendly (and computer-friendly too) .csv file.

# Installation and use
The software is written in python 3.8 and requires PyQt5, specifics are contained in requirements.txt which can be used in conjunction with pip install to get all necessary dependencies. To get help running the test, use `python test_loop.py -h` which will display the help text specifying the arguments that can be given to the software.

# Example


https://user-images.githubusercontent.com/26527575/184550952-516a8455-f0b5-4a6f-a519-e2e88a779c83.mp4

