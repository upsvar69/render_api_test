@app.route('/')
def scrape_google():
    print(f"🧩 Selenium version: {selenium.__version__}")

    # Paths for Chrome and Chromedriver on Render.com
    chrome_path = "/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"
    driver_path = "/opt/render/project/.render/chrome/usr/bin/chromedriver"

    print(f"🔍 Checking Chrome binary path: {chrome_path}")
    print(f"🔍 Checking Chromedriver path: {driver_path}")

    if not os.path.exists(chrome_path):
        print("⚠️ Chrome binary not found at expected path.")
        return {"error": "Chrome binary not found."}
    if not os.path.exists(driver_path):
        print("⚠️ Chromedriver not found at expected path.")
        return {"error": "Chromedriver not found."}

    try:
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_path
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        print("🚀 Launching Chrome browser...")
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        query = "Belt and Road Initiative"
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        print(f"🌐 Navigating to: {search_url}")

        driver.get(search_url)
        time.sleep(3)

        print("🔎 Scraping links...")
        results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')
        links = [a.get_attribute('href') for a in results]

        print(f"✅ Found {len(links)} links.")
        for link in links:
            print(link)

        driver.quit()
        return {"links": links}

    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return {"error": str(e)}