from browser_use import Browser


async def search_glassdoor(keywords):
    browser = Browser(browser="chrome", headless=True)
    jobs = []
    await browser.start()
    try:
        for keyword in keywords:
            await browser.navigate("https://www.glassdoor.com/Job/index.htm")
            search_box = await browser.find_element("input[id='searchBar-jobTitle']")
            await search_box.fill(keyword)
            submit_button = await browser.find_element("button[type='submit']")
            await submit_button.click()
            await browser.wait_for_element(".job-search-results")
            job_elements = await browser.find_elements(".job-card")
            for job in job_elements:
                jobs.append({
                    "title": (await job.find_element(".job-title")).text,
                    "company": (await job.find_element(".company-name")).text,
                    "location": (await job.find_element(".location")).text,
                    "type": (await job.find_element(".job-type")).text.lower(),
                    "link": (await job.find_element("a")).get_attribute("href")
                })
    finally:
        await browser.stop()
    return jobs

async def search_indeed(keywords):
    browser = Browser(browser="chrome", headless=True)
    jobs = []
    await browser.start()
    try:
        for keyword in keywords:
            await browser.navigate("https://www.indeed.com")
            search_box = await browser.find_element("input[id='text-input-what']")
            await search_box.fill(keyword)
            submit_button = await browser.find_element("button[type='submit']")
            await submit_button.click()
            await browser.wait_for_element(".jobsearch-ResultsList")
            job_elements = await browser.find_elements(".jobseen")
            for job in job_elements:
                jobs.append({
                    "title": (await job.find_element(".jobTitle")).text,
                    "company": (await job.find_element(".companyName")).text,
                    "location": (await job.find_element(".companyLocation")).text,
                    "type": (await job.find_element(".attribute_snippet")).text.lower(),
                    "link": (await job.find_element("a")).get_attribute("href")
                })
    finally:
        await browser.stop()
    return jobs

async def search_google(keywords):
    browser = Browser(browser="chrome", headless=True)
    jobs = []
    await browser.start()
    try:
        for keyword in keywords:
            await browser.navigate("https://www.google.com")
            search_box = await browser.find_element("input[name='q']")
            await search_box.fill(f"{keyword} jobs")
            submit_button = await browser.find_element("button[type='submit']")
            await submit_button.click()
            await browser.wait_for_element(".g")
            job_elements = await browser.find_elements(".tF2Cxc")
            for job in job_elements:
                jobs.append({
                    "title": (await job.find_element("h3")).text,
                    "company": (await job.find_element(".Vpfmgd")).text,
                    "location": (await job.find_element(".r0tvf")).text,
                    "type": "remote" if "remote" in (await job.text).lower() else "onsite",
                    "link": (await job.find_element("a")).get_attribute("href")
                })
    finally:
        await browser.stop()
    return jobs