#! python3
# make_URLList.py - Creates and saves a list of jobsearch query links

def make_URLList(keywords, Cities, Sites):

    import shelve
    import os

    ###############################################################################

    print('\n')
    print('creating URL list...')

    URLList = [];

    for c in range(len(Cities)):

        # change search radius according to city
        city = Cities[c][0]
        Distance = str(Cities[c][1])

        for site in Sites:
            if site == 'linkedin':
                for keyword in keywords:
                    if ' ' in keyword:
                        keyword = keyword.split(' ')
                        keyword = '%20'.join(keyword)

                    URLList.append('https://www.linkedin.com/jobs/search/?distance='+ \
                                Distance + '&keywords=' + keyword +
                                '&location=' + city + '&sortBy=R')

            elif site == 'xing':
                for keyword in keywords:   
                    if ' ' in keyword:
                        keyword = keyword.split(' ')
                        keyword = '%20'.join(keyword)

                    URLList.append('https://www.xing.com/jobs/search?page=1&keywords='+ \
                                    keyword + '&location=' + city+ '&radius=' + \
                                Distance + '&sort=date')

            elif site == 'jobvector':
                for keyword in keywords:   
                    if ' ' in keyword:
                        keyword = keyword.split(' ')
                        keyword = '%20'.join(keyword)

                    URLList.append('https://www.jobvector.de/stellensuche.html?keywords=' + keyword + \
                        '&locations=' + city + '&distance=' + Distance + '&sort=date_start&_pn=0')

            elif site == 'indeed':
                for keyword in keywords:   
                    if ' ' in keyword:
                        keyword = keyword.split(' ')
                        keyword = '+'.join(keyword)

                    # change toplevel domain according to city
                    if 'Zürich' in city or 'Basel' in city or 'Bern' in city or 'Leausanne' in city:
                        Domain = 'ch'
                    else:
                        Domain = 'de'

                    URLList.append('https://' + Domain + '.indeed.com/jobs?q=' + \
                                    keyword + '&l=' + city + '&radius=' + Distance)



    print('done')
    print('\n')

    return(URLList)
