import logging
import asyncio
from config import load_config
from search_jobs import search_glassdoor, search_indeed, search_google
from filter_jobs import filter_by_location
from apply_to_job import apply_to_job

logging.basicConfig(
    filename="job_applications.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def main():
    config = load_config()
    all_jobs = []
    for search_func in [search_glassdoor, search_indeed, search_google]:
        jobs = await search_func(config["keywords"])
        all_jobs.extend(jobs)
    filtered_jobs = filter_by_location(all_jobs, config["location_preferences"])
    applied_count = 0
    for job in filtered_jobs[:20]:
        success = await apply_to_job(job, config)
        if success:
            logging.info(f"Applied to '{job['title']}' at '{job['company']}'")
            applied_count += 1
        else:
            logging.error(f"Failed to apply to '{job['title']}' at '{job['company']}'")
    print(f"Applied to {applied_count} jobs in this run.")

if __name__ == "__main__":
    asyncio.run(main())