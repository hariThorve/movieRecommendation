import bcrypt

def hash_password(password : str):
    passwordBytes = password.encode("utf-8")
    # Generate a salt and hash the password in one step
    hashedPass = bcrypt.hashpw(passwordBytes, bcrypt.gensalt())
    return hashedPass.decode("utf-8")

def validatePass(password : str, hashedPassword : str):
    # convert inputs to bytes
    passBytes = password.encode('utf-8')
    storedHashBytes = hashedPassword.encode('utf-8')

    return bcrypt.checkpw(passBytes, storedHashBytes)

password = "harry123"

hp = hash_password(password=password)
print(hp)
print(validatePass(password=password, hashedPassword=hp))