JobScraper - A set of python scripts that crawls job listing from a list of URLs 
and saves the resuls to a .html file for more convenient browsing. 
A naive web scraper custom built for my personal job hunt,
currently set to work on LinkedIn, Jobvector.de and the German indeed.com site.

HOW TO USE:---------------------------------------------------------------------

    Step 0) Preparation:

        To run JobScraper you need to have a version of Python 3 installed on 
	your system, as well als the following additonal libraries:
	
		beautifulsoup4
		requests

    Step 1) Adjust search parameters:

	The main script is ScrapeJobs_fast.py.
	
	For a search to work, you need to enter keywords for the search (e.g.
	"Data Scientist"), Cities to search and the search radius and the
	platform you want to search. The script will create a list of URLs out
	of these elements and request the html from the respective platforms.
	
	The script first gets all results from these URLs and then removes
	double entries (you might get the same job ad dozens of times!).
	
	Additionally, you can also enter a list of exclusion words. Any jobs that
	contain these terms will be deleted from the list as well.
	
	You have the option to pick between a fast variant, that just performs 
	one request per URL, and a slower one, that requests the indivudal job listings
	for a detailed description as mouseover text in the results page. This
	second round of requests is done after doubles and exclusion words are removed,
	but it is still a lot slower!
	
	Lastly, if you have previously performed job searches, the data of these
	scraping attempts will be saved in the Results folder. You can compare your
	current results with previous ones and either a) keep them in the list,
	where they will be marked blue, while nwe jobs are green or b) remove
	them from the result list.

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
	you can enter the filename of the comparison file into "PreviouslyScrapedJobs.txt" 
	contained in the "Results\\JobData" folder.

		yesterday = 'name_of_file_you_want_to_compare_to'

	This filename should be something like this:

		yesterday = 'JobData_05_14_2020_22_48_51' 

	If you run "ScrapeJobs.py" with a file writte in there, jobs in the current 
	search that are contained in the comparison file will be displayed with a 
	blue background. By doing this you can, for example, compare yesterday's 
	results with todays results and easily see the new jobs.
