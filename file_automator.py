import os
import shutil
from datetime import datetime

class FileAutomator:
    def __init__(self, directory):
        self.directory = directory
        # اطمینان از صحت مسیر
        if not os.path.exists(directory):
            print(f"❌ مسیر '{directory}' یافت نشد.")
            return

    def bulk_rename(self, prefix):
        """تغییر نام تمام فایل‌ها با یک پیشوند و شماره سریال"""
        files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
        for i, filename in enumerate(files):
            extension = os.path.splitext(filename)[1]
            new_name = f"{prefix}_{i+1}{extension}"
            os.rename(os.path.join(self.directory, filename), 
                      os.path.join(self.directory, new_name))
        print(f"✅ تعداد {len(files)} فایل با موفقیت تغییر نام یافتند.")

    def sort_by_date(self):
        """مرتب‌سازی و انتقال فایل‌ها به پوشه‌هایی بر اساس سال و ماه ایجاد"""
        files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
        for filename in files:
            filepath = os.path.join(self.directory, filename)
            # گرفتن زمان آخرین ویرایش
            timestamp = os.path.getmtime(filepath)
            date = datetime.fromtimestamp(timestamp)
            folder_name = date.strftime('%Y-%m') # ساخت پوشه به فرمت '2023-12'
            
            target_path = os.path.join(self.directory, folder_name)
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            
            shutil.move(filepath, os.path.join(target_path, filename))
        print(f"📂 فایل‌ها بر اساس تاریخ در پوشه‌های مجزا مرتب شدند.")

    def filter_by_extension(self, extension):
        """جدا کردن فایل‌های خاص (مثلاً jpg) و انتقال به پوشه‌ای جداگانه"""
        if not extension.startswith('.'):
            extension = '.' + extension
            
        target_folder = os.path.join(self.directory, f"Filtered_{extension[1:]}")
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            
        files = [f for f in os.listdir(self.directory) if f.lower().endswith(extension.lower())]
        for filename in files:
            shutil.move(os.path.join(self.directory, filename), 
                        os.path.join(target_folder, filename))
        print(f"🎯 تعداد {len(files)} فایل با پسوند {extension} جدا شدند.")

# --- نحوه استفاده از اسکریپت ---
if __name__ == "__main__":
    # مسیر پوشه خود را اینجا وارد کنید (مثلاً 'C:/Users/Name/Desktop/MyFolder')
    path = input("لطفاً مسیر پوشه را وارد کنید: ")
    automator = FileAutomator(path)

    print("\n1. تغییر نام دسته‌جمعی\n2. مرتب‌سازی بر اساس تاریخ\n3. جداسازی بر اساس پسوند")
    choice = input("کدام عملیات را انتخاب می‌کنید؟ (1/2/3): ")

    if choice == '1':
        pfx = input("پیشوند نام جدید را وارد کنید: ")
        automator.bulk_rename(pfx)
    elif choice == '2':
        automator.sort_by_date()
    elif choice == '3':
        ext = input("پسوند مورد نظر را وارد کنید (مثل jpg یا pdf): ")
        automator.filter_by_extension(ext)