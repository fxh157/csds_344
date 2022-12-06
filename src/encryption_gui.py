from PyQt5.QtWidgets import *
import sympy
from vigenere import encrypt_vigenere, decrypt_vigenere
from des import des_algorithm
from rsa import encrypt_rsa, decrypt_rsa, create_keys
from md5 import encrypt_md5, md5
import sys

class encryptionGUI(QDialog):
    def __init__(self):
        super().__init__()
        self.assemble_gui()

    def assemble_gui(self):
        self.private_rsa_key = 0

        self.setWindowTitle("Encryption Chicken")
        self.setFixedWidth(700)

        encrypt_label = QLabel("&Input Message: ",self)
        encrypt_input_space = QLineEdit(self)
        encrypt_label.setBuddy(encrypt_input_space)

        decrypt_label = QLabel("&Decrypt Message: ",self)
        decrypt_input_space = QLineEdit(self)
        decrypt_label.setBuddy(decrypt_input_space)

        key_label = QLabel("&Key: ",self)
        key_input_space = QLineEdit(self)
        key_label.setBuddy(key_input_space)

        encryption_choices = QComboBox()
        encryption_choices.addItems(["Select cipher", "Vigenere Cipher", "DES", "RSA", "md5-Checksum"])

        
        def check_hex(s):
            try:
                n = int(s,16)
                return True
            except ValueError:
                return False

        def encrypt_button_clicked():
            RSA = False
            message = encrypt_input_space.text()
            key = key_input_space.text()
            encryption_type = encryption_choices.currentText()
            if encryption_type == "RSA" or encryption_type == "md5-Checksum":
                key_input_space.setText("")
                key = ""
                RSA = True
            if len(key) != 0 and len(message) != 0 or RSA:
                if encryption_type == "Vigenere Cipher":
                    encrypted_message_body.setText(encrypt_vigenere(message,key))
                elif encryption_type == "DES": 
                    if check_hex(key):
                        encrypted_message_body.setText(des_algorithm(message, key, encrypt=True))
                    else:
                        key_input_space.setText("")
                elif encryption_type == "RSA":
                    public_key, private_key = create_keys(sympy.randprime(100, 500), sympy.randprime(100,500))
                    self.private_rsa_key = private_key
                    cipher = encrypt_rsa(message, public_key)
                    string_cipher = "-".join([str(e) for e in cipher])
                    encrypted_message_body.setText(string_cipher)
                elif encryption_type == "md5-Checksum":
                    encrypted_message_body.setText(encrypt_md5(message, key))

        def decrypt_button_clicked():
            RSA = False
            message = decrypt_input_space.text()
            key = key_input_space.text()
            encryption_type = encryption_choices.currentText()
            if encryption_type == "RSA" or encryption_type == "md5-Checksum":
                RSA = True
            if len(key) != 0 and len(message) != 0 or RSA:
                if encryption_type == "Vigenere Cipher":
                    decrypted_message_body.setText(decrypt_vigenere(message,key))
                elif encryption_type == "DES":
                    if check_hex(key):
                        decrypted_message_body.setText(des_algorithm(message, key, encrypt=False))
                    else:
                        key_input_space.setText("")
                elif encryption_type == "RSA":
                    message = [int(m) for m in message.split("-")]
                    decrypted_message_body.setText(decrypt_rsa(message, self.private_rsa_key))

        def move_encryption_button_clicked():
            if encryption_choices.currentText() != "md5-Checksum":
                encrypted_message = encrypted_message_body.text()
                decrypt_input_space.setText(encrypted_message)
        
        def clear_button_clicked():
            decrypt_input_space.setText("")
            encrypt_input_space.setText("")
            key_input_space.setText("")
            decrypted_message_body.setText("")
            encrypted_message_body.setText("")

        clear_button = QPushButton('Clear')
        clear_button.clicked.connect(clear_button_clicked)

        encrypt_button = QPushButton('Encrypt')
        encrypt_button.clicked.connect(encrypt_button_clicked)
        decrypt_button = QPushButton('Decrypt')
        decrypt_button.clicked.connect(decrypt_button_clicked)
        move_encryption_button = QPushButton('Move Encryption')
        move_encryption_button.clicked.connect(move_encryption_button_clicked)

        encrypted_message_label = QLabel("Encrypted Message: ",self)
        encrypted_message_body = QLineEdit("", self)
        encrypted_message_label.setBuddy(encrypted_message_body)

        decrypted_message_label = QLabel("Decrypted Message: ",self)
        decrypted_message_body = QLineEdit("", self)
        decrypted_message_label.setBuddy(decrypted_message_body)

        main_layout = QGridLayout(self)
        
        main_layout.addWidget(key_label,0,0)
        main_layout.addWidget(key_input_space,0,1,1,2)
        main_layout.addWidget(encryption_choices,0,4,1,2)
        main_layout.addWidget(clear_button,0,6,1,1)
        
        main_layout.addWidget(encrypt_label,1,0)
        main_layout.addWidget(encrypt_input_space,1,1,1,2)
        main_layout.addWidget(decrypt_label,1,4)
        main_layout.addWidget(decrypt_input_space,1,5,1,2)
        
        main_layout.addWidget(encrypt_button,2,2,1,1)
        main_layout.addWidget(decrypt_button,2,6,1,1)

        main_layout.addWidget(encrypted_message_label,3,0,1,1)
        main_layout.addWidget(encrypted_message_body,3,1,1,2)
        main_layout.addWidget(decrypted_message_label,3,4,1,1)
        main_layout.addWidget(decrypted_message_body,3,5,1,2)

        main_layout.addWidget(move_encryption_button,4,1,1,2)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = encryptionGUI()
    main.show()
    sys.exit(app.exec_())
