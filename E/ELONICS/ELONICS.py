import string

def convert_to_elonic(n):
    alphabet = string.ascii_uppercase
    letter_index = (n - 1) // 10  # Determine the prefix group
    digit = (n - 1) % 10  # Determine the trailing digit

    if letter_index < len(alphabet):
        prefix = alphabet[letter_index]
    else:
        # Expand into multi-letter sequences (AA, AB, etc.) for higher values
        multi_letter = ""
        while letter_index >= 0:
            multi_letter = alphabet[letter_index % 26] + multi_letter
            letter_index = (letter_index // 26) - 1
        prefix = multi_letter

    return f"{prefix}{digit}"

def main():
    while True:
        user_input = input("\nEnter a number to convert (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        if user_input.isdigit():
            num = int(user_input)
            elonic = convert_to_elonic(num)
            print(f"{num} → {elonic}")
        else:
            print("Please enter a valid number!")

if __name__ == "__main__":
    main()
