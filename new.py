from tkinter import *
import cv2
from PIL import Image, ImageTk
import os
root = Tk()
path = r'Enter path to original images'
final_path = r'Enter path to final destination'

def make_global():

    global img_number
    img_number = 0
    global image_list
    image_list = []
    global photo_image_list
    photo_image_list = []
    global resized
    resized = []
    global scale_percent
    scale_percent = []


make_global()
def read_image(img_name):

    img = cv2.imread(os.path.join(path,img_name))
    # Rearrange the color channel
    b, g, r = cv2.split(img)
    img = cv2.merge((r, g, b))
    height,width,channel = img.shape
    #print('height in read',height)
    if height < 1000:
        scale_percent.append(50)
    elif height < 2000:
        scale_percent.append(33)
    elif height < 3000:
        scale_percent.append(24)
    elif height < 4000:
        scale_percent.append(15)
    else:
        scale_percent.append(13)

    new_height = int(height * scale_percent[-1] / 100)
    new_width = int(width * scale_percent[-1] / 100)
    dim = (new_width, new_height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    print("Old Dimensions:  ",width,height)
    print("Scale Percentage:  ",scale_percent[-1])
    print("New Dimensions: ",dim)
    # A root window for displaying objects
    # Convert the Image object into a TkPhoto object
    im = Image.fromarray(resized)
    imgtk = ImageTk.PhotoImage(image=im)
    return imgtk,img,resized

def load_images(path):
    global img_list
    img_list = os.listdir(path)
    total_size = len(img_list)
    ct = 0
    new_img_list = []
    for i in img_list:
        print(ct," of ",total_size)
        print(i)
        imgtk,img,resized_img = read_image(i)
        new_img_list.append(imgtk)
        image_list.append(img)
        resized.append(resized_img)
        ct = ct + 1
        print()
        print()
    return new_img_list

def cut_from_here(event):
    #print(event.x,event.y)
    y_coordinate = event.y
    #print('img_number in mouse click',img_number)
    y_actual = y_coordinate * 100 / scale_percent[img_number]
    #print(scale_percent[img_number])
    print('y on new image', y_coordinate)
    print('y on actual image', int(y_actual))
    original_image_height, original_image_width, channel = image_list[img_number].shape
    global y_actual_image
    y_actual_image = int(y_actual)

    new_image_height, new_image_width, channel = resized[img_number].shape
    print('height', new_image_height)
    print('width', new_image_width)
    canvas.grid_forget()
    newcanvas = Canvas(root, width=900, height=900, background='white')
    newcanvas.create_image(50, 0, image=photo_image_list[img_number], anchor=NW)
    newcanvas.grid(row=0, column=0)
    newcanvas.bind('<Button-1>', cut_from_here)
    Save_button = Button(root, text='Save', command=lambda:cut_square(img_number))
    exit_button = Button(root, text='Exit', command=root.quit)
    #next_button = Button(root, text='Next Image', command=lambda: forward(img_number + 1))
    Save_button.grid(row=0, column=1)
    exit_button.grid(row=0, column=2)
    #next_button.grid(row=0, column=3)
    newcanvas.create_rectangle(50, y_coordinate, new_image_width + 50, y_coordinate + new_image_width, fill='')

def cut_square(img_number):
    #print('img number',img_number)
    #print(y_actual_image,y_actual_image + image_list[img_number].shape[1],0,image_list[img_number].shape[1])
    img = image_list[img_number]
    im_crop = img[y_actual_image:y_actual_image + image_list[img_number].shape[1],0:image_list[img_number].shape[1]]
    b, g, r = cv2.split(im_crop)
    im_crop = cv2.merge((r, g, b))
    save_to = os.path.join(final_path,img_list[img_number])
    cv2.imwrite(save_to,im_crop)
    print('Saved to: ',os.path.join(final_path,img_list[img_number]))
    os.remove(os.path.join(path,img_list[img_number]))

def forward(image_number):
    global Save_button
    global exit_button
    global next_button
    canvas.grid_forget()
    newcanvas = Canvas(root, width=900, height=900, background='white')
    newcanvas.create_image(50, 0, image=photo_image_list[image_number], anchor=NW)
    newcanvas.grid(row=0, column=0)
    Save_button = Button(root, text='Save', command=lambda: cut_square(image_number))
    next_button = Button(root, text='Next Image', command=lambda: forward(image_number + 1))
    exit_button = Button(root, text='Exit', command=root.quit)
    Save_button.grid(row=0, column=1)
    exit_button.grid(row=0, column=2)
    next_button.grid(row=0, column=3)
    newcanvas.bind('<Button-1>', cut_from_here)
    global img_number
    img_number = image_number

photo_image_list = load_images(path)
imgtk = photo_image_list[img_number]
canvas = Canvas(root,width = 900,height = 900, background = 'white')
canvas.create_image(50, 0, image=imgtk, anchor=NW)
canvas.grid(row = 0,column = 0)
canvas.bind('<Button-1>',cut_from_here)
Save_button = Button(root,text='Save',command = lambda : cut_square(img_number))
next_button = Button(root,text='Next Image',command = lambda: forward(img_number+1))
exit_button = Button(root,text='Exit',command = root.quit)
Save_button.grid(row=0,column=1)
exit_button.grid(row=0,column=2)
next_button.grid(row=0,column=3)
root.mainloop()

