import requests
from bs4 import BeautifulSoup

# Set up session to maintain cookies
session = requests.Session()

# Step 1: Get the CSRF login token
login_page_url = "https://lms.iiitkottayam.ac.in/login/index.php"
response = session.get(login_page_url)

# Parse login page to extract the token
soup = BeautifulSoup(response.text, "html.parser")
logintoken = soup.find("input", {"name": "logintoken"})["value"]

# Step 2: Send login request with token, username, and password

payload = {"logintoken": logintoken, "username": username, "password": password}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": login_page_url,
}

response = session.post(login_page_url, data=payload, headers=headers)

# Step 3: Check if login was successful
if "Dashboard" in response.text or "My courses" in response.text:
    print("Login successful!")
else:
    print("Login failed. Check credentials or login process.")


dashboard_url = "https://lms.iiitkottayam.ac.in/my/"
dashboard_response = session.get(dashboard_url)
soup = BeautifulSoup(dashboard_response.text, "html.parser")
courses = [names.text for names in soup.find_all(class_="text")]
# print(courses)
courses = courses[5:-1]
# courses[0]=courses[0][1:]
courses=[i.replace(' ','') for i in courses]
courses=[i.replace('.','') for i in courses]
# print(courses)


# for i in range(len(courses)):
#     courses[i]=courses[i].strip()
# courses=courses.trim()
# for i in range(len(courses)):
#     courses[i]=courses[i][:3]+courses[i][4:]
# courses = [item.lstrip(" ") for item in courses]
# courses = [item.lstrip(".") for item in courses]
# print(courses)


att_urls = [
    "https://lms.iiitkottayam.ac.in/mod/attendance/view.php?id=1473&mode=1",
    "https://lms.iiitkottayam.ac.in/mod/attendance/view.php?id=1472&mode=1",
    "https://lms.iiitkottayam.ac.in/mod/attendance/view.php?id=1602&mode=1",
]

final_response = None

for url in att_urls:
    att_response = session.get(url)
    if "IMA121 Calculus and Linear Algebra" in att_response.text:
        final_url = url
        final_response = att_response
        break

if final_response:
    soup = BeautifulSoup(final_response.text, "html.parser")

course_names = [course.text for course in soup.find_all(class_="colcourse cell c0")]
course_percentages = [
    percent.text
    for percent in soup.find_all(
        class_="colpercentagesessionscompleted cell c4 lastcol"
    )
]
zipped = list(zip(course_names, course_percentages))
joined = []
for i in zipped:
    joined.append((i[0] + " " + i[1]))
# print(joined)
# for i in joined:
#     print(i)
# filtered_list = [item for item in joined if 'lab' not in item.lower()]
filtered = [item for item in joined if any(sub in item for sub in courses)]
# filtered_courses = [word for word in joined if any(sub in word for sub in courses)]
# filtered.pop(3)
# for i in currents:
# for i in currents:
#     print(i)

# Filter the courses
# filtered_courses = [course for course in joined if any(sub in course for sub in courses)]

# Print results
#save in a file
# with open("attendance.txt", "w") as f:
#     for course in filtered:
#         f.write(course + "\n")

for course in filtered:
    print(course)
