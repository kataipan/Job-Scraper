JobScraper - A set of python scripts that crawl job listings from a list of URLs 
and saves the results to a .html file for more convenient browsing. 
A naive web scraper custom built for my personal job hunt, currently set to work 
on LinkedIn, Jobvector.de and the German indeed.com site.

BASE FUNCTIONALITY:--------------------------------------------------------------

A list of URLs is generated from search terms, locations, radius and websites,
used for requests and then parsed to form a html list of jobs with the form

	[new/ scrape date]
	Job Name [links to job ad]
	Company
	City
	
	[search term/s]
	
Jobs are either highlighted green to indicate new jobs, or blue to indicate 
previously scraped jobs. If previously scraped jobs surpass a certain time 
threshold, they will be indicated as green again. This happens to ensure that
jobs that are re-advertised are caught as new rather than ignored.

CONTENTS:-----------------------------------------------------------------------

- ScrapeJobs_fast	The main script that manages high-level control and has
			several options for the job-search (see next section).
- scrape		Module containin the main request and processing functions.
- parse			Module that includes a few string-processing methods
- Make_URLList		Module that generates the URLs for requests based on the
			options specified in ScrapeJobs_fast.
- requirements.txt	To install dependencies (currently unneccessarily bloated)

HOW TO USE:---------------------------------------------------------------------

    Step 1) Adjust search parameters:

	The main script is ScrapeJobs_fast.py.
	
	For a search to work, you need to enter keywords for the search (e.g.
	"Data Scientist"), Cities to search and the search radius in a list, as
	well as the platform you want to search. 
	
	Additionally, you can also enter a list of exclusion words. 
	Any jobs that contain these terms will be deleted from the list as well.
	
	You have the option to pick between a fast variant, that just performs 
	one request per URL, and a slower one, that requests the indivudal job 		
	listings for a detailed description as mouseover text in the results 			
	page. This second round of requests is done after doubles and exclusion 		
	words are removed, but it is still a lot slower!
	
	Lastly, if you have previously performed job searches, the data of these
	scraping attempts will be saved in the Results folder. You can compare 	
	your current results with previous ones and either a) keep them in the 			
	list, where they will be marked blue, while new jobs are green or 
	b) 	remove them from the result list.

Options in detail:-------------------------------------------------------------------------

You can adjust a few things in ScrapeJobs.py:

Sort by city:
	If you want to sort the resulting job list alphabetically by city 
	(or rather location), set the constant "sort_by_city" to "True"

Exclusion keywords:
	If you wish to change the list of no-no words, which remove job 
	descriptions with undesirable keywords, navigate to NoGoWords 
	(crtl + f --> NoNoWords) and change the words contained in that list. 
	Note that all entries should be lower case.

	The same can be done for undesired companies in NoGoCompany

Compare to old jobs:
	By default, the entries in the resulting job list are of a green background.
	If you wish to compare the results of the current search to a previous one, 
	you can enter the filename of the comparison file into 
	"PreviouslyScrapedJobs.txt" contained in the "Results\\JobData" folder.

		yesterday = 'name_of_file_you_want_to_compare_to'

	This filename should be something like this:

		yesterday = 'JobData_05_14_2020_22_48_51' 

	If you run "ScrapeJobs.py" with a file writte in there, jobs in the current 
	search that are contained in the comparison file will be displayed with a 
	blue background. By doing this you can, for example, compare yesterday's 
	results with todays results and easily see the new jobs.
