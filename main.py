import secrets
import pyaes as aes
import string
import base64
from PIL import Image

class SecretManager:
    def __init__(self):
        pass

    def key_generator(self, length: int = 32) -> str:
        character_base = string.ascii_letters + string.digits + string.punctuation

        return "".join([secrets.choice(character_base) for i in range(length)])

    def encrypt_encode(self, algorithm:aes, data:bytes) -> bytes:
        '''
        used to aply DES encryptionand then encoding in Base64
        algorithm:des is the class that implements the DES algorithm
        data:bytes are the data to be encrypted
        '''
        secret = algorithm.encrypt(data)
        return base64.b64encode(secret).decode('utf-8')

    def decrypt_decode(self, algorithm:aes, secret:str) -> bytes:
        '''
        Used to decode a base64 secret and decryting it using DES
        algorithm:des is the class that implements the DES algorithm
        secret:bytes are the secret to be decrypted
        '''
        clear = base64.b64decode(secret.encode('utf-8'))
        return algorithm.decrypt(clear)


class ImageManager:
    def __init__(self):
        pass

    def generate_data(self, message:str) -> list:
        '''
        Used to generate a list of bytes from a string
        '''
        return [format(ord(i), '08b') for i in message]

    def BinaryToDecimal(self, binary):
        decimal, i = 0, 0
        while(binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary//10
            i += 1
        return (decimal)

    def _modify_pixels(self, message: str, image: Image) -> Image:
        '''
        Used to encode every character of the message in the image using 8 bits per character
        the last bit from the eigth bit is used to indicate if the character is the last one
        
        Atributes:
        message:str is the message to be encoded in the image
        image:Image is the image to use as container for the message
        '''
        data = self.generate_data(message)
        imgData = iter(Image.Image.getdata(image))

        for i in range(len(data)):
            # Extract three pixels at a time from the image
            pixel = [value for value in imgData.__next__()[:3] +
                    imgData.__next__()[:3] +
                    imgData.__next__()[:3]]

            # Pixel value should be made
            # odd for 1 and even for 0
            for j in range(0, 8):
                if (data[i][j] == '0') and (pixel[j] % 2 != 0):
                    if (pixel[j] % 2 != 0):
                        if (pixel[j] - 1) >= 0:
                            pixel[j] -= 1
                        else:
                            pixel[j] += 1

                elif (data[i][j] == '1') and (pixel[j] % 2 == 0):
                    if (pixel[j] -1) >= 0:
                        pixel[j] -= 1
                    else:
                        pixel[j] += 1

            # Eighth pixel of every set tells whether to stop ot read further.
            # 0 means keep reading; 1 means the message is over.
            if (i == len(data) - 1):
                if (pixel[-1] % 2 == 0):
                    pixel[-1] -= 1
            else:
                if (pixel[-1] % 2 != 0):
                    pixel[-1] -= 1

            # Place the modified pixels back in the image
            pixel = tuple(pixel)
            yield pixel[:3]
            yield pixel[3:6]
            yield pixel[6:9]

    def encode_in_image(self, message: str, image: str) -> Image:
        '''
        Used to encode a message in an image using tree pixels per character
        the last bit from the eigth bit is used to indicate if the character is the last one

        Atributes:
        message:str is the message to be encoded in the image
        image:Image is the image to use as container for the message
        '''
        image = Image.open(image, 'r')
        w = image.size[0]
        (x, y) = (0, 0)

        for pixel in self._modify_pixels(message, image):
            # Putting modified pixels in the new image
            image.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

        return image

    def decode_from_image(self, image: Image) -> str:
        '''
        Used to decode a message from an image using tree pixels per character
        the last bit from the eigth bit is used to indicate if the character is the last one

        Atributes:
        image:Image is the image used as container for the message
        '''
        imgData = iter(Image.Image.getdata(image))
        message = ''

        while (True):
            # Extract three pixels at a time from the image
            pixel = [value for value in imgData.__next__()[:3] +
                    imgData.__next__()[:3] +
                    imgData.__next__()[:3]]

            # string of binary data
            binstr = ''

            for i in pixel[:8]:
                if (i % 2 == 0):
                    binstr += '0'
                else:
                    binstr += '1'
            
            message += chr(self.BinaryToDecimal(int(binstr)))
            # message is over if the eighth pixel
            # is not even
            if (pixel[-1] % 2 != 0):
                return message

def get_string_input(input_message: str, error_message: str) -> str:
    while True:
        value = input(input_message)

        if not value:
            print(error_message)
            continue
        else:
            return value


def first_option():
    secret_manager = SecretManager()
    image_manager = ImageManager()

    message = get_string_input(
        "Ingrese el mensaje que desea codificar\n", "Ingrese un mensaje para encriptar"
    )

    image_path = get_string_input(
        "Ingrese la ruta para la imagen base\n", "Ingrese la ruta de la imagen"
    )

    key = secret_manager.key_generator()
    algorithm = aes.aes.AESModeOfOperationCTR(
        bytes(key, encoding="ascii"), aes.Counter(100)
    )
    secret = secret_manager.encrypt_encode(algorithm, message)
    print(f"Su clave privada es: >> {key} <<")

    new_image = image_manager.encode_in_image(secret, image_path)
    new_image.save("encoded_image." + image_path.split(".")[-1])


def second_option():
    secret_manager = SecretManager()
    image_manager = ImageManager()

    image_path = get_string_input(
        "Ingrese la ruta para la imagen base\n", "Ingrese la ruta de la imagen"
    )
    key = input("Ingrese su clave privada: ")

    image = Image.open(image_path)
    algorithm = aes.aes.AESModeOfOperationCTR(
        bytes(key, encoding="ascii"), aes.Counter(100)
    )

    secret = image_manager.decode_from_image(image)
    message:str = secret_manager.decrypt_decode(algorithm, secret)

    print(f"El mensaje oculto es: >> {str(message)} <<")

def selection_menu() -> None:
    while True:
        error = True
        selection = input(
            "A continuación seleccione que desea hacer:\n\
            1) Encriptar un nuevo mensaje\n\
            2) Desencriptar un mensaje\n\
            3) Finalizar la ejecución\n"
        )

        if selection == "1":
            first_option()
            error = False
        elif selection == "2":
            second_option()
            error = False
        elif selection == "3":
            exit()

        if error:
            print("Su selección no pudo ser admitida, intente nuevamente\n")
        else:
            decision = input("finalizó la ejecución, desea continuar? (s/n)\n")
            if decision != "s":
                break


def main():
    print("Bienvenido al sistema de encriptación esteganografico!!\n\n")
    selection_menu()


if __name__ == "__main__":
    main()
