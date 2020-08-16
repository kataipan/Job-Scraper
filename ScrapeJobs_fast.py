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

def ScrapeJobs():
    
    # set up constants
    # change entries accordingly ###################################################

    keywords = ['Gehirn', 'neuro', 'electroencephalogram', 'imaging',
                'biology', 'biologist', 'life science',
                'naturwissenschaften', 'bioinformatic',
                'naturwissenschaftler', 'Matlab', 'cognitive', 'affective',
                'behaviour',
                'brain', 'data science', 'neuroscience',
                'neurowissenschaft', 'biomarker', 'jupyter', 'python',
                'pandas', 'numpy', 'scientific programmer',
                'digital signal processing', 'neuro', 'brain',
                'brain-computer', 'brain-machine']

                # 'natural science'

    # [city, search radius]
    Cities = [
              ['Amsterdam',             20],
              ['Copenhagen',            20],
##              ['Stockholm',             20],
##              ['Lissabon',              20],
              ['Nürnberg',              20],
              ['Würzburg',              20],
              ['Leipzig',               10],
              ['Freiburg im Breisgau',  50],
              ['Basel',                 10],
              ['Karlsruhe',             10],
              ['Heidelberg',            20],
              ['Hamburg',               20],
              ['München',               20],
              ['Zürich',                20],
              ['Tübingen',              20],
##              ['Göttingen',             20],
              ['Stuttgart',             20],
             ['Köln',                  20],
              ['Berlin',                20],
              ['Wien',                  20],
              ['Lausanne',              10],
              ['Bern',                  20],
              ['Strasbourg',            20],
              ['Mannheim',              10],
              ['Frankfurt',             20]
                ]
    
    Sites = ['indeed', 'jobvector', 'linkedin'] # 'jobvector', 'linkedin', 'indeed']     # 'jobvector', 'linkedin', 'indeed'

    # list of keywords to exclude jobs
    NoNoWords = [' ra ',
                 'abschlussarbeit', 'account', 'administator', 'affairs',
                     'appliation manager', 'application', 'arbeit', 'arzt',
                     'ausbildung', 'aussendienst', 'auszubilden',
                     'außendienst',
                 'bachelor', 'berater', 'bundesweit', 'business',
                     'buchhalter',
                 'carosserie', 'chemiker', 'compliance', 'consultant',
                     'consulting', 'customer', 'chemie', 'chemisch',
                 'director',
                 'enrolled', 'ergotherapeut',
                 'fachangestellt', 'financial',
                 'gmp',
                 'head',
                 'in vivo', 'ingenieurpraktikant', 'intern', 'internship',
                 'kundenservice',
                 'laborant', 'lead', 'liaison', 'lehrer',
                 'marketing', 'mfa', 'microbiolog', 'mta',
                 'nachhilfe',
                 'physician', 'postdoc', 'praktikant',
                     'praktikum', 'produktion', 'professor',
                 'qc', 'qm', 'qualitaet', 'quality', 'quality assurance',
                 'recruiter', 'referent', 'rzt',
                 'sales', 'seminar', 'senior', 'student',
                 'technician', 'techniker', 'thesis', 'therapeut', 'tutor',
                 'unternehmensberatung',
                 'vertrieb',
                 'werkstudent',
                 'zertifikat', 'zivildienst']

    NoNoCompany = ['campusjäger']

    # options

    # time distance to re-consider previously scraped jobs
    previousThreshold = 14
    
    # sorting (only one option ca be active) 
    sort_by_city = True
    sort_by_company = False
    sort_by_jobtitle = False

    # generate additional separate result pages for keywords?
    split_by_keyword = True

    # scrape detailed job descriptions?
    scrape_job_details = False # SLOW!

    # remove previously found jobs from listing?
    remove_old_jobs = False

    #########################################################################################################

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
