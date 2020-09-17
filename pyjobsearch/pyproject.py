from app import application
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
import json
from listing import Listing


jobs = []


def listing_filter(title):
    job_reqs = ["Web", "Developer", "Engineer", "Designer", "Software", "Quality", "Programmer", "Data"]
    for req in job_reqs:
        if req not in title or "Senior" in title or "Manager" in title or "Sr" in title:
            continue
        elif req not in title and "Senior" in title or "Manager" in title or "Sr" in title:
            continue
        else:
            return True
    return False


''''''
''''''
# LINKEDIN FUNCTION
linkedin_url_web = "https://www.linkedin.com/jobs/search/?f_E=2&f_T=100%2C25167%2C25170%2C25194&f_TP=1&f_TPR=r86400&keywords=entry%20level%20web%20developer&location=United%20States"
linkedin_url_software = "https://www.linkedin.com/jobs/search/?f_E=2&f_T=9%2C24%2C509%2C1180%2C1397%2C3549&f_TP=1&f_TPR=r86400&keywords=entry%20level%20software%20developer&location=United%20States"


def linkedin_jobs(url):
    req = requests.get(url, headers={"User-agent": "job_bot 1.0"})
    soup = BeautifulSoup(req.content, "html.parser")
    tags = soup.html.body.findAll("div", class_="result-card__contents job-result-card__contents")
    # print(len(tags))
    for tag in tags:
        listing = Listing()
        listing.title = tag.h3.text[:35] + "..." if len(tag.h3.text) > 40 else tag.h3.text
        listing.company = tag.h4.a.text
        listing.location = tag.div.span.text
        listing.date = tag.time.text
        listing.link = tag.h4.a.get("href")
        listing.logo = "https://cdn4.iconfinder.com/data/icons/flat-icon-social-media/256/Linkedin.png"
        jobs.append(listing.to_dict())


linkedin_jobs(linkedin_url_web)
linkedin_jobs(linkedin_url_software)
''''''
''''''
# GLASSDOOR
glassdoor_url_web = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=entry%20level%20web%20developer&locT=&locId=0&locKeyword=&jobType=all&fromAge=1&minSalary=0&includeNoSalaryJobs=true&radius=25&cityId=-1&minRating=0.0&industryId=-1&gocId=-1&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0"
glassdoor_web_interns = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=web%20developer%20internship&locT=&locId=0&locKeyword=&jobType=all&fromAge=1&minSalary=0&includeNoSalaryJobs=true&radius=25&cityId=-1&minRating=0.0&industryId=-1&gocId=-1&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0"
glassdoor_url_software_d = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=Entry%20Level%20Software%20developer&locT=&locId=0&locKeyword=&jobType=all&fromAge=1&minSalary=0&includeNoSalaryJobs=true&radius=25&cityId=-1&minRating=0.0&industryId=-1&gocId=-1&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0"
glassdoor_url_software_e = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=Entry%20Level%20Software%20engineer&locT=&locId=0&locKeyword=&jobType=all&fromAge=1&minSalary=0&includeNoSalaryJobs=true&radius=25&cityId=-1&minRating=0.0&industryId=-1&gocId=-1&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0"
glassdoor_software_interns = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=software%20developer%20internship&locT=&locId=0&locKeyword=&jobType=all&fromAge=1&minSalary=0&includeNoSalaryJobs=true&radius=25&cityId=-1&minRating=0.0&industryId=-1&gocId=-1&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0"


def glassdoor_jobs(url):
    req = requests.get(url, headers={"User-agent": "job_bot 1.0"})
    soup = BeautifulSoup(req.content, "html.parser")
    tags = soup.findAll("li", class_="jl react-job-listing gdGrid")
    print(len(tags))
    for tag in tags:
        listing = Listing()
        title = tag.find("a", class_="jobInfoItem jobTitle css-13w0lq6 eigr9kq1 jobLink").span.text
        listing.title = title[:35] + "..." if len(title) > 40 else title
        listing.company = tag.find("div", class_="jobHeader d-flex justify-content-between align-items-start").a.span.text
        salary = tag.find("div", class_="salaryEstimate ")
        listing.salary = salary.span.span.text if salary is not None else "Not Listed"
        location = tag.find("div", class_="d-flex flex-wrap css-yytu5e e1rrn5ka1")
        listing.location = location.span.text if location is not None else "US"
        listing.date = "24hr"
        listing.link = "https://www.glassdoor.com" + tag.find("a", class_="jobLink").get("href")
        listing.logo = "https://www.adweek.com/agencyspy/wp-content/uploads/sites/7/2016/01/glassdoor.jpg"
        exists = False
        for job in jobs:
            if listing == job:
                exists = True
                break
        if not exists:
            jobs.append(listing.to_dict())


glassdoor_jobs(glassdoor_url_web)
glassdoor_jobs(glassdoor_web_interns)
glassdoor_jobs(glassdoor_url_software_d)
glassdoor_jobs(glassdoor_url_software_e) # similar to developer jobs
glassdoor_jobs(glassdoor_software_interns)
''''''
''''''
# MONSTER FUNCTION(web/software)
monster_url_web = "https://www.monster.com/jobs/search/?q=entry-level-web-developer&tm=1"
monster_web_interns = "https://www.monster.com/jobs/search/?q=web-developer-internship&intcid=skr_navigation_nhpso_searchMain&tm=1"
monster_url_software_e = "https://www.monster.com/jobs/search/?q=entry-level-software-engineer&tm=1"
monster_url_software_d = "https://www.monster.com/jobs/search/?q=entry-level-software-developer&tm=1"
monster_software_interns = "https://www.monster.com/jobs/search/?q=software-developer-internship&tm=1"


def monster_jobs(url):
    req = requests.get(url, headers={"User-agent": "job_bot 1.0"})
    soup = BeautifulSoup(req.content, "html.parser")
    tags = soup.findAll("div", class_="flex-row")
    for tag in tags:
        title = tag.find("h2", class_="title").a.text[:-2]
        if listing_filter(title):
            listing = Listing()
            listing.title = title[:35] + "..." if len(title) > 40 else title
            listing.company = tag.find("div", class_="company").span.text
            listing.location = tag.find("div", class_="location").span.text[2:-2]
            listing.date = tag.find("div", class_="meta flex-col").time.get("datetime")[:-6]
            listing.link = tag.find("h2", class_="title").a.get("href")
            listing.logo = "https://games.lol/wp-content/uploads/2018/10/monster-search-best-pc-download-online.png"
            exists = False
            for job in jobs:
                if listing == job:
                    exists = True
                    break
            if not exists:
                jobs.append(listing.to_dict())


monster_jobs(monster_url_web)
monster_jobs(monster_web_interns)
monster_jobs(monster_url_software_e)
monster_jobs(monster_url_software_d)
monster_jobs(monster_software_interns)
''''''
''''''
# INDEED FUNCTION(web/software)
indeed_url_web = "https://www.indeed.com/jobs?as_and=web+developer+entry+level&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=&fromage=1&limit=50&sort=&psf=advsrch"
indeed_web_interns = "https://www.indeed.com/jobs?as_and=web+developer+internship&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=&fromage=1&limit=50&sort=&psf=advsrch"
indeed_url_software_e = "https://www.indeed.com/jobs?as_and=entry+level+software+engineer&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=&fromage=1&limit=50&sort=&psf=advsrch"
indeed_url_software_d = "https://www.indeed.com/jobs?as_and=entry+level+software+developer&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=&fromage=1&limit=10&sort=&psf=advsrch"
indeed_software_interns = "https://www.indeed.com/jobs?as_and=software+developer+internship&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=25&l=&fromage=1&limit=50&sort=&psf=advsrch"


def indeed_jobs(url):
    req = requests.get(url, headers={"User-agent": "job_bot 1.0"})
    soup = BeautifulSoup(req.content, "html.parser")
    tags = soup.findAll("div", class_="jobsearch-SerpJobCard")
    for tag in tags:
        title = tag.find("h2", class_="title").a.get("title").strip()
        if listing_filter(title):
            listing = Listing()
            listing.title = title[:35] + "..." if len(title) > 40 else title # 75 and 80
            listing.company = tag.find("div", class_="sjcl").div.span.text.lstrip()
            salary = tag.find("span", class_="salaryText")
            listing.salary = salary.text.lstrip() if salary is not None else "Not Listed"
            listing.location = tag.find("div", class_="recJobLoc")["data-rc-loc"] # same as .get("data-rc-loc")
            listing.date = (date.today() - timedelta(days=1)).strftime('%y-%m-%d')
            listing.link = f"https://www.google.com/search?q={title}+{listing.company}+{listing.location}+{listing.date}+job+opening"
            listing.logo = "https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/ab/03/b8/ab03b82b-12cf-ce7c-249f-b54a8f01c1b9/AppIcon-1x_U007emarketing-85-220-0-6.png/246x0w.jpg"
            exists = False
            for job in jobs:
                if listing == job:
                    exists = True
                    break
            if not exists:
                jobs.append(listing.to_dict())


indeed_jobs(indeed_url_web)
indeed_jobs(indeed_url_software_e)
indeed_jobs(indeed_url_software_d)
indeed_jobs(indeed_web_interns)
indeed_jobs(indeed_software_interns)
''''''
'''
# CRAIGSLIST FUNCTION (web/software)
# craigslist_url_web_sb(not today) = "https://santabarbara.craigslist.org/search/web?sort=date&nearbyArea=63&nearbyArea=43&nearbyArea=709&nearbyArea=455&nearbyArea=104&nearbyArea=26&nearbyArea=7&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=103&nearbyArea=209&nearbyArea=12&nearbyArea=8&nearbyArea=191&nearbyArea=710&nearbyArea=1&nearbyArea=97&nearbyArea=208&nearbyArea=346&searchNearby=2"
craigslist_url_web_sb = "https://santabarbara.craigslist.org/search/web?sort=date&postedToday=1&nearbyArea=63&nearbyArea=43&nearbyArea=709&nearbyArea=455&nearbyArea=104&nearbyArea=26&nearbyArea=7&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=103&nearbyArea=209&nearbyArea=12&nearbyArea=8&nearbyArea=191&nearbyArea=710&nearbyArea=1&nearbyArea=97&nearbyArea=208&nearbyArea=346&searchNearby=2"
craigslist_url_web_tx = "https://austin.craigslist.org/search/web?postedToday=1&searchNearby=2&nearbyArea=364&nearbyArea=264&nearbyArea=266&nearbyArea=326&nearbyArea=265&nearbyArea=21&nearbyArea=645&nearbyArea=647&nearbyArea=470&nearbyArea=23&nearbyArea=327&nearbyArea=284&nearbyArea=271&nearbyArea=422&nearbyArea=263&nearbyArea=268&nearbyArea=646&nearbyArea=53&nearbyArea=449&nearbyArea=206&nearbyArea=359&nearbyArea=649&nearbyArea=308&nearbyArea=564&nearbyArea=270&nearbyArea=365"
craigslist_url_web_fl = "https://miami.craigslist.org/search/web?postedToday=1&searchNearby=1"
craigslist_url_web_wa = "https://seattle.craigslist.org/search/web?postedToday=1&searchNearby=2&nearbyArea=217&nearbyArea=466&nearbyArea=9&nearbyArea=461&nearbyArea=325&nearbyArea=246"
craigslist_url_web_ut = "https://saltlakecity.craigslist.org/search/web?postedToday=1&searchNearby=2&nearbyArea=52&nearbyArea=424&nearbyArea=652&nearbyArea=288&nearbyArea=448&nearbyArea=351&nearbyArea=292&nearbyArea=352&nearbyArea=469&nearbyArea=320&nearbyArea=197"
craigslist_url_web_wi = "https://milwaukee.craigslist.org/search/web?postedToday=1&searchNearby=1"
craigslist_url_web_or = "https://portland.craigslist.org/search/web?postedToday=1&searchNearby=2&nearbyArea=233&nearbyArea=350&nearbyArea=94&nearbyArea=232&nearbyArea=2&nearbyArea=246"
craigslist_url_web_az = "https://phoenix.craigslist.org/search/web?postedToday=1&searchNearby=1"
craigslist_url_web_co = "https://denver.craigslist.org/search/web?postedToday=1&searchNearby=2&nearbyArea=319&nearbyArea=210&nearbyArea=713&nearbyArea=287&nearbyArea=288&nearbyArea=315"
# craigslist_url_software_sb(not today) = "https://santabarbara.craigslist.org/search/sof?sort=date&nearbyArea=63&nearbyArea=43&nearbyArea=709&nearbyArea=455&nearbyArea=104&nearbyArea=26&nearbyArea=7&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=103&nearbyArea=209&nearbyArea=12&nearbyArea=8&nearbyArea=191&nearbyArea=710&nearbyArea=1&nearbyArea=97&nearbyArea=208&nearbyArea=346&searchNearby=2"
craigslist_url_software_sb = "https://santabarbara.craigslist.org/search/sof?sort=date&postedToday=1&searchNearby=2&nearbyArea=63&nearbyArea=43&nearbyArea=709&nearbyArea=455&nearbyArea=104&nearbyArea=26&nearbyArea=7&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=103&nearbyArea=209&nearbyArea=12&nearbyArea=8&nearbyArea=191&nearbyArea=710&nearbyArea=1&nearbyArea=97&nearbyArea=208&nearbyArea=346"
craigslist_url_software_tx = "https://austin.craigslist.org/search/sof?postedToday=1&searchNearby=2&nearbyArea=364&nearbyArea=264&nearbyArea=266&nearbyArea=326&nearbyArea=265&nearbyArea=21&nearbyArea=645&nearbyArea=647&nearbyArea=470&nearbyArea=23&nearbyArea=327&nearbyArea=284&nearbyArea=271&nearbyArea=422&nearbyArea=263&nearbyArea=268&nearbyArea=646&nearbyArea=53&nearbyArea=449&nearbyArea=206&nearbyArea=359&nearbyArea=649&nearbyArea=308&nearbyArea=564&nearbyArea=270&nearbyArea=365"
craigslist_url_software_fl = "https://miami.craigslist.org/search/sof?postedToday=1&searchNearby=1"
craigslist_url_software_wa = "https://seattle.craigslist.org/search/sof?postedToday=1&nearbyArea=217&nearbyArea=466&nearbyArea=9&nearbyArea=461&nearbyArea=325&nearbyArea=246&searchNearby=2"
craigslist_url_software_ut = "https://saltlakecity.craigslist.org/search/sof?postedToday=1&nearbyArea=52&nearbyArea=424&nearbyArea=652&nearbyArea=288&nearbyArea=448&nearbyArea=351&nearbyArea=292&nearbyArea=352&nearbyArea=469&nearbyArea=320&nearbyArea=197&searchNearby=2"
craigslist_url_software_wi = "https://milwaukee.craigslist.org/search/sof?postedToday=1&searchNearby=1"
craigslist_url_software_or = "https://portland.craigslist.org/search/sof?postedToday=1&nearbyArea=233&nearbyArea=350&nearbyArea=94&nearbyArea=232&nearbyArea=2&nearbyArea=246&searchNearby=2"
craigslist_url_software_az = "https://phoenix.craigslist.org/search/sof?postedToday=1&searchNearby=1"
craigslist_url_software_co = "https://denver.craigslist.org/search/sof?postedToday=1&nearbyArea=319&nearbyArea=210&nearbyArea=713&nearbyArea=287&nearbyArea=288&nearbyArea=315&searchNearby=2"


def craigs_jobs(url):
    req = requests.get(url, headers={"User-agent": "job_bot 1.0"})
    soup = BeautifulSoup(req.content, "html.parser")
    tags = soup.findAll("li", class_="result-row")
    for tag in tags:
        title = tag.find("a", class_="result-title hdrlnk")
        if title is not None and listing_filter(title.text):
            listing = Listing()
            listing.title = title.text
            location = tag.find("span", class_="result-meta").find("span", class_="nearby")
            listing.location = location.text if location is not None else "nearby"
            listing.date = tag.find("time", attrs={"datetime": True})["datetime"][:-6]
            listing.link = tag.find("a", class_="result-title hdrlnk", attrs={"href": True})["href"]
            listing.logo = "https://apprecs.org/ios/images/app-icons/256/4b/597638475.jpg"
            for job in jobs:
                if listing == job:
                    continue
            jobs.append(listing.to_dict())


craigs_jobs(craigslist_url_web_sb)
craigs_jobs(craigslist_url_web_tx)
craigs_jobs(craigslist_url_web_fl)
craigs_jobs(craigslist_url_web_wa)
craigs_jobs(craigslist_url_web_ut)
craigs_jobs(craigslist_url_web_wi)
craigs_jobs(craigslist_url_web_or)
craigs_jobs(craigslist_url_web_az)
craigs_jobs(craigslist_url_web_co)
craigs_jobs(craigslist_url_software_sb)
craigs_jobs(craigslist_url_software_tx)
craigs_jobs(craigslist_url_software_fl)
craigs_jobs(craigslist_url_software_wa)
craigs_jobs(craigslist_url_software_ut)
craigs_jobs(craigslist_url_software_wi)
craigs_jobs(craigslist_url_software_or)
craigs_jobs(craigslist_url_software_az)
craigs_jobs(craigslist_url_software_co)
'''
'''
# GOOGLE CAREERS
# google_url_web = "https://www.google.com/search?q=entry+level+web+developer+jobs&ibp=htl;jobs#fpstate=tldetail&htichips=date_posted:today&htidocid=ziFYbdR-ytsLOYbPAAAAAA%3D%3D&htischips=date_posted;today&htivrt=jobs"
# google_url_software = "https://www.google.com/search?q=entry+level+software+developer+jobs&ibp=htl;jobs#fpstate=tldetail&htichips=date_posted:today&htidocid=L7MdHDNb59o9XyVPAAAAAA%3D%3D&htischips=date_posted;today&htivrt=jobs"
'''
filtered_jobs = list(filter(lambda job: "Revature" not in job["company"], jobs))
# print(jobs)
print(len(jobs))
idx = 0
for job in filtered_jobs:
    job["idx"] = idx
    idx += 1

with open("jobs.json", "w") as jsonfile:
    jsonfile.write(json.dumps(filtered_jobs))
    jsonfile.close()
