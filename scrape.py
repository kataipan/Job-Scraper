# scrape module

from bs4 import BeautifulSoup
import requests
import parse
import os
import shelve
import datetime as dt
from numpy import random as rnd

###################################################################
# request-functions ###############################################

def grab_linkedin(URL, Jobs):

    # grab all content of specified website  
    page = requests.get(URL)

    # parse HTML with BeautifulSoup
    soup = BeautifulSoup(page.content, "html5lib")

    # get job listings
    linkz = soup.findAll('li', class_='result-card job-result-card result-card--with-hover-state')

    # isolate job contents
    JobCount = 1
    for linkNum in range(len(linkz)):
        print(' ' * 4 + 'Job# ' + str(JobCount))
        
        link = linkz[linkNum]
        
        OrgName = link.find('a', class_="result-card__subtitle-link job-result-card__subtitle-link")
        City = link.find('span', class_="job-result-card__location")
        JobTitle = link.find('h3', class_="result-card__title job-result-card__title")
        Text = link.find(class_="job-result-card__snippet")
        JobLink = link.find('a', class_="result-card__full-card-link")
        ScrapeDate = dt.date.today()

        JobTitle, OrgName, City, Text = parse.unpack_jobInfo(JobTitle, OrgName, City, Text)

        Jobs.append({'JobTitle': JobTitle, 'OrgName': OrgName, 'City': City,\
            'Link': str(JobLink.get('href')), 'Text': Text, 'PreviouslyScraped': False, 'ScrapeDate': ScrapeDate})

        JobCount += 1
    return(Jobs)

###################################################################

def grab_jobvector(URL, Jobs):

    # grab all content of specified website  
    page = requests.get(URL)

    # parse HTML with BeautifulSoup
    soup = BeautifulSoup(page.content, "html5lib")

    # get job listings
    linkz = soup.findAll('div', class_='list-group-item')

    # isolate job contents
    JobCount = 1
    for linkNum in range(len(linkz)):
        print(' ' * 4 + 'Job# ' + str(JobCount))
        
        link = linkz[linkNum]
        
        OrgName = link.find(class_="company_name")
        City = link.find('li', class_="hidden-md hidden-xs")
        JobTitle = link.find(class_="list-group-item-heading")
        Text = link.find(class_="job_teaser")
        JobLink = link.find('a', class_="list-group-item-resultlist")
        ScrapeDate = dt.date.today()

        JobTitle, OrgName, City, Text = parse.unpack_jobInfo(JobTitle, OrgName, City, Text)

        Jobs.append({'JobTitle': JobTitle.strip(), 'OrgName': OrgName.strip(), 'City': City.strip(),\
            'Link': ('https://www.jobvector.de' + str(JobLink.get('href'))), 'Text': Text, 'PreviouslyScraped': False, 'ScrapeDate': ScrapeDate})

        JobCount += 1
    return(Jobs)

###################################################################

def grab_indeed(URL, Jobs):

    # grab all content of specified website  
    page = requests.get(URL)

    # parse HTML with BeautifulSoup
    soup = BeautifulSoup(page.content, "html5lib")

    # get job listings
    linkz = soup.findAll('a', class_="jobtitle turnstileLink")
    ResultcardContent = soup.findAll(class_="sjcl")
    Summaries = soup.findAll(class_="summary")

    # isolate job contents
    JobCount = 1
    for linkNum in range(len(linkz)):
        print(' ' * 4 + 'Job# ' + str(JobCount))

        ResultCard = ResultcardContent[linkNum]
        
        OrgName = ResultCard.find(class_="company")
        City = ResultCard.find(class_="location accessible-contrast-color-location")
        JobTitle = linkz[linkNum]
        Text = Summaries[linkNum]
        JobLink = linkz[linkNum]
        ScrapeDate = dt.date.today()

        JobTitle, OrgName, City, Text = parse.unpack_jobInfo(JobTitle, OrgName, City, Text)

        Jobs.append({'JobTitle': JobTitle, 'OrgName': OrgName, 'City': City,\
            'Link': ('https://indeed.com' + str(JobLink.get('href'))), 'Text': Text, 'PreviouslyScraped': False, \
                     'ScrapeDate': ScrapeDate})

        JobCount += 1

    return(Jobs)
##############################################################################

def get_details(Jobs):

    print('scraping job details')
    print('this might take a while...')

    for job in range(len(Jobs)):
        if Jobs[job].keys() and Jobs[job]['PreviouslyScraped']==False: # ónly get details for new jobs for speed
            Link = Jobs[job]['Link']
            if 'indeed' in Link:
                page = requests.get(Link)
                soup = BeautifulSoup(page.content, 'html5lib')
                Text = soup.find('div', class_ = 'jobsearch-jobDescriptionText')
                d, d, d, Jobs[job]['Text'] = parse.unpack_jobInfo([], [], [], Text)
            elif 'jobvector' in Link:
                page = requests.get(Link)
                soup = BeautifulSoup(page.content, 'html5lib')
                Text = soup.find('div', id='jobdescription')
                d, d, d, Jobs[job]['Text'] = parse.unpack_jobInfo([], [], [], Text)
            elif 'linkedin' in Link:
                page = requests.get(Link)
                soup = BeautifulSoup(page.content, 'html5lib')
                Text = soup.find('div', class_='description__text description__text--rich')
                d, d, d, Jobs[job]['Text'] = parse.unpack_jobInfo([], [], [], Text)

    return Jobs

###################################################################
# clean-up ########################################################

def doubles(Jobs):
    nocount = 0
    for CheckJob in range(len(Jobs)):
        if Jobs[CheckJob] != {}:
            AddDoublesKeywords = []
            for AgainstJob in range(CheckJob + 1, len(Jobs)):
                if Jobs[AgainstJob] != {}:
                    if Jobs[CheckJob]['JobTitle'] == Jobs[AgainstJob]['JobTitle'] and \
                       Jobs[CheckJob]['OrgName'] == Jobs[AgainstJob]['OrgName']:

                        AddDoublesKeywords.append(Jobs[AgainstJob]['keywords'][0]) # get str out of list

                        Jobs[AgainstJob] = {}

                        nocount += 1
                    else:
                        continue
                else:
                    continue

            # carry over keywords of double entries
            if AddDoublesKeywords != []:
                AddDoublesKeywords.append(Jobs[CheckJob]['keywords'][0])
                UniqueKeywords = set(AddDoublesKeywords)
                Jobs[CheckJob]['keywords'] = []
                for keyword in UniqueKeywords:
                    Jobs[CheckJob]['keywords'].append(keyword)
        else:
            continue

    print("    %d out of %d"%(nocount,len(Jobs)) + ' jobs marked as double entries')
    return(Jobs, nocount)

################################################################################

def nogo(Jobs, NoNoWords):

    nocount = 0;
    for CheckJob in range(len(Jobs)):
        if Jobs[CheckJob] != {}:

            B = Jobs[CheckJob]['JobTitle']
            B = B.lower()

            for nonoWord in NoNoWords:
                n = nonoWord.lower()
                if nonoWord in B:
           
                    Jobs[CheckJob] = {}
                    nocount += 1
                    break # to prevent re-entering the loop if two words match

        
    print("    %d out of %d"%(nocount,len(Jobs)) + ' jobs marked as no-go entries')
    return(Jobs)

################################################################################

def nogo_company(Jobs, NoNoCompany):

    nocount = 0
    for CheckJob in range(len(Jobs)):
        if Jobs[CheckJob] != {}:

            C = Jobs[CheckJob]['OrgName']
            C = C.lower()
            C = C.split(' ')

            for nonoCompany in NoNoCompany:
                if nonoCompany in C:
                    print("    No-No company '" + nonoCompany + "' detected in '" +  \
                          Jobs[CheckJob]['JobTitle'] + ',' + Jobs[CheckJob]['OrgName'])
                    
                    Jobs[CheckJob] = {}
                    nocount += 1
                    break # to prevent re-entering the loop if two words match
        
    print("    %d out of %d"%(nocount,len(Jobs)) + ' jobs marked as no-go company')
    return(Jobs)

###################################################################
# sorting-functions ###############################################

def by_city(Jobs):

    print('    sorting jobs alphabetically by city')

    # extract list of all cities
    cities = []
    for i in range(len(Jobs)):
        if Jobs[i] != {}:
            cities.append(Jobs[i]['City'])

    # sort alphabetically
    cities = sorted(set(cities))

    sortedJobs = []    
    for i in range(len(cities)):
        c = cities[i]
        for j in range(len(Jobs)):
            if Jobs[j] != {} and Jobs[j]['City'] == c:
                sortedJobs.append(Jobs[j])
                
    Jobs  = sortedJobs

    return(Jobs)

def by_jobtitle(Jobs):

    print('    sorting jobs alphabetically by title')

    # extract list of all cities
    jobtitles = []
    for i in range(len(Jobs)):
        if Jobs[i] != {}:
            jobtitles.append(Jobs[i]['JobTitle'])

    # sort alphabetically
    cities = sorted(set(jobtitles))

    sortedJobs = []    
    for i in range(len(jobtitles)):
        c = jobtitles[i]
        for j in range(len(Jobs)):
            if Jobs[j] != {} and Jobs[j]['JobTitle'] == c:
                sortedJobs.append(Jobs[j])
                
    Jobs  = sortedJobs

    return(Jobs)

def by_company(Jobs):

    print('    sorting jobs alphabetically by company')

    # extract list of all cities
    companies = []
    for i in range(len(Jobs)):
        if Jobs[i] != {}:
            companies.append(Jobs[i]['OrgName'])

    # sort alphabetically
    cities = sorted(set(companies))

    sortedJobs = []    
    for i in range(len(companies)):
        c = companies[i]
        for j in range(len(Jobs)):
            if Jobs[j] != {} and Jobs[j]['OrgName'] == c:
                sortedJobs.append(Jobs[j])
                
    Jobs  = sortedJobs

    return(Jobs)
    
###################################################################
# modifying functions #############################################

def compare2oldJobs(Jobs, timeThreshold):

    # Comparsed new jobs to specified list of previously scraped jobs and marks
    # recurring entries accordingly. If, however, the date an old job was scraped
    # exceeds a threshold (like 7 days), the job is deleted from the old job list
    # and thus recognized as new. This is to allow for re-advertised jobs to show up as new.

    OldJobFilename = ''
    
    try:
        OldJobsList = open('.\\Results\\JobData\\PreviouslyScrapedJobs.txt')
        OldJobContent = OldJobsList.read()
        
        yesterday = OldJobContent.strip("yesterday = '")

        OldJobsFile = shelve.open('.\\Results\\JobData\\' + yesterday)
        OldJobs = OldJobsFile['URLs']

        OldJobFilename = yesterday

        for oldJob in OldJobs:
            for j in range(len(Jobs)):
                # job has been scraped before
                if Jobs[j] !={} and \
                   Jobs[j]['JobTitle'] == oldJob['JobTitle'] and \
                    Jobs[j]['OrgName'] == oldJob['OrgName']:

                    if 'ScrapeDate' in oldJob:
                        # check date threshold
                        PrevScrapeDate = oldJob['ScrapeDate']
                        Delta = dt.date.today() - PrevScrapeDate 

                        if  Delta.days <= timeThreshold:
                            Jobs[j].update({'PreviouslyScraped': True})
                            Jobs[j].update({'ScrapeDate': PrevScrapeDate}) # we carry over the original scraping date, so that we can actually track and display the time since it was first scraped
                        else:
                            Jobs[j].update({'PreviouslyScraped': False}) # treated as new although in list
                            Jobs[j].update({'ScrapeDate': PrevScrapeDate}) # we mark it as new, but keep the original scraping date, so we can differentiate between true nwe jobs and re-advertised ones
                    else:
                        Jobs[j].update({'PreviouslyScraped': True})
                    
    except KeyError:
        print('key error')
        return(Jobs, OldJobFilename)

    return(Jobs, OldJobFilename)
    
###################################################################
# saving ##########################################################

def save_html(Jobs, date_time, OldJobFilename, NoNoWords, URLList):

    # unpack arguments
    URLList = ''.join(URLList)
    sites = []
    if 'xing' in URLList:
        sites.append('Xing')
    if 'linkedin' in URLList:
        sites.append('Linkedin')
    if 'indeed' in URLList:
        sites.append('Indeed')
    if 'jobvector' in URLList:
        sites.append('Jobvector')
    
    # prepare filename
    OldJobFilename = OldJobFilename.strip('.html')
    OldJobFilename = OldJobFilename.strip('JobData_')

    # create folder
    SavePath = os.path.abspath('.') + "\\Results\\" + date_time
    os.mkdir(SavePath)

    DisplayJobFile = open(SavePath + "\\DisplayJobs_" \
                          + date_time + ".html" ,'w')

    # construct html
    HTML_header = '''<!doctype html>
        <html><head>

        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0"><!-- Stylesheets -->
        <link href='http://fonts.googleapis.com/css?family=Delius+Swash+Caps' rel='stylesheet' type='text/css'>
        <link href='http://fonts.googleapis.com/css?family=Signika' rel='stylesheet' type='text/css'>
        <link href='http://fonts.googleapis.com/css?family=Sacramento' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap-theme.min.css">
        <link rel="stylesheet" href="_ressources/css/screen.css" type="text/css"/>
        <style>
        .myDiv1 {
          padding: 10px;
          border: 2px outset white;
          background-color: rgb(217, 234, 249); <!-- lightblue -->  
            }
        .myDiv2 {
          padding: 10px;
          border: 2px outset white;
          background-color: rgb(206, 252, 204); <!-- lightgreen -->
            }
        .headlineDiv {
          padding: 10px;
          background-color: rgb(232, 232, 232); <!-- grey --> 
        .keywordSpan {
          color: darkgray;
            }
        </style>
        </head>

        <body>
            <div class="headlineDiv">
                <h3>Job-search results:</h3>
                <h4> ''' + date_time + ' vs. ' + OldJobFilename + '''</h4>''' +\
                'Exclusion words: ' + str(NoNoWords) + '<br><br>' +\
                         'searched on ' + str(sites) + \
                '''</div>'''
            

    DisplayJobFile.write(HTML_header)

    # write job results to html
    for job in range(len(Jobs)):
        if Jobs[job] != {}:
            try:
                Title = Jobs[job]['JobTitle']
                Company = Jobs[job]['OrgName']
                City = Jobs[job]['City']

                k = set(Jobs[job]['keywords'])
            
                Keywords = ', '.join(i for i in k)

                # difference today - scrape date
                ScrapeDate = Jobs[job]['ScrapeDate']
                TimeDiff = dt.date.today() - ScrapeDate

                if TimeDiff.days == 0:
                    TimeDiffDays = 'new'
                else:
                    TimeDiffDays = str(TimeDiff.days) + ' days ago'

                # change color to indicate new(or old enough to be new) and old jobs
                if Jobs[job]['PreviouslyScraped'] == True:
                    divClass = 'myDiv1'
                else:
                    divClass = 'myDiv2'

##                HTML_element = '<div class="' + divClass + '"><a href="' + Jobs[job]['Link'] + \
##                                   '" title="' + Jobs[job]['Text'] + \
##                                   '"><strong>' + Title + '<strong></a><br>' + Company + \
##                                   '<br>' + City + LineBreak + '<span style="color: darkgray">' \
##                                   + TimeDiffDays + '</span>' + \
##                                    '<br><br><span style="color: darkgray">' \
##                                    + Keywords + '</span></div>'

                HTML_element = '<div class="' + divClass + '">' + \
                               '<span style="color: darkgray">' \
                                   + TimeDiffDays + '</span><br>' +'<a href="' + Jobs[job]['Link'] + \
                                   '" title="' + Jobs[job]['Text'] + \
                                   '"><strong>' + Title + '<strong></a><br>' + Company + \
                                   '<br>' + City + \
                                    '<br><br><span style="color: darkgray">' \
                                    + Keywords + '</span></div>'
    
                DisplayJobFile.write(HTML_element)
            except UnicodeEncodeError:
                continue
        else:
            continue

    DisplayJobFile.write('<body><html>')
    
    # save
    DisplayJobFile.close()

    return(date_time)

#################################################################################################

def save_jobData(Jobs, date_time):
    import os
    import shelve
    from datetime import datetime

    d = shelve.open(os.path.abspath('.') + "\\Results\\JobData\\JobData_" \
                          + date_time)
    
    d['URLs'] = Jobs
    d.close()

################################################################################

def split_by_keyword(Jobs, date_time, keywords):

    SavePath = os.path.abspath('.') + "\\Results\\" + date_time

    # create new html file for each keyword
    for keyword in keywords:
        
        DisplayJobFile = open(SavePath + "\\DisplayJobs_" \
                              + date_time + '_' + keyword + ".html" ,'w')

        # construct html
        HTML_header = '''<!doctype html>
            <html><head>

            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0"><!-- Stylesheets -->
            <link href='http://fonts.googleapis.com/css?family=Delius+Swash+Caps' rel='stylesheet' type='text/css'>
            <link href='http://fonts.googleapis.com/css?family=Signika' rel='stylesheet' type='text/css'>
            <link href='http://fonts.googleapis.com/css?family=Sacramento' rel='stylesheet' type='text/css'>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap-theme.min.css">
            <link rel="stylesheet" href="_ressources/css/screen.css" type="text/css"/>
            <style>
            .myDiv1 {
              padding: 10px;
              border: 2px outset white;
              background-color: rgb(217, 234, 249); <!-- lightblue -->  
                }
            .myDiv2 {
              padding: 10px;
              border: 2px outset white;
              background-color: rgb(206, 252, 204); <!-- lightgreen -->
                }
            .headlineDiv {
              padding: 10px;
              background-color: rgb(232, 232, 232); <!-- grey --> 
            .keywordSpan {
              color: darkgray;
                }
            </style>
            </head>

            <body>
                <div class="headlineDiv">
                    </div>'''
                

        DisplayJobFile.write(HTML_header)

        # write job results to html
        for job in range(len(Jobs)):
            if Jobs[job] != {} and keyword in Jobs[job]['keywords']:
                try:
                    Title = Jobs[job]['JobTitle']
                    Company = Jobs[job]['OrgName']
                    City = Jobs[job]['City']

                    k = set(Jobs[job]['keywords'])
                    Keywords = ', '.join(i for i in k)

                    # difference today - scrape date
                    ScrapeDate = Jobs[job]['ScrapeDate']
                    TimeDiff = dt.date.today() - ScrapeDate
                    TimeDiffDays = TimeDiff.days
                    print(TimeDiffDays)

                    # change color to indicate new and old jobs
                    if Jobs[job]['PreviouslyScraped'] == True:
                        divClass = 'myDiv1'
                        TimeDiffDays = str(TimeDiff.days) + ' days ago'
                        LineBreak = '<br><br>'
                    
                    else:
                        divClass = 'myDiv2'
                        TimeDiffDays = ''
                        LineBreak = ''

                    print(TimeDiff)

                    HTML_element = '<div class="' + divClass + '"><a href="' + Jobs[job]['Link'] + \
                                   '" title="' + Jobs[job]['Text'] + \
                                   '"><strong>' + Title + '<strong></a><br>' + Company + \
                                   '<br>' + City + LineBreak + '<span style="color: darkgray">' \
                                   + TimeDiffDays + '</span>' + \
                                    '<br><br><span style="color: darkgray">' \
                                    + Keywords + '</span></div>'
    
                    DisplayJobFile.write(HTML_element)
                except UnicodeEncodeError:
                    continue
            else:
                continue

        DisplayJobFile.write('<body><html>')
        
        # save
        DisplayJobFile.close()
