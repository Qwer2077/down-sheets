import requests
from bs4 import BeautifulSoup
import os

login_url = "https://sheet.host/account/login"
user_url = "https://sheet.host/user/colsene/sheets"

username = user_url[24:-7]
success_sheets = []
failed_sheets = []

payload = {
    "login": "your-username",
    "password": "your-password"
}

if not os.path.exists(username):
    os.makedirs(username)

os.chdir(username)

with requests.session() as s:
    s.post(login_url, payload)
    r = s.get(user_url)

    soup = BeautifulSoup(r.content, "html.parser")
    all_tr_a = soup.select('table[class="sh-table-score"] tbody tr td div a')

    print(f"Total Sheets: {len(all_tr_a)}")

    for i, tr_a in enumerate(all_tr_a):
        href = tr_a["href"]

        r = s.get(href)

        soup = BeautifulSoup(r.content, "html.parser")
        well_sheet = soup.find_all(class_="well sheet-download")
        well_sheet_0 = well_sheet[0]
        all_a = well_sheet_0.find("ul").find_all("a")

        for j, a in enumerate(all_a):
            print()
            href = a["href"]
            r = requests.get(href)

            try:
                filename = r.headers["Content-Disposition"][22:-1]
            except Exception as e:
                print(f"{i}.{j} Failed on: {tr_a['href']}\n"
                      f"Download Link: {href}\n"
                      f"Error: {e}")
                failed_sheets.append([tr_a["href"], href, e])
                continue

            with open(f"{filename}", "wb") as f:
                f.write(r.content)

            print(f"{i}.{j} Success: filename")
            success_sheets.append(filename)

print()
print("-" * 20)
print(f"Total Failed: {len(failed_sheets)}")
print(f"Total Success {len(success_sheets)}")
for i, failed in enumerate(failed_sheets):
    print()
    print(f"{i}. Failed on: {failed[0]}\n"
          f"Download Link: {failed[1]}\n"
          f"Error: {failed[2]}")

print()
print(f"Success")
print()
for i, success in enumerate(success_sheets):
    print(f"{i}. {success}")
