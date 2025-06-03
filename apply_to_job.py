import PyPDF2
from langchain_gemini import ChatGemini
from browser_use import Browser
import asyncio

def parse_resume(resume_path):
    with open(resume_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

async def generate_cover_letter(job_description, resume_text):
    llm = ChatGemini(model="gemini-pro")
    prompt = (
        f"Generate a professional cover letter for a job based on the following job description and my resume.\n"
        f"Job Description: {job_description}\n"
        f"My Resume: {resume_text}\n"
        f"Highlight relevant skills and experiences from my resume that match the job requirements."
        f"Write with my style: concise, direct sentences; full-word forms (no contractions); "
        f"minimal filler or ornament; polite but businesslike tone. Swap any casual turns of phrase for precise, "
        f"formal vocabulary; and always use complete, well-punctuated sentences"
    )
    return await llm.generate(prompt)

async def fill_form(browser, personal_info):
    form_fields = await browser.find_elements("input, textarea, select")
    for field in form_fields:
        try:
            label = (await field.find_element("label")).text.lower() if await field.find_element("label") else ""
            if "name" in label:
                await field.fill(personal_info["name"])
            elif "email" in label:
                await field.fill(personal_info["email"])
            elif "resume" in label and field.get_attribute("type") == "file":
                await field.upload_file(personal_info["resume_path"])
            elif "phone" in label and personal_info["phone"]:
                await field.fill(personal_info["phone"])
            elif "portfolio" in label and personal_info["portfolio"]:
                await field.fill(personal_info["portfolio"])
            elif "cover letter" in label:
                pass  # Handled separately
        except:
            continue

async def submit_application(browser):
    await browser.find_element("button[type='submit']").click()
    await browser.wait_for_element(".confirmation-message", timeout=10)

async def apply_to_job(job, config):
    browser = Browser(browser="chrome", headless=True)
    await browser.start()
    try:
        await browser.navigate(job["link"])
        job_description = (await browser.find_element(".job-description")).text
        resume_text = parse_resume(config["personal_info"]["resume_path"])
        cover_letter = await generate_cover_letter(job_description, resume_text)
        await fill_form(browser, config["personal_info"])
        cover_letter_field = await browser.find_element("textarea[id*='cover']")
        if cover_letter_field:
            await cover_letter_field.fill(cover_letter)
        await submit_application(browser)
        return True
    except Exception as e:
        print(f"Chrome failed for {job['title']}: {e}")
        browser = Browser(browser="edge", headless=True)
        await browser.start()
        try:
            await browser.navigate(job["link"])
            await fill_form(browser, config["personal_info"])
            cover_letter_field = await browser.find_element("textarea[id*='cover']")
            if cover_letter_field:
                await cover_letter_field.fill(cover_letter)
            await submit_application(browser)
            return True
        except Exception as e:
            print(f"Edge failed for {job['title']}: {e}")
            return False
        finally:
            await browser.stop()
    finally:
        await browser.stop()