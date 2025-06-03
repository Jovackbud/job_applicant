def filter_by_location(job_listings, location_preferences):
    filtered = []
    for job in job_listings:
        location = job["location"].lower()
        job_type = job["type"].lower()
        if "abuja" in location:
            if any(t in job_type for t in location_preferences["abuja"]):
                filtered.append(job)
        else:
            if any(t in job_type for t in location_preferences["other"]):
                filtered.append(job)
    return filtered