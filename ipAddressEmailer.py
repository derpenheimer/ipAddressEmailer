
import smtplib, ssl, getpass, sched, time, requests

seconds_per_minute = 60;

def get_start_parameters():
    global host_server, host_port, host_user, host_pwd, addr_to, last_ip_address, update_frequency_seconds, scheduler

    host_server = input("Server: ") #'smtp.gmail.com'
    host_port = input("Port: ") #465
    host_user = input("Username: ") #'your.address.here@gmail.com'
    host_pwd = getpass.getpass("Password: ")
    addr_to  = input("To: ") #'recv.address.here@live.ca'
    update_frequency_seconds  = int(input("Update frequency (minutes): "))*seconds_per_minute #60

    last_ip_address = get_ip_address()
    scheduler = sched.scheduler(time.time, time.sleep)


def schedule_ip_address_check():
    scheduler.enter(update_frequency_seconds, 1, check_if_ip_address_changed)
    scheduler.run()

def check_if_ip_address_changed():
    print("Checking if ip address changed...")
    global last_ip_address
    current_ip_address = get_ip_address()

    if last_ip_address != current_ip_address:
        last_ip_address = current_ip_address  
        notify_by_email()
    
    scheduler.enter(update_frequency_seconds, 1, check_if_ip_address_changed)

def notify_by_email():
    print("Sending ip address by email...")
    
    msg = ("From: %s\r\nTo: %s\r\n\r\nYour computer's ip address changed\r\nYour new ip address is: %s"
        % (host_user, addr_to, last_ip_address))

    with smtplib.SMTP_SSL(host_server, host_port, 20, context=ssl.create_default_context()) as server:
        server.ehlo()
        server.login(host_user, host_pwd)
        server.sendmail(host_user, addr_to, msg)

def prompt(prompt):
    return input(prompt).strip()

def get_ip_address():
    return requests.get('https://api.ipify.org').text

def main():
    get_start_parameters()
    notify_by_email()
    schedule_ip_address_check()
    
if __name__ == "__main__":
    main()
