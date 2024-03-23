from PIL import Image
import glob


def take_files(folder: str) -> list[str]:
    return glob.glob(folder + '/*')


def in_bounds(choice: int, length: int) -> bool:
    return choice in range(0, length)


def choose_file(folder: str, contents: list[str]) -> int:
    print(f"Options from {folder}:\n")
    for index, file in enumerate(contents, 1):
        print(index, file, sep=': ')

    option: str = input("\nPick an option: ")

    try:
        if in_bounds(int(option) - 1, len(contents)):
            return int(option) - 1
        else:
            raise ValueError
    except ValueError:
        while (option.isnumeric() and not in_bounds(int(option) - 1, len(contents))) or not option.isnumeric():
            print("Invalid; please pick a valid option!")
            option = input("\nPick an option: ")

    return int(option) - 1


def convert_to_ascii(file: str, new_height: int, chars="@%#*+=-:. ") -> str:
    """
    TODO: ASCII characters are taller than they are wider, I need to configure the algorithm with this in mind.
    TODO: The calculation of width with respect to height must be modified.
    """
    img: Image = Image.open(file)
    img = img.convert('L')
    with open('result.txt', 'w') as ret:

        width, height = img.size
        aspect_ratio: float = width / height
        new_width: int = int(aspect_ratio * new_height)
        img.thumbnail((new_width, new_height))

        pixels = img.load()
        width, height = img.size

        for i in range(height):
            for j in range(width):
                scaled_value: int = int(pixels[j, i] * (len(chars) - 1) / 255)
                ret.write(chars[scaled_value])
            ret.write('\n')
        img.close()
        return ret.name


def take_int_option(value: str, measurement: str) -> int:
    choice: str = input(f"Enter {value} in {measurement}: ")
    try:
        return int(choice)
    except ValueError:
        while not choice.isnumeric():
            choice = input(f"Not an integer!\n"
                           f"Please re-enter {value} in {measurement}: ")
    return int(choice)


def take_bool_option(true: str, false: str) -> bool:
    valid_choices: tuple[str, str] = (true.lower(), false.lower())
    choice: str = input(f"Choose an option ({true}/{false}): ").lower()
    while choice not in valid_choices:
        choice = input("Invalid choice!\n"
                       f"Please re-enter ({true}/{false}): ").lower()

    return choice == true.lower()


def main():
    print("Hello! Welcome to ASCpii, an image to ASCII converter!")
    directory: str = input("\nEnter image folder name: ")
    files: list[str] = take_files(directory)

    while not files:
        print("No images loaded.")
        directory = input("\nEnter image folder name: ")
        files = take_files(directory)

    index: int = choose_file(directory, contents=files)
    converted_height: int = 100
    print("\nWould you like to change the converted image height?\n"
          "(default is 100px)")
    if take_bool_option("Y", "N"):
        converted_height: int = take_int_option("new height", "pixels")
    result_file: str = convert_to_ascii(files[index], converted_height)
    print(f"\nImage converted! Check {result_file}!")


if __name__ == "__main__":
    main()
