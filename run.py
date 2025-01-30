import os
import time
import random
import string
import requests
from datetime import datetime  # Sửa lại import datetime
from colorama import init, Fore, Style
import platform
import psutil

# Khởi tạo colorama
init()

# Biến lưu trữ địa chỉ IP và trạng thái setup server
ip_address = "default"
server_setup_completed = False

# URL chứa danh sách key hợp lệ
key_file_url = "https://raw.githubusercontent.com/vtgv42/FreeFire/main/keyokkochtht"

# URLs tải file HTHT
android_file_url = "https://320.gsscdn.com/HTDC_20241113.apk"
ios_file_url = "https://example.com/HTHT_iOS.ipa"

# ==================== HÀM HỖ TRỢ ====================
def clear_screen():
    """Xóa màn hình và đưa người dùng về trạng thái ban đầu."""
    os.system("cls" if os.name == "nt" else "clear")

def exit_program():
    """Hiển thị thông báo thoát và xóa menu chính."""
    clear_screen()  # Xóa toàn bộ màn hình
    print(Fore.GREEN + "Thoát thành công!" + Style.RESET_ALL)
    time.sleep(2)  # Hiển thị thông báo trong 2 giây
    exit(0)  # Kết thúc chương trình


def check_key_and_update_usage(key):
    try:
        response = requests.get(key_file_url)
        response.raise_for_status()
        valid_keys = response.text.splitlines()

        if key in valid_keys:
            key_usage = {}
            try:
                with open("key_usage.txt", "r") as file:
                    for line in file:
                        k, count = line.strip().split(":")
                        key_usage[k] = int(count)
            except FileNotFoundError:
                pass

            if key in key_usage:
                key_usage[key] += 1
            else:
                key_usage[key] = 1

            with open("key_usage.txt", "w") as file:
                for k, count in key_usage.items():
                    file.write(f"{k}:{count}\n")

            return True, key_usage[key]
        else:
            return False, 0

    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi kiểm tra key: {e}")
        return False, 0

# Biến toàn cục
start_time = time.time()  # Lưu thời gian bắt đầu chạy chương trình

def clear_screen():
    """Xóa màn hình."""
    os.system("cls" if os.name == "nt" else "clear")

def format_time(seconds):
    """Định dạng thời gian từ giây sang giờ:phút:giây."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def get_system_info():
    """Lấy thông tin hệ thống."""
    os_name = platform.system()
    os_version = platform.version()
    machine_name = platform.node()
    cpu_percent = psutil.cpu_percent(interval=1)
    ram_info = psutil.virtual_memory()
    ram_percent = ram_info.percent
    total_ram = ram_info.total // (1024 ** 3)  # RAM tổng (GB)

    try:
        battery = psutil.sensors_battery()
        if battery:
            battery_percent = battery.percent
            is_plugged = battery.power_plugged
            charging_status = "Đang sạc" if is_plugged else "Không sạc"
        else:
            battery_percent = "N/A"
            charging_status = "Không có thông tin pin"
    except Exception:
        battery_percent = "N/A"
        charging_status = "Không có thông tin pin"

    return {
        "os_name": os_name,
        "os_version": os_version,
        "machine_name": machine_name,
        "cpu_percent": cpu_percent,
        "ram_percent": ram_percent,
        "total_ram": total_ram,
        "battery_percent": battery_percent,
        "charging_status": charging_status,
    }

def display_system_info():
    """Hiển thị thông tin hệ thống."""
    info = get_system_info()
    program_uptime = time.time() - start_time
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Lấy ngày giờ hiện tại

    print(Fore.CYAN + "===== THÔNG TIN HỆ THỐNG =====" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Ngày giờ hiện tại: {current_datetime}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Hệ điều hành: {info['os_name']} {info['os_version']}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Tên máy: {info['machine_name']}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Sử dụng CPU: {info['cpu_percent']}%" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Sử dụng RAM: {info['ram_percent']}% (Tổng: {info['total_ram']} GB)" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Pin: {info['battery_percent']}%, {info['charging_status']}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Thời gian máy đã chạy: {format_time(program_uptime)}" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 30 + Style.RESET_ALL)

# ==================== CHỨC NĂNG CHÍNH ====================
def setup_server():
    global server_setup_completed
    clear_screen()
    print(Fore.CYAN + "Đang setup server...")
    for i in range(10):  # Thay đổi thành 10 giây cho nhanh
        print(f"Đang chạy... {i + 1} giây", end="\r", flush=True)
        time.sleep(1)
    print("\n" + Fore.CYAN + "Setup server hoàn tất!" + Style.RESET_ALL)
    server_setup_completed = True

server_first_run = True

# Biến toàn cục để theo dõi trạng thái server
server_running = False

# ==================== HÀM DỪNG SERVER ====================
def stop_server():
    global server_running
    if not server_running:
        print(Fore.RED + "Server chưa được chạy! Không thể dừng." + Style.RESET_ALL)
        input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)
        return

    print(Fore.CYAN + "Server đang được tắt..." + Style.RESET_ALL)
    time.sleep(2)
    print(Fore.CYAN + "Server lưu dữ liệu..." + Style.RESET_ALL)
    time.sleep(2)
    print(Fore.GREEN + "Server tắt thành công!" + Style.RESET_ALL)

    server_running = False  # Đánh dấu server đã tắt
    input(Fore.YELLOW + "Nhấn Enter để quay lại menu chính..." + Style.RESET_ALL)

# ==================== CHỨC NĂNG CHẠY SERVER ====================
def run_server():
    global ip_address, server_setup_completed, server_first_run, server_running

    if server_running:  # Kiểm tra xem server đã chạy chưa
        print(Fore.RED + "Server đã được chạy rồi! Bạn cần dừng server trước khi chạy lại." + Style.RESET_ALL)
        input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)
        return

    if not server_setup_completed:
        print(Fore.RED + "Chưa setup server! Vui lòng thực hiện setup trước khi chạy server." + Style.RESET_ALL)
        input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)
        return

    if ip_address != "127.0.0.1":
        print(Fore.RED + "Không thể chạy server! Vui lòng chỉnh sửa IP thành '127.0.0.1' trước." + Style.RESET_ALL)
        input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)
        return

    print(Fore.YELLOW + "Nhập key để chạy server:" + Style.RESET_ALL)
    input_key = input("> ")

    valid, usage_count = check_key_and_update_usage(input_key)

    if valid:
        if server_first_run: 
            # Lần đầu chạy server - hiển thị 5 dòng
            print(Fore.CYAN + "Server đang được khởi tạo..." + Style.RESET_ALL)
            time.sleep(2)
            print(Fore.CYAN + "Server đang trong quá trình bật..." + Style.RESET_ALL)
            time.sleep(2)
            print(Fore.CYAN + "Server đang tạo cơ sở dữ liệu..." + Style.RESET_ALL)
            time.sleep(2)
            print(Fore.GREEN + "Server đã được chạy!" + Style.RESET_ALL)
            time.sleep(2)
            print(Fore.GREEN + "Server đã chạy thành công!" + Style.RESET_ALL)
            server_first_run = False  # Đánh dấu lần đầu đã hoàn tất
        else:
            # Các lần sau chạy server - hiển thị 3 dòng
            print(Fore.CYAN + "Server load dữ liệu..." + Style.RESET_ALL)
            time.sleep(2)
            print(Fore.GREEN + "Server đang chạy..." + Style.RESET_ALL)
            time.sleep(2)
            print(Fore.GREEN + "Server chạy thành công!" + Style.RESET_ALL)

        server_running = True  # Đánh dấu server đã chạy
    else:
        print(Fore.RED + "Key không hợp lệ! Vui lòng thử lại." + Style.RESET_ALL)

    # Sau khi hoàn thành, xóa màn hình
    input(Fore.YELLOW + "Nhấn Enter để quay lại menu chính..." + Style.RESET_ALL)
    clear_screen()


# ==================== MENU CON ====================
def create_account():
    clear_screen()
    print(Fore.MAGENTA + "===== TẠO TÀI KHOẢN =====" + Style.RESET_ALL)
    username = input(Fore.YELLOW + "Nhập tên tài khoản: " + Style.RESET_ALL)
    password = input(Fore.YELLOW + "Nhập mật khẩu: " + Style.RESET_ALL)

    with open("accounts.txt", "a") as file:
        file.write(f"{username}:{password}\n")

    print(Fore.GREEN + "Tạo tài khoản thành công!" + Style.RESET_ALL)
    input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)

def manage_accounts():
    clear_screen()
    print(Fore.MAGENTA + "===== QUẢN LÝ TÀI KHOẢN =====" + Style.RESET_ALL)
    try:
        with open("accounts.txt", "r") as file:
            accounts = file.readlines()

        for i, account in enumerate(accounts, start=1):
            print(f"{i}. {account.strip()}")

        choice = int(input(Fore.YELLOW + "Nhập số thứ tự tài khoản để xóa (0 để thoát): " + Style.RESET_ALL))
        if 0 < choice <= len(accounts):
            del accounts[choice - 1]
            with open("accounts.txt", "w") as file:
                file.writelines(accounts)
            print(Fore.GREEN + "Xóa tài khoản thành công!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Lựa chọn không hợp lệ." + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + "Không tìm thấy danh sách tài khoản!" + Style.RESET_ALL)

    input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)

def edit_ip():
    global ip_address
    clear_screen()
    print(Fore.MAGENTA + "===== CHỈNH SỬA IP =====" + Style.RESET_ALL)
    ip_address = input(Fore.YELLOW + "Nhập địa chỉ IP mới: " + Style.RESET_ALL)
    print(Fore.GREEN + f"Địa chỉ IP đã được đổi thành: {ip_address}" + Style.RESET_ALL)
    input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)

def check_for_updates():
    clear_screen()
    print(Fore.YELLOW + "Đang kiểm tra cập nhật phần mềm..." + Style.RESET_ALL)
    time.sleep(2)
    update_available = random.choice([True, False])
    if update_available:
        print(Fore.GREEN + "Có bản cập nhật mới!" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "Bạn đang sử dụng phiên bản mới nhất." + Style.RESET_ALL)
    input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)

def create_giftcode():
    clear_screen()
    print(Fore.MAGENTA + "===== TẠO GIFTCODE =====" + Style.RESET_ALL)
    length = int(input(Fore.YELLOW + "Nhập độ dài giftcode: " + Style.RESET_ALL))
    giftcode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    print(Fore.GREEN + f"Giftcode đã tạo: {giftcode}" + Style.RESET_ALL)
    with open("giftcodes.txt", "a") as file:
        file.write(giftcode + "\n")
    input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)

def manage_giftcodes():
    clear_screen()
    print(Fore.MAGENTA + "===== QUẢN LÝ GIFTCODE =====" + Style.RESET_ALL)
    try:
        with open("giftcodes.txt", "r") as file:
            giftcodes = file.readlines()

        for i, code in enumerate(giftcodes, start=1):
            print(f"{i}. {code.strip()}")

        choice = int(input(Fore.YELLOW + "Nhập số thứ tự giftcode để xóa (0 để thoát): " + Style.RESET_ALL))
        if 0 < choice <= len(giftcodes):
            del giftcodes[choice - 1]
            with open("giftcodes.txt", "w") as file:
                file.writelines(giftcodes)
            print(Fore.GREEN + "Xóa giftcode thành công!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Lựa chọn không hợp lệ." + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + "Không tìm thấy danh sách giftcode!" + Style.RESET_ALL)

    input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)

def check_key_usage():
    clear_screen()
    print(Fore.MAGENTA + "===== KIỂM TRA SỐ LẦN KEY =====" + Style.RESET_ALL)
    try:
        with open("key_usage.txt", "r") as file:
            for line in file:
                key, count = line.strip().split(":")
                print(f"Key: {key}, Số lần sử dụng: {count}")
    except FileNotFoundError:
        print(Fore.RED + "Không tìm thấy tệp key_usage.txt!" + Style.RESET_ALL)

    input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)

def account_exists(username):
    """Kiểm tra xem tài khoản có tồn tại trong tệp accounts.txt hay không."""
    try:
        with open("accounts.txt", "r") as file:
            accounts = [line.strip().split(":")[0] for line in file.readlines()]
            return username in accounts
    except FileNotFoundError:
        print(Fore.RED + "Không tìm thấy tệp danh sách tài khoản! Vui lòng tạo tài khoản trước." + Style.RESET_ALL)
        return False

def buff_account():
    """Buff account bằng cách thêm vật phẩm và số lượng vào tài khoản."""
    clear_screen()
    print(Fore.MAGENTA + "===== BUFF ACCOUNT =====" + Style.RESET_ALL)
    username = input(Fore.YELLOW + "Nhập tên tài khoản: " + Style.RESET_ALL)

    if not account_exists(username):
        print(Fore.RED + f"Tài khoản '{username}' không tồn tại! Vui lòng tạo tài khoản trước." + Style.RESET_ALL)
        input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)
        return

    item = input(Fore.YELLOW + "Nhập tên vật phẩm để buff: " + Style.RESET_ALL)

    while True:
        try:
            quantity = int(input(Fore.YELLOW + "Nhập số lượng vật phẩm: " + Style.RESET_ALL))
            if quantity <= 0:
                print(Fore.RED + "Số lượng phải lớn hơn 0!" + Style.RESET_ALL)
            else:
                break
        except ValueError:
            print(Fore.RED + "Vui lòng nhập một số nguyên hợp lệ!" + Style.RESET_ALL)

    try:
        with open("buffed_accounts.txt", "a") as file:
            file.write(f"{username}:{item}:{quantity}\n")
        print(Fore.GREEN + f"Đã buff {quantity} '{item}' cho tài khoản '{username}'!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Lỗi khi buff tài khoản: {e}" + Style.RESET_ALL)

    input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)

def buff_admin():
    """Cấp quyền admin cho tài khoản."""
    clear_screen()
    print(Fore.MAGENTA + "===== BUFF ADMIN =====" + Style.RESET_ALL)
    username = input(Fore.YELLOW + "Nhập tên tài khoản để cấp quyền admin: " + Style.RESET_ALL)

    if not account_exists(username):
        print(Fore.RED + f"Tài khoản '{username}' không tồn tại! Vui lòng tạo tài khoản trước." + Style.RESET_ALL)
        input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)
        return

    confirmation = input(Fore.YELLOW + f"Bạn có chắc chắn muốn cấp quyền admin cho tài khoản '{username}'? (y/n): " + Style.RESET_ALL).lower()
    if confirmation == "y":
        try:
            with open("admin_accounts.txt", "a") as file:
                file.write(f"{username}\n")
            print(Fore.GREEN + f"Đã cấp quyền admin cho tài khoản '{username}'!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Lỗi khi cấp quyền admin: {e}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Hủy bỏ cấp quyền admin." + Style.RESET_ALL)

    input(Fore.YELLOW + "Nhấn Enter để quay lại..." + Style.RESET_ALL)

def get_quest_data(username):
    """Lấy trạng thái nhiệm vụ của tài khoản."""
    try:
        with open("quests.txt", "r") as file:
            for line in file:
                data = line.strip().split(":")
                if data[0] == username:
                    return {"username": data[0], "current_task": int(data[1]), "total_tasks": int(data[2])}
        return None
    except FileNotFoundError:
        return None

def update_quest_data(username, current_task, total_tasks):
    """Cập nhật trạng thái nhiệm vụ."""
    found = False
    lines = []
    try:
        with open("quests.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        pass

    with open("quests.txt", "w") as file:
        for line in lines:
            data = line.strip().split(":")
            if data[0] == username:
                file.write(f"{username}:{current_task}:{total_tasks}\n")
                found = True
            else:
                file.write(line)
        if not found:
            file.write(f"{username}:{current_task}:{total_tasks}\n")

def buff_task():
    """Menu buff nhiệm vụ."""
    # **Step 1:** Check if quests.txt exists
    if not os.path.exists("quests.txt"):
        with open("quests.txt", "w") as file:
            pass # Create an empty file

    # **Step 2:** Iterate over each account and add it to quests.txt
    with open("accounts.txt", "r") as accounts_file:
        for line in accounts_file:
            username = line.strip().split(":")[0]
            # **Step 3:** Set current_task and total_tasks
            current_task = 0
            total_tasks = 10
            with open("quests.txt", "a") as quests_file:
                quests_file.write(f"{username}:{current_task}:{total_tasks}\n")

    while True:
        clear_screen()
        print(Fore.CYAN + "===== BUFF NHIỆM VỤ =====" + Style.RESET_ALL)
        print("1. Buff qua nhiệm vụ hiện tại")
        print("2. Buff qua full nhiệm vụ")
        print("3. Reset nhiệm vụ về từ đầu")
        print("0. Quay lại menu chính")
        choice = input("Nhập lựa chọn: ")

        if choice == "0":
            break

        username = input(Fore.YELLOW + "Nhập tên tài khoản: " + Style.RESET_ALL)
        quest_data = get_quest_data(username)

        if not quest_data:
            print(Fore.RED + "Tài khoản không tồn tại hoặc chưa có nhiệm vụ!" + Style.RESET_ALL)
            input(Fore.YELLOW + "Nhấn Enter để tiếp tục..." + Style.RESET_ALL)
            continue

        if choice == "1":  # Buff qua nhiệm vụ hiện tại
            if quest_data["current_task"] < quest_data["total_tasks"]:
                quest_data["current_task"] += 1
                update_quest_data(username, quest_data["current_task"], quest_data["total_tasks"])
                print(Fore.GREEN + f"Đã buff qua nhiệm vụ hiện tại cho '{username}'. Nhiệm vụ hiện tại: {quest_data['current_task']}" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Tài khoản đã hoàn thành toàn bộ nhiệm vụ!" + Style.RESET_ALL)

        elif choice == "2":  # Buff qua toàn bộ nhiệm vụ
            update_quest_data(username, quest_data["total_tasks"], quest_data["total_tasks"])
            print(Fore.GREEN + f"Đã buff qua toàn bộ nhiệm vụ cho '{username}'." + Style.RESET_ALL)

        elif choice == "3":  # Reset nhiệm vụ về từ đầu
            update_quest_data(username, 0, quest_data["total_tasks"])
            print(Fore.GREEN + f"Nhiệm vụ của tài khoản '{username}' đã được reset." + Style.RESET_ALL)

        else:
            print(Fore.RED + "Lựa chọn không hợp lệ!" + Style.RESET_ALL)

        input(Fore.YELLOW + "Nhấn Enter để tiếp tục..." + Style.RESET_ALL)


def create_event():
    """Tạo sự kiện mới."""
    while True:
        clear_screen()
        print(Fore.CYAN + "===== TẠO SỰ KIỆN =====" + Style.RESET_ALL)
        event_name = input(Fore.YELLOW + "Nhập tên sự kiện: " + Style.RESET_ALL).strip()
        description = input(Fore.YELLOW + "Nhập nội dung sự kiện: " + Style.RESET_ALL).strip()

        # Nhập và kiểm tra ngày giờ hết hạn
        while True:
            expiry_date = input(Fore.YELLOW + "Nhập ngày giờ hết hạn (YYYY-MM-DD HH:MM): " + Style.RESET_ALL).strip()
            try:
                expiry_datetime = datetime.strptime(expiry_date, "%Y-%m-%d %H:%M")
                break
            except ValueError:
                print(Fore.RED + "Định dạng ngày giờ không hợp lệ! Vui lòng nhập lại." + Style.RESET_ALL)

        confirm = input(Fore.RED + "Bạn có chắc chắn muốn tạo sự kiện này? (y/n): " + Style.RESET_ALL).lower()
        if confirm == "y":
            with open("events.txt", "a") as file:
                file.write(f"{event_name}|{description}|{expiry_date}|active\n")
            print(Fore.GREEN + f"Sự kiện '{event_name}' đã được tạo thành công!" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Đã hủy tạo sự kiện." + Style.RESET_ALL)

        cont = input(Fore.YELLOW + "Nhấn Enter để tiếp tục hoặc gõ 'q' để quay lại: " + Style.RESET_ALL)
        if cont.lower() == "q":
            break

def manage_events():
    """Quản lý sự kiện (xóa hoặc mở lại sự kiện)."""
    while True:
        clear_screen()
        print(Fore.CYAN + "===== QUẢN LÝ SỰ KIỆN =====" + Style.RESET_ALL)

        try:
            with open("events.txt", "r") as file:
                events = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            events = []

        if not events:
            print(Fore.RED + "Không có sự kiện nào được tạo!" + Style.RESET_ALL)
            input(Fore.YELLOW + "Nhấn Enter để quay lại: " + Style.RESET_ALL)
            break

        # Hiển thị danh sách sự kiện
        print(Fore.YELLOW + "Danh sách sự kiện:" + Style.RESET_ALL)
        for idx, event in enumerate(events):
            name, description, expiry, status = event.split("|")
            print(f"{idx + 1}. {name} - {status} - Hết hạn: {expiry}")

        choice = input(Fore.YELLOW + "Nhập số thứ tự sự kiện để quản lý (hoặc 'q' để quay lại): " + Style.RESET_ALL).strip()
        if choice.lower() == "q":
            break

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(events):
            print(Fore.RED + "Lựa chọn không hợp lệ!" + Style.RESET_ALL)
            time.sleep(1)
            continue

        event_index = int(choice) - 1
        name, description, expiry, status = events[event_index].split("|")

        print(Fore.YELLOW + f"Bạn đang quản lý sự kiện: {name}" + Style.RESET_ALL)
        print("1. Xóa sự kiện")
        print("2. Mở lại sự kiện (nếu đã tắt)")
        print("0. Quay lại")

        action = input(Fore.YELLOW + "Chọn hành động: " + Style.RESET_ALL).strip()
        if action == "1":
            confirm = input(Fore.RED + f"Bạn có chắc chắn muốn xóa sự kiện '{name}'? (y/n): " + Style.RESET_ALL).lower()
            if confirm == "y":
                events.pop(event_index)
                print(Fore.GREEN + f"Đã xóa sự kiện '{name}'!" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "Đã hủy xóa sự kiện." + Style.RESET_ALL)

        elif action == "2":
            if status == "active":
                print(Fore.RED + "Sự kiện đã đang hoạt động!" + Style.RESET_ALL)
            else:
                events[event_index] = f"{name}|{description}|{expiry}|active"
                print(Fore.GREEN + f"Đã mở lại sự kiện '{name}'!" + Style.RESET_ALL)

        elif action == "0":
            continue

        else:
            print(Fore.RED + "Lựa chọn không hợp lệ!" + Style.RESET_ALL)

        # Cập nhật file
        with open("events.txt", "w") as file:
            file.write("\n".join(events) + "\n")

        input(Fore.YELLOW + "Nhấn Enter để tiếp tục..." + Style.RESET_ALL)


def buff_menu():
    """Menu Buff."""
    while True:
        clear_screen()
        print(Fore.CYAN + "===== MENU BUFF =====" + Style.RESET_ALL)
        print("1. Buff Item")
        print("2. Buff Admin")
        print("3. Buff Nhiệm Vụ")
        print("0. Quay lại menu chính")
        choice = input("Nhập lựa chọn: ")

        if choice == "1":
            buff_account()
        elif choice == "2":
            buff_admin()
        elif choice == "3":
            buff_task()
        elif choice == "0":
            break
        else:
            print(Fore.RED + "Lựa chọn không hợp lệ!" + Style.RESET_ALL)
            time.sleep(1)


# ==================== MENU ====================
def menu_con():
    while True:
        clear_screen()
        print(Fore.CYAN + "===== MENU CHỨC NĂNG =====" + Style.RESET_ALL)
        print("1. Tạo tài khoản")
        print("2. Quản lý tài khoản")
        print("3. Chỉnh sửa IP")
        print("4. Kiểm tra cập nhật phần mềm")
        print("5. Tạo giftcode")
        print("6. Quản lý giftcode")
        print("7. Tạo Sự Kiện")
        print("8. Quản Lý Sự Kiện")
        print("9. Check số lần key")
        print("0. Quay lại menu chính")
        choice = input("Nhập lựa chọn: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            manage_accounts()
        elif choice == "3":
            edit_ip()
        elif choice == "4":
            check_for_updates()
        elif choice == "5":
            create_giftcode()
        elif choice == "6":
            manage_giftcodes()
        elif choice == "7":
            create_event()
        elif choice == "8":
            mange_event()
        elif choice == "9":
            check_key_usage()
        elif choice == "0":
            break
        else:
            print(Fore.RED + "Lựa chọn không hợp lệ!" + Style.RESET_ALL)
            time.sleep(1)

def main_menu():
    while True:
        clear_screen()

        display_system_info()

        print(Fore.CYAN + "===== MENU CHÍNH =====" + Style.RESET_ALL)
        print("1. Setup server")
        print("2. Chạy server")
        print("3. Stop Server")
        print("4. Chức năng khác")
        print("5. Buff Menu")
        print("6. Tải File HTHT")
        print("0. Thoát")
        choice = input("Nhập lựa chọn: ")

        if choice == "1":
            setup_server()
        elif choice == "2":
            run_server()
        elif choice == "3":
            stop_server()
        elif choice == "4":
            menu_con()
        elif choice == "5":
            buff_menu()
        elif choice == "6":
            download_file()
        elif choice == "0":
            exit_program()
            break
        else:
            print(Fore.RED + "Lựa chọn không hợp lệ!" + Style.RESET_ALL)
            time.sleep(1)

if __name__ == "__main__":
    main_menu()