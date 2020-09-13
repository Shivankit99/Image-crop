# Image-crop
This code will help anyone who is gathering their own dataset and has multiple images of different sizes and needs them to be square images(1:1).

The tool is very easy to use as it requires just one click and is a very user friengly GUI.
The pixel value of the click is the top of the cropped image then the biggest square below that pixel will be drawn. if its not the square you want to crop you can click again and adjust according to you need.

Steps to use the code:
1) Open new.py in any text editor/IDE
2) Edit lines 6 and 7, line number 6 is the path that has the actual images, and line number 7 is the path to where the cropped images are to be saved.
3) Once these lines have been updated you can either run the code from the IDE or from the command prompt.
4) To run from the command prompt - python3 new.py

Note:
1) The original images will be deleted as you press the save button and the new image will be saved to the specified folder.
2) You can always press exit at any point during the process, when you run the code again it will automatically pick up from the last photo you saw.
3) You can click multiple times on the image before pressing save, the last pressed would be taken as the final coordinates.
4) This works perfectly fine for images that have height>width. minor changes will be required in the function cut_square() for width>height images
