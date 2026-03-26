cap_letters = "ABCDE"
low_letters = "abcde"
num = "12345"
special_chars = "$&%"
possible_chars = cap_letters + low_letters + num + special_chars
valid_starts = cap_letters + low_letters

# Precompute category increments to avoid repeated set membership checks in recursion.
char_deltas = {}
for char in possible_chars:
    char_deltas[char] = (
        1 if char in cap_letters else 0,
        1 if char in low_letters else 0,
        1 if char in num else 0,
        1 if char in special_chars else 0,
    )

password_length = int(input("Enter the length of the password to generate: "))
total_combinations = len(possible_chars) ** password_length


BUFFER_SIZE = 10000  
buffer = []
added_passwords = 0

with open("task1.2/possible_passwords.txt", "w") as file:

    def generate_password(password_list, current_length, cap_count, low_count, num_count, spcl_count):
        global added_passwords, buffer
        if cap_count > 2 or spcl_count > 2:
            return

        # Prune branches that cannot satisfy the required character categories.
        remaining_slots = password_length - current_length
        missing_required = ((1 if cap_count == 0 else 0) + (1 if low_count == 0 else 0) + (1 if num_count == 0 else 0) + (1 if spcl_count == 0 else 0))
        if missing_required > remaining_slots:
            return
            
        if current_length == password_length:
            if cap_count > 0 and low_count > 0 and num_count > 0 and spcl_count > 0:
                added_passwords += 1
                
        
                buffer.append(f"{added_passwords}. {''.join(password_list)}\n")
                
                # If buffer is full, flush it to the file and clear it
                if len(buffer) >= BUFFER_SIZE:
                    file.writelines(buffer)
                    buffer.clear()
            return
          
        # Choose the right character set based on position
        chars_to_check = valid_starts if current_length == 0 else possible_chars
        
        for char in chars_to_check:
            cap_delta, low_delta, num_delta, spcl_delta = char_deltas[char]
            new_cap = cap_count + cap_delta
            new_low = low_count + low_delta
            new_num = num_count + num_delta
            new_spcl = spcl_count + spcl_delta
            
            password_list.append(char)
            
            generate_password(password_list, current_length + 1, new_cap, new_low, new_num, new_spcl)
            
          
            password_list.pop()

    # Start generator
    generate_password([], 0, 0, 0, 0, 0)
    
    # Clean up: Write any remaining passwords left in the buffer after recursion finishes
    if buffer:
        file.writelines(buffer)

print(f"Passwords added to file: {added_passwords} out of {total_combinations} total combinations.")