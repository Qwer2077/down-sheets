import requests
from bs4 import BeautifulSoup
import os

username = "gracelessghost"
login = "your email username"
password = "your password"

login_url = "https://sheet.host/account/login"
user_url = f"https://sheet.host/user/{username}/sheets"

success_sheets = []
failed_sheets = []

payload = {
    "login": f"{login}",
    "password": f"{password}"
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
        try:
            well_sheet_0 = well_sheet[0]
        except Exception as e:
            print(f"{i}. Failed on: {href} Error: {e}")
            failed_sheets.append([href, "No sheet music for this", e])
            continue

        all_a = well_sheet_0.find("ul").find_all("a")

        for j, a in enumerate(all_a):
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

            print(f"{i}.{j} Success: {filename} link:{tr_a['href']}")
            success_sheets.append(filename)

print()
print("Failed:")

for i, failed in enumerate(failed_sheets):
    print(f"{i}. Failed on: {failed[0]}\n"
          f"Download Link: {failed[1]}\n"
          f"Error: {failed[2]}")

print()
print(f"Success:")
for i, success in enumerate(success_sheets):
    print(f"{i}. {success}")

print()
print("-" * 20)
print(f"Total Failed: {len(failed_sheets)}")
print(f"Total Success {len(success_sheets)}")
print("-" * 20)
