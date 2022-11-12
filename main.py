from PIL import Image
from io import TextIOWrapper
import sys

def get_file(query:str, is_reading:bool = False) -> TextIOWrapper:
    '''
    Return the file given as input
    
    Arguments:
        - is_reading: True if the file is going to be used for reading, False if it's going to be used for writing
    
    Return the'''
    file:str = input(f'Enter the path to the {query} file: ')
    
    if is_reading:
        return open(file, 'r')
    
    return open(file, 'w')

def get_image(is_saving:bool = False) -> Image:
    '''Return the image given as input'''
    image_path:str = input('Enter the path to the image: ')
    
    if is_saving:
        return Image.save()


def hide() -> None:
    '''Hide a message in an image'''
    img = get_image()
    message = get_file('message', is_reading=True)
    height, width = img.size



    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if index < len(message):
                r = ord(message[index])
                index += 1
            if index < len(message):
                g = ord(message[index])
                index += 1
            if index < len(message):
                b = ord(message[index])
                index += 1
            img.putpixel((col, row), (r, g, b))
    
    print('Message hidden successfully!')

def main() -> None:
    '''Main function'''
    try:
        option:int = int(input('''
        Welcome to the steganography program!\n
        1. Hide a message in an image
        2. Retrieve a message from an image
        3. Exit
        '''))

        if option == 1:
            hide()
        elif option == 2:
            retrieve()
        elif option == 3:
            sys.exit()
        else:
            print('Invalid option!')
    except Exception as e:
        print(e)
        sys.exit(1)

# Driver code
if __name__ == '__main__':
    main()
