import random

caps_letters = "ABCDE"
low_letters = "abcde"
nums = "12345"
special_chars = "$&%"
possible_chars = caps_letters + low_letters + nums + special_chars
valid_sarts = caps_letters + low_letters
password_length = int(input("Enter the length of the password to crack: "))
open("task1.2/possible_passwords.txt", "w").close()  # Clear the file before writing new passwords
max_pass =  len(possible_chars) ** password_length
i = 0
while i < max_pass:
    password = ''.join(random.choice(possible_chars) for _ in range(password_length))
    with open("task1.2/possible_passwords.txt", "a") as file:
        if password[0] in valid_sarts:
            count = 0
            count += sum(1 for char in password if char in caps_letters)
            if count >0 and count<= 2:
                count = 0
                count += sum(1 for char in password if char in special_chars)
                if count > 0 and count <= 2:
                    count = 0
                    count += sum(1 for char in password if char in nums)
                    if count > 0:
                        count = 0
                        count += sum(1 for char in password if char in low_letters)
                        if count > 0:
                            file.write(password + "\n")
    i += 1

print(f"Passwords added to file")