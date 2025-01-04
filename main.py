

import ipfshttpclient
import os
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from colorama import Fore, Back, Style

# إعدادات IPFS
client = ipfshttpclient.connect("/dns/ipfs.infura.io/tcp/5001/https")

# دالة لتوليد مفتاح تشفير AES
def generate_key(password):
    return password.ljust(32)[:32].encode('utf-8')

    # دالة لتشفير الرسالة
    def encrypt_message(message, key):
        cipher = AES.new(key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
                iv = b64encode(cipher.iv).decode('utf-8')
                    ct = b64encode(ct_bytes).decode('utf-8')
                        return json.dumps({'iv': iv, 'ciphertext': ct})

                        # دالة لفك تشفير الرسالة
                        def decrypt_message(encrypted_message, key):
                            try:
                                    b64 = json.loads(encrypted_message)
                                            iv = b64decode(b64['iv'])
                                                    ct = b64decode(b64['ciphertext'])
                                                            cipher = AES.new(key, AES.MODE_CBC, iv)
                                                                    pt = unpad(cipher.decrypt(ct), AES.block_size)
                                                                            return pt.decode('utf-8')
                                                                                except Exception as e:
                                                                                        print(Fore.RED + "خطأ في فك التشفير: " + str(e))
                                                                                                return None

                                                                                                # دالة لتحميل الرسائل من IPFS
                                                                                                def fetch_message(cid):
                                                                                                    try:
                                                                                                            return client.cat(cid).decode('utf-8')
                                                                                                                except Exception as e:
                                                                                                                        print(Fore.RED + "خطأ في استرجاع الرسالة: " + str(e))
                                                                                                                                return None

                                                                                                                                # دالة لإرسال الرسالة عبر IPFS
                                                                                                                                def send_message(message, key):
                                                                                                                                    encrypted_message = encrypt_message(message, key)
                                                                                                                                        try:
                                                                                                                                                res = client.add_json(encrypted_message)
                                                                                                                                                        print(Fore.GREEN + "تم إرسال الرسالة بنجاح!")
                                                                                                                                                                print("CID للرسالة: ", res['Hash'])
                                                                                                                                                                        return res['Hash']
                                                                                                                                                                            except Exception as e:
                                                                                                                                                                                    print(Fore.RED + "خطأ في إرسال الرسالة: " + str(e))
                                                                                                                                                                                            return None

                                                                                                                                                                                            # واجهة المستخدم
                                                                                                                                                                                            def user_interface():
                                                                                                                                                                                                print(Style.BRIGHT + Fore.CYAN + "مرحبًا في تطبيق المراسلة الآمن!" + Style.RESET_ALL)
                                                                                                                                                                                                    
                                                                                                                                                                                                        # تسجيل الدخول
                                                                                                                                                                                                            username = input(Fore.YELLOW + "أدخل اسم المستخدم: " + Style.RESET_ALL)
                                                                                                                                                                                                                password = input(Fore.YELLOW + "أدخل كلمة المرور: " + Style.RESET_ALL)
                                                                                                                                                                                                                    
                                                                                                                                                                                                                        key = generate_key(password)
                                                                                                                                                                                                                            
                                                                                                                                                                                                                                while True:
                                                                                                                                                                                                                                        print(Fore.GREEN + "\nخيارات:")
                                                                                                                                                                                                                                                print("1. إرسال رسالة")
                                                                                                                                                                                                                                                        print("2. استلام رسالة")
                                                                                                                                                                                                                                                                print("3. الخروج")
                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                choice = input(Fore.YELLOW + "اختر خيارًا: " + Style.RESET_ALL)
                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                if choice == '1':
                                                                                                                                                                                                                                                                                                            message = input(Fore.CYAN + "أدخل الرسالة التي تريد إرسالها: " + Style.RESET_ALL)
                                                                                                                                                                                                                                                                                                                        cid = send_message(message, key)
                                                                                                                                                                                                                                                                                                                                    if cid:
                                                                                                                                                                                                                                                                                                                                                    print(Fore.GREEN + "تم إرسال الرسالة بنجاح!")
                                                                                                                                                                                                                                                                                                                                                            elif choice == '2':
                                                                                                                                                                                                                                                                                                                                                                        cid = input(Fore.CYAN + "أدخل CID الرسالة التي تريد استلامها: " + Style.RESET_ALL)
                                                                                                                                                                                                                                                                                                                                                                                    encrypted_message = fetch_message(cid)
                                                                                                                                                                                                                                                                                                                                                                                                if encrypted_message:
                                                                                                                                                                                                                                                                                                                                                                                                                decrypted_message = decrypt_message(encrypted_message, key)
                                                                                                                                                                                                                                                                                                                                                                                                                                if decrypted_message:
                                                                                                                                                                                                                                                                                                                                                                                                                                                    print(Fore.GREEN + "الرسالة المستلمة: " + decrypted_message)
                                                                                                                                                                                                                                                                                                                                                                                                                                                            elif choice == '3':
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        print(Fore.RED + "الخروج..." + Style.RESET_ALL)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        print(Fore.RED + "اختيار غير صالح، حاول مرة أخرى!" + Style.RESET_ALL)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if name == "main":
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            user_interface()

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            