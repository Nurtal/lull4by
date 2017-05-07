'''
hide a short message (255 char max) in an image
the image has to be .bmp or .png format
and the image mode has to be 'RGB'
'''
from PIL import Image
import os
import shutil
import sys
import getopt

def encode_image(img, msg):
    """
    use the red portion of an image (r, g, b) tuple to
    hide the msg string characters as ASCII values
    red value of the first pixel is used for length of string
    """
    length = len(msg)
    # limit length of message to 255
    if length > 255:
        print("[!] text too long! (don't exeed 255 characters)")
        return False
    if img.mode != 'RGB':
        print("[!] image mode needs to be RGB")
        return False
    # use a copy of image to hide the text in
    encoded = img.copy()
    width, height = img.size
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            # first value is length of msg
            if row == 0 and col == 0 and index < length:
                asc = length
            elif index <= length:
                c = msg[index -1]
                asc = ord(c)
            else:
                asc = r
            encoded.putpixel((col, row), (asc, g , b))
            index += 1
    return encoded

def decode_image(img):
    """
    check the red portion of an image (r, g, b) tuple for
    hidden message characters (ASCII values)
    """
    width, height = img.size
    msg = ""
    index = 0
    for row in range(height):
        for col in range(width):
            try:
                r, g, b = img.getpixel((col, row))
            except ValueError:
                # need to add transparency a for some .png files
                r, g, b, a = img.getpixel((col, row))		
            # first pixel r value is length of message
            if row == 0 and col == 0:
                length = r
            elif index <= length:
                msg += chr(r)
            index += 1
    return msg




def main(argv):
   action = ''
   image = ''
   message = ''
   try:
      opts, args = getopt.getopt(argv,"a:i:m:",["action=","image=","message="])
   except getopt.GetoptError:
   	print "[!] error"
   	print 'trickyImage.py -a <action> -i <image> -m <message>'
   	sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'trickyImage.py -a <action> -i <image> -m <message>'
         print "\taction: the action to perform, e for encryption, d for decipher"
         print "\timage: the image used to hide the message"
         print "\tmessage: the message to hide"
         print "\n\texemple: trickyImage.py -a e -i test.png -m in darkness he came"
         sys.exit()
      elif opt in ("-a", "--action"):
         action = arg
      elif opt in ("-i", "--image"):
      	image = arg
      elif opt in ("-m", "--message"):
      	message = arg

   # run programm with args
   original_image_file = image
   img = Image.open(original_image_file)
   
   # image mode needs to be 'RGB'
   if(img.mode != "RGB"):
       print "[!] image mode needs to be RGB"
       sys.exit(2)


   if(action == "e"):   	   
   	   # create a new filename for the modified/encoded image
   	   encoded_image_file = "enc_" + original_image_file

   	   # don't exceed 255 characters in the message
   	   secret_msg = message

   	   img_encoded = encode_image(img, secret_msg)
   	   if img_encoded:
   	       # save the image with the hidden text
   	       img_encoded.save(encoded_image_file)
   	       print "[*] message encrypted"

   	       shutil.copy(encoded_image_file, original_image_file)
   	       os.remove(encoded_image_file)

   elif(action == "d"):
   	   img = Image.open(original_image_file)
   	   hidden_text = decode_image(img)
   	   print("[*]Hidden text:\n{}".format(hidden_text))

    
if __name__ == "__main__":
   main(sys.argv[1:])