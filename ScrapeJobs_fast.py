#! python3

## ScrapeJobs.py - web scraper that collects job listings for combinations
## of keywords and locations from a variety of platforms
## (currently LinkedIn, German Indeed and jobvector) and saves the links to an HTML file for easy
## browsing. After compilation of a all jobs from all desired URLs, double entries
## and jobs containing undesired keywords are removed from the list.

import scrape
from datetime import datetime
import make_URLList
import parse
import os 
import tkinter as tk
from tkinter import filedialog

def ScrapeJobs(): # main function
    
    # set up constants
    # change entries accordingly ###################################################

    keywords = ['data science',
                'python',
                'biology']

    # [city, search radius]
    Cities = [['Leipzig',               10],
              ['Hamburg',               20],
              ['München',               20],
              ['Berlin',                20],
                ]
    
    Sites = ['indeed', 'jobvector', 'linkedin'] # 'jobvector', 'linkedin', 'indeed']     # 'jobvector', 'linkedin', 'indeed'

    # list of keywords to exclude jobs
    NoNoWords = ['sales', 'consulting']

    NoNoCompany = ['Nestle']

    # options ##################################################################

    # time in days after which already scraped jobs
    # are considered as new again (to catch re-advertisments etc.)
    previousThreshold = 10
    
    # sorting (only one option can be active at a time)
    # within eacht category, sorting is alphabetical
    sort_by_city = True
    sort_by_company = False
    sort_by_jobtitle = False

    # generate additional result pages for each separate search term?
    split_by_keyword = True

    # scrape detailed job descriptions? WARNING: SLOW!
    scrape_job_details = False

    # remove previously found jobs from listing?
    remove_old_jobs = False

    ############################################################################
    # scrape #############################################################################

    # check for Results folder
    if not os.path.isdir('.\\Results'):
        print('Creating Results folder...')
        
        os.mkdir('.\\Results')
        os.mkdir('.\\Results\\JobData')
        file = open('.\\Results\\JobData\\PreviouslyScrapedJobs.txt' ,'x')
        file.write("yesterday = ''")
        file.close()

    # pick file with old jobs for comparison
    rootPath = os.path.abspath('.')
    resultPath = rootPath + '\\Results\\JobData\\'
    os.chdir(resultPath)

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title = "Select file", \
                filetypes = (("dat.files","*.dat"),))

    fileName = file_path.split('JobData')
    fileName = fileName[-1].split('.')
    fileName = 'JobData' + fileName[0]

    file = open(resultPath + 'PreviouslyScrapedJobs.txt', 'w')
    file.write("yesterday = '" + fileName + "'")
    file.close()

    os.chdir(rootPath)

    # check for option conflicts
    if int(sort_by_city) + int(sort_by_company) + int(sort_by_jobtitle) > 1:
        raise ValueError('Sorting Options Conflict: Please set only one sorting option to True')
        
    # time script
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
    startTime = now

    # create URLList
    URLList = make_URLList.make_URLList(keywords, Cities, Sites)

    # scrape jobs from URLs
    Jobs = []
    ContentList = []

    for URL in URLList:
        print(URL)
        jobKeywords = parse.extract_keyword(URL, keywords)
        
        if 'linkedin' in URL:
            scrape.grab_linkedin(URL, Jobs)
        elif 'indeed' in URL:
            scrape.grab_indeed(URL, Jobs)
        elif 'jobvector' in URL:
            scrape.grab_jobvector(URL, Jobs)
        else:
            print('no method for this URL type')
            continue

        for job in Jobs:
            if 'keywords' not in job.keys():
                job['keywords'] = jobKeywords

    print('\n')
    print("Scraping complete")
    print('\n')
    print('    Time to complete(h:mm:ss.ms):' + str(datetime.now() - startTime))
    print("    %d Jobs found in %d URLs" %(len(Jobs), len(URLList)))


    # save job data
    scrape.save_jobData(Jobs, date_time)
        # saving before removing doubles etc.,
        # so we can use all entries for comparisons in the future 
    
    # check for doubles
    Jobs, nocount = scrape.doubles(Jobs)

    # check for no-no words
    scrape.nogo(Jobs, NoNoWords)
    scrape.nogo_company(Jobs, NoNoCompany)

    # compare to previously scraped jobs
    Jobs, OldJobFilename = scrape.compare2oldJobs(Jobs, previousThreshold)

    # count previously scraped jobs and optionally remove
    PrevScrCount = 0
    for i in range(len(Jobs)):
        if Jobs[i] != {}:
            if Jobs[i]['PreviouslyScraped'] == True:
                if remove_old_jobs:
                    Jobs[i] = {}

                PrevScrCount += 1

    print('    ' + str(PrevScrCount) + ' previously scraped Jobs')
    
    # get detailed job description if desired
    if scrape_job_details == True:
        scrape.get_details(Jobs)

    # evaluate sort by company/city option
    if sort_by_city:
        Jobs = scrape.by_city(Jobs)
    elif sort_by_company:
        Jobs = scrape.by_company(Jobs)
    elif sort_by_jobtitle:
        Jobs = scrape.by_jobtitle(Jobs)

    # create job display
    print("    removing doubles and no-go's")
    print('    saving results...')

    c = 0
    for i in range(len(Jobs)):
        if Jobs[i] != {}:
            c += 1
    print(str(c) + ' Jobs remaining')

    # create html file
    scrape.save_html(Jobs, date_time, OldJobFilename, NoNoWords, URLList)

    if split_by_keyword:
        scrape.split_by_keyword(Jobs, date_time, keywords)

ScrapeJobs()
