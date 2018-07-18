HEADERS    = {
    'User-Agent': 'Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36', 
    'Origin': 'https://www.udemy.com', 
    'Referer': 'https://www.udemy.com',
    "Accept": "application/json, text/plain, */*",
}

BASE_URL   = 'https://www.udemy.com{0}'
LOGIN_URL  = BASE_URL.format('/join/login-popup/')
BASE_API   = BASE_URL.format('/api-2.0{0}')

MY_COURSES_EXPIRY = (60*30)   #30 Minutes
COURSE_EXPIRY     = (60*60*24) #24 Hours
