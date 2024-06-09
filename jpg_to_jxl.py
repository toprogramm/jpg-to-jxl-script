import os
import subprocess
import sys
import time

try:
    from colorama import Fore, Style
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import Fore, Style

def check_cjxl_installed():
    try:
        subprocess.run(["cjxl", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print("Warning: cjxl not found. Please install cjxl manually.")
        return False

def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{int(hours)}h:{int(mins)}m:{int(secs)}s"

def apply_cjxl_command(directory_path, quality, replace_files, lossless):
    total_start_time = time.time()  # Start time of the script execution
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.jpg'):
                input_file = os.path.join(root, file)
                if replace_files:
                    output_folder = root
                else:
                    output_folder = os.path.join(root, os.path.basename(root) + '_jxl')
                    os.makedirs(output_folder, exist_ok=True)
                output_file = os.path.join(output_folder, '.'.join(file.split('.')[:-1]) + f'.jxl')
                if lossless:
                    command = f'cjxl "{input_file}" "{output_file}" -v'
                else:
                    command = f'cjxl "{input_file}" "{output_file}" --lossless_jpeg 0 -q {quality} -v'
                
                start_time = time.time()  # Start time of file encoding
                os.system(command)
                end_time = time.time()  # End time of file encoding
                
                input_size = os.path.getsize(input_file)
                output_size = os.path.getsize(output_file)
                
                file_time = end_time - start_time
                print(f"{Fore.RED}Input file: {input_file}, Size: {int(input_size / 1048576)} MB{Style.RESET_ALL}")
                print(f"{Fore.RED}Output file: {output_file}, Size: {int(output_size / 1048576)} MB{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}File encoding time: {file_time:.2f} seconds ({format_time(file_time)}){Style.RESET_ALL}")

                # Удаление оригинального файла
                os.remove(input_file)
                print(f"{Fore.GREEN}Original file {input_file} has been removed.{Style.RESET_ALL}")
    
    total_end_time = time.time()  # End time of the script execution
    total_time = total_end_time - total_start_time
    print(f"{Fore.GREEN}Total script execution time: {total_time:.2f} seconds ({format_time(total_time)}){Style.RESET_ALL}")

if not check_cjxl_installed():
    sys.exit()

directory_path = input("Enter the directory path: ")
lossless = input("Do you want to use lossless compression? (Y/N): ").lower().strip() == 'y'

if lossless:
    quality = None
else:
    quality = input("Enter the quality (0-100): ")

replace_files = input("Do you want to replace files in destination folder? (Y/N): ").lower().strip() == 'y'

apply_cjxl_command(directory_path, quality, replace_files, lossless)


