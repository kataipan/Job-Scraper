# parse - helper functions for scrape module

##########################################################################

def  extract_keyword(URL, keywords):

    URL = URL.replace('%20',' ')
    URL = URL.replace('+',' ')

    jobKeywords = []
    for keyword in keywords:
        if keyword in URL:
            jobKeywords.append(keyword)

    return(jobKeywords)

def unpack_jobInfo(JobTitle, OrgName, City, Text):

    def check4Umlauts(string):

        Umlauts = ['ä', 'ü', 'ö', 'Ä', 'Ü', 'Ö', 'ß']
        Replacements = ['ae', 'ue', 'oe', 'Ae', 'Ue', 'Oe', 'ss']
        for i in range(len(Umlauts)):
            if Umlauts[i] in string:

                oldChar = Umlauts[i]
                newChar = Replacements[i]
                string = string.replace(str(oldChar), str(newChar))

        return(string)

    try:
        JobTitle = check4Umlauts(JobTitle.text)
        JobTitle.strip()
    except AttributeError:
        JobTitle = ''
    try:
        OrgName = check4Umlauts(OrgName.text)
        OrgName.strip()
    except AttributeError:
        OrgName = ''            
    try:
        City = check4Umlauts(City.text)
        City.strip()
    except AttributeError:
        City = ''
    try:
        Text = check4Umlauts(Text.text)
    except AttributeError:
        Text = ''
        
    return(JobTitle, OrgName, City, Text)
