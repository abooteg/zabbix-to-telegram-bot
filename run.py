from selenium import webdriver
import telegram
from telegram.ext import Updater, CommandHandler
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from io import BytesIO

# auth on zabbix server
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome("YOUR_CHROME_DRIVER",chrome_options=chrome_options)
driver.get("http://example.zabbix.net/zabbix/")
driver.find_element(By.ID,"name").send_keys("ZABBIX_USERNAME")
driver.find_element(By.ID,"password").send_keys("ZABBIX_PASSWORD")
driver.find_element(By.ID,"enter").click()
driver.set_window_size(1660, 425)
# init Telegram-bot
bot_token = "TELEGRAM_BOT_TOKEN"
bot = telegram.Bot(token=bot_token)

# graphs urls
graph1_url = "http://example.zabbix.net/zabbix/chart2.php?graphid=YOUR_GRAPH_ID&isNow=1&profileIdx=web.graphs.filter&profileIdx2=YOUR_GRAPH_ID&from=now-3h&to=now&height=201&width=1489"
graph2_url = "http://example.zabbix.net/zabbix/chart2.php?graphid=YOUR_GRAPH_ID&isNow=1&profileIdx=web.graphs.filter&profileIdx2=YOUR_GRAPH_ID&from=now-3h&to=now&height=201&width=1489"

# command handlers
def graph1(update, context):
    chat_id = update.effective_chat.id
    driver.get(graph1_url)
    screenshot = driver.get_screenshot_as_png()
    bio = BytesIO(screenshot)
    bot.send_photo(chat_id=chat_id, photo=bio)

def graph2(update, context):
    chat_id = update.effective_chat.id
    driver.get(graph2_url)
    screenshot = driver.get_screenshot_as_png()
    bio = BytesIO(screenshot)
    bot.send_photo(chat_id=chat_id, photo=bio)

# creating a bot object and launching
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# adding command handlers
dispatcher.add_handler(CommandHandler("graph1", graph1))
dispatcher.add_handler(CommandHandler("graph2", graph2))

# launching the bot
updater.start_polling()
updater.idle()

# closing the browser
driver.quit()
