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


def convert_to_ascii(file: str) -> str:
    chars: str = "@%#*+=-:. "

    img: Image = Image.open(file)
    img = img.convert('L')
    with open('result.txt', 'w') as ret:

        width, height = img.size
        aspect_ratio: float = height / width
        new_height: int = 100
        new_width: int = int(aspect_ratio * new_height)
        img.thumbnail((new_width, new_height))

        pixels = img.load()
        width, height = img.size

        for i in range(height):
            for j in range(width):
                scaled_value: int = int(pixels[j, i] * (len(chars) - 1) / 255)
                ret.write(chars[scaled_value])
            ret.write('\n')
        return ret.name


def main():
    print("Hello! Welcome to ASCpii, a .jpg to ASCII converter!")
    directory: str = input("\nEnter image folder name: ")
    files: list[str] = take_files(directory)

    while not files:
        print("No images loaded.")
        directory = input("\nEnter image folder name: ")
        files = take_files(directory)

    index: int = choose_file(directory, contents=files)
    result_file = convert_to_ascii(files[index])
    print(f"Image converted! Check {result_file}!")


if __name__ == "__main__":
    main()
