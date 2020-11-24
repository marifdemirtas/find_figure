# find_figure
A command line tool written in Python for getting the borders for the largest figure in a given PDF document.

By looking at the pixels where there is a color change, finds the distance from the borders of a rectangle around the largest figure to the borders of the page. Can be used as a command line tool or can be imported for using on other image formats. 

Uses pdf2image for reading the PDF, PIL and numpy for image manipulation.
