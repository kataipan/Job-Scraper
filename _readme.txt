JobScraper - python script set that crawls job listing from a list of URLs 
and saves the resuls to an .html file. 
Currently works for linkedin and German indeed.

HOW TO USE:---------------------------------------------------------------------

    Step 0) Preparation:

        To run JobScraper you need to have a version of Python 3 installed on 
	your system, as well als the following additonal modules:
	
		beautifulsoup4
		requests

	You can install modules by searching for cmd under windows and 
	entering something like the following in the command line:

		python -m pip install beautifulsoup4

    Step 1) Create list of job query URLs:

	Open "make_URLList.py" in a texteditor of your choice or python's IDLE.
	For each query you usually do on a given job platform, e.g. indeed.com,
	enter the keywords, city and distance and run the script "make_URLList.py".
	This will create the shelve files for "URLs" that will be needed later.
	Note that the city for now can only be single word, unless you modify
	the entries for yourself.

    Step 2) Run "ScrapeJobs.py"

	The script should now iterate through all your URLs and the contained 
	Jobs and write them into a new .html file in the Folder 
	'.\JobScraper\Results\'. You can open this file in your browser of choice.
	
	The links displayed on the page contain the job description as mouseover 
	text.


Options:-------------------------------------------------------------------------

You can adjust a few things in ScrapeJobs.py:

Sort by city:
	If you want to sort the resulting job list alphabetically by city 
	(or rather location), set the constant "sort_by_city" to "True"
	
	Sorting by company is not yet implemented.	

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