from PIL import Image
import glob


def take_files(folder: str) -> list[str]:
    return glob.glob(folder + '/*.jpg')


def choose_file(folder: str, contents: list[str]) -> int:
    print(f"Options from {folder}:\n")
    for index, file in enumerate(contents, 1):
        print(index, file, sep=': ')

    option: str = input("\nPick an option: ")
    try:
        if 0 <= int(option) - 1 < len(contents):
            return int(option) - 1
        else:
            raise ValueError
    except ValueError:
        invalid_scope = option.isnumeric() and not 0 <= int(option) - 1 < len(contents)

        while invalid_scope or not option.isnumeric():
            print("Invalid; please pick a valid option!")
            option = input("\nPick an option: ")

            invalid_scope = option.isnumeric() and not 0 <= int(option) - 1 < len(contents)

    return int(option) - 1


def convert_to_ascii(file: str):
    chars = """@QB#NgWM8RDHdOKq9$6khEPXwmeZaoS2yjufF]}{tx1zv7lciL/\|?*>r^;:_"~,'.-` """

    img = Image.open(file)
    img = img.resize((178, 100))  # TODO: i want to be able to scale image based on aspect ratio
    img = img.convert('L')
    pixels = img.load()

    width, height = img.size
    ret = open('result.txt', 'w')

    for i in range(height):
        for j in range(width):
            scaled_value = int(pixels[j, i] * 65 / 255)
            ret.write(chars[scaled_value])
        ret.write('\n')


def main():
    print("Hello! Welcome to ASCpii, a .jpg to ASCII converter!")
    directory = input("\nEnter image folder name: ")
    files = take_files(directory)
    while not files:
        print("No images loaded.")
        directory = input("\nEnter image folder name: ")
        files = take_files(directory)

    index = choose_file(directory, contents=files)
    convert_to_ascii(files[index])
    print(f"Image converted! Check {glob.glob('result.txt')}")


if __name__ == "__main__":
    main()
