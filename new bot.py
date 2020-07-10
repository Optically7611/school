import discord
import time
from selenium import webdriver
from fake_useragent import UserAgent
from discord_webhook import DiscordWebhook
from discord_webhook import DiscordEmbed

ua = UserAgent()
a = ua.random
user_agent = ua.random

discord_webhook_url = "https://discordapp.com/api/webhooks/731153419460673536/WU2ug4EOnimiGDxJBk6L1bnnbBLb9-sSfaCusZ4NFSWFairntCdCfGpSSkcbiziTyzGL" # 디스코드 웹훅 url

# 해당하는 교육청 고유 주소 ex) 서울 —> sen
REGION = "sen"

# 학교명 ex) 경희고등학교
SCHOOL_NAME = "신일고등학교"

# 본인 이름
NAME = "김동현"

# 본인 생년월일 ex) 주민등록번호 앞자리
END = "030110"

USER_AGENT = user_agent
print(USER_AGENT)
webhook = DiscordWebhook(url=discord_webhook_url)
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_argument('window-size=1920x1080')

# User agent 설정
options.add_argument(argument=f"user-agent={USER_AGENT}")


app = webdriver.Chrome(executable_path="/Users/zeroday0619/Downloads/chromedriver", options=options)
app.implicitly_wait(10)

# 교육청 코로나 바이러스 감염증 19 자가진단 URL
app.get(url=f"https://eduro.{REGION}.go.kr/hcheck/index.jsp")
studentsInfo = app.find_element_by_xpath(xpath='//*[@id="container"]/div/div/div/div[2]/div/a[2]/div')
studentsInfo.click()

selectSchool = app.find_element_by_xpath('//*[@id="btnSrchSchul"]')

# POPUP 처리
main_window_handle = None
while not main_window_handle:
    main_window_handle = app.current_window_handle

selectSchool.click()

search_school_window_handle = None
while not search_school_window_handle:
    for handle in app.window_handles:
        if handle != main_window_handle:
            search_school_window_handle = handle
            break

# 학교 검색 페이지 전환
app.switch_to.window(search_school_window_handle)

# 학교 검색
s = app.find_element_by_xpath('//*[@id="schulNm"]')
s.send_keys(SCHOOL_NAME)

# 4 second
time.sleep(3)

schoolPush = app.find_element_by_xpath('//*[@id="infoForm"]/div[1]/p/span[3]/button')
schoolPush.click()

schoolPush1 = app.find_element_by_xpath('//*[@id="btnConfirm"]')
schoolPush1.click()

time.sleep(1)

# POPUP 페이지에서 기존 페이지 전환
app.switch_to.window(main_window_handle)

# 이름 입력
writeName = app.find_element_by_xpath('//*[@id="pName"]')
writeName.send_keys(NAME)
time.sleep(3)

# 생년월일 입력
end = app.find_element_by_xpath('//*[@id="frnoRidno"]')
end.send_keys(END)
time.sleep(3)

# 인증 정보 입력 완료
complete = app.find_element_by_xpath('//*[@id="btnConfirm"]')
complete.click()

# =================================================================================================
#                                      | 자가진단 항목 입력 |
# =================================================================================================

select1 = app.find_element_by_xpath('//*[@id="rspns011"]')
select1.click()

select2 = app.find_element_by_xpath('//*[@id="rspns02"]')
select2.click()

select3 = app.find_element_by_xpath('//*[@id="rspns070"]')
select3.click()

select4 = app.find_element_by_xpath('//*[@id="rspns080"]')
select4.click()

select5 = app.find_element_by_xpath('//*[@id="rspns090"]')
select5.click()

time.sleep(3)
select6 = app.find_element_by_xpath('//*[@id="btnConfirm"]')
select6.click()

is_complete = app.get_screenshot_as_file("ok.png")
if is_complete:
    with open("ok.png", "rb") as f:
        webhook.add_file(file=f.read(), filename='self-diagnosis.png')
    embed = DiscordEmbed(title='Auto Self-diagnosis', description='교육부 코로나19 자가진단 자동화 System', color=242424)
    embed.set_image(url="attachment://self-diagnosis.png")
    webhook.add_embed(embed)
    response = webhook.execute()

print("Complete!")
time.sleep(2)
app.close()
