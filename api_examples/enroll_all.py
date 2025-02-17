import requests
from decouple import config


"""
Automated course enrollment script that:
1. Fetches all available courses from the API
2. Enrolls the authenticated user in each course
3. Provides feedback on enrollment status
"""

# Load credentials from environment variables
username = config('TEST_USERNAME', default='')
password = config('TEST_PASSWORD', default='')

# API endpoint configuration
base_url = 'http://127.0.0.1:8000/api/'
url = f'{base_url}courses/'
available_courses = []

# Fetch all courses using pagination
while url is not None:
    print(f'Loading courses from {url}')
    r = requests.get(url)
    response = r.json()
    url = response['next']  # Get next page URL if available
    courses = response['results']
    available_courses += [course['title'] for course in courses]
print(f'Available courses: {", ".join(available_courses)}')

# Enroll in each course
for course in courses:
    course_id = course['id']
    course_title = course['title']
    r = requests.post(
        f'{base_url}courses/{course_id}/enroll/',
        auth=(username, password)  # Basic authentication
    )
    if r.status_code == 200:
        # successful request
        print(f'Successfully enrolled in {course_title}')
