import bcrypt

class Bcrypt:
    def hash_password(password : str):
        passwordBytes = password.encode("utf-8")
        hashedPass = bcrypt.hashpw(passwordBytes, bcrypt.gensalt())
        return hashedPass.decode("utf-8")
    
    def validate_password(password: str, hashedPassword: str):
        passBytes = password.encode("utf-8")
        storedHasbytes = hashedPassword.encode("utf-8")

        return bcrypt.checkpw(passBytes, storedHasbytes)