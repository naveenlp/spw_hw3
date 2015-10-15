import random
from string import ascii_letters, digits, punctuation

def add_random_noise(password):
    noise_chars = digits + ascii_letters + punctuation
    noise_length = random.randint(1,9)

    noise = [random.choice(noise_chars) for i in range(0, noise_length)]
    noise = ''.join(str(num) for num in noise)

    pre_post_choice = random.randint(0,1)
    if pre_post_choice == 0:
        noisy_pass = password + noise
    else:
        noisy_pass = noise + password
    return noisy_pass

def add_num_digit_noise(password):
    noise_chars = digits + ascii_letters
    noise_length = random.randint(1,9)

    noise = [random.choice(noise_chars) for i in range(0, noise_length)]
    noise = ''.join(str(num) for num in noise)

    pre_post_choice = random.randint(0,1)
    if pre_post_choice == 0:
        noisy_pass = password + noise
    else:
        noisy_pass = noise + password
    return noisy_pass

def add_num_noise(password):
    noise_length = random.randint(1,9)


    noise = [random.randint(0,9) for i in range(0, noise_length)]
    noise = ''.join(str(num) for num in noise)


    pre_post_choice = random.randint(0,1)
    if pre_post_choice == 0:
        noisy_pass = password + noise
    else:
        noisy_pass = noise + password
    return noisy_pass

def chop(password):
    noise_length = random.randint(0,len(password)-6)

    pre_post_choice = random.randint(0,2)
    if pre_post_choice == 0:
        noisy_pass = password[0:len(password)-noise_length]
    elif pre_post_choice == 1:
        noisy_pass = password[noise_length:]
    else:
        start = noise_length/2
        noisy_pass = password[start:len(password)-start]
    return noisy_pass
