cap_letters = "ABCDE"
low_letters = "abcde"
num = "12345"
special_chars = "$&%"
possible_chars = cap_letters + low_letters + num + special_chars
valid_starts = cap_letters + low_letters


cap_letters_set = set(cap_letters)
low_letters_set = set(low_letters)
num_set = set(num)
special_chars_set = set(special_chars)
valid_starts_set = set(valid_starts)

password_length = int(input("Enter the length of the password to generate: "))
max_pass = len(possible_chars) ** password_length


BUFFER_SIZE = 10000  
buffer = []
added_passwords = 0

with open("task1.2/possible_passwords.txt", "w") as file:

    def generate_password(password_list, cap_count, low_count, num_count, spcl_count):
        global added_passwords, buffer
        if cap_count > 2 or spcl_count > 2:
            return
            
        if len(password_list) == password_length:
            if cap_count > 0 and low_count > 0 and num_count > 0 and spcl_count > 0:
                added_passwords += 1
                
        
                buffer.append(f"{added_passwords}. {''.join(password_list)}\n")
                
                # If buffer is full, flush it to the file and clear it
                if len(buffer) >= BUFFER_SIZE:
                    file.writelines(buffer)
                    buffer.clear()
            return
          
        for char in possible_chars:
            if len(password_list) == 0 and char not in valid_starts_set:
                continue
                
            # Calculate new counts but DON'T reassign the loop variables
            new_cap = cap_count + (1 if char in cap_letters_set else 0)
            new_low = low_count + (1 if char in low_letters_set else 0)
            new_num = num_count + (1 if char in num_set else 0)
            new_spcl = spcl_count + (1 if char in special_chars_set else 0)
            
            password_list.append(char)
            
            generate_password(password_list, new_cap, new_low, new_num, new_spcl)
            
          
            password_list.pop()

    # Start generator
    generate_password([], 0, 0, 0, 0)
    
    # Clean up: Write any remaining passwords left in the buffer after recursion finishes
    if buffer:
        file.writelines(buffer)

print(f"Passwords added to file: {added_passwords} out of {max_pass} possible combinations.")