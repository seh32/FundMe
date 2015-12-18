"""FundMe.py: Returns grant information from PubMed on an inputted list of diseases using Entrez E-utilities API"""

__author__ = 'Susan Hromada'
__email__ = 'seh32@students.calvin.edu'
__data__ = 'December 2015'

import urllib2
from bs4 import BeautifulSoup


def main():
    """Run the FundMe program"""
    # prompt user input
    inputfile = raw_input("Please enter path of disease file: ")
    summaryfile = raw_input("Please enter desired path of output summary file: ")
    datafile = raw_input("Please enter desired path of output data file: ")
    print "Please enter year range for article search: "
    start_year = raw_input("Start year (ex: '2010'): ")
    end_year = raw_input("End year (ex: '2015'): ")
    # clear contents of summaryfile and datafile
    sf = open(summaryfile, 'w')
    sf.seek(0)
    sf.truncate()
    sf.write("Year range: " + start_year + "-" + end_year + '\n')
    sf.close()
    df = open(datafile, 'w')
    df.seek(0)
    df.truncate()
    df.close()
    # read disease file
    filein = open(inputfile, 'r')
    diseaselist = []
    for line in filein:
        diseaselist.append(line.strip())
    for disease in diseaselist:
        idlist = disease_search(disease, start_year, end_year)
        grant_info(idlist, disease, summaryfile, datafile)
    print "Search complete. See " + summaryfile + " and " + datafile + " for results."


def disease_search(disease, start_year, end_year):
    """
    Return search result idlist for a disease

    Keyword arguments:
    disease -- one disease, str
    summaryfile -- location for summary output file
    datafile -- location for data output file

    return:
    idlist -- list of str
    """
    # set up URL of PubMed search
    esearch_base = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=xml&term="
    searchterm = disease.replace(" ", "+")
    year = ' AND ("' + start_year + '"[Date - Publication] : "' + end_year + '"[Date - Publication]) '
    yearterm = year.replace(" ", "%20")
    final_url = esearch_base + searchterm + yearterm + "&retmax=1000"
    # get xml data
    xml_obj = urllib2.urlopen(final_url)
    data = xml_obj.read()
    # find list of article IDS
    soup = BeautifulSoup(data, 'html.parser')
    ids = soup.find_all('idlist')
    idlist = []
    # convert into list format
    for tag in ids:
        i = str(tag.text)
        split = i.split('\n')
        idlist = split[1:(len(split) - 1)]
    return idlist


def grant_info(myidlist, disease, summaryfile, datafile):
    """
    Write grant information for articles in an idlist to file

    Keyword arguments:
    myidlist -- idlist, list of str
    disease -- one disease, str
    summaryfile -- location for summary output file
    datafile -- location for data output file
    """
    print "Searching " + disease + "..."
    numarticles = 0
    numarticles_with_grants = 0
    agencydict = {}
    data = open(datafile, 'a+')
    summary = open(summaryfile, 'a+')
    for item in myidlist:
        # get xml data from pubmed API
        efetch_base = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id="
        id = item
        final_url2 = efetch_base + id
        xml_obj = urllib2.urlopen(final_url2)
        contents = xml_obj.read()
        # general information
        soup = BeautifulSoup(contents, 'html.parser')
        try:
            title = (str(soup.find('articletitle').text))
        except UnicodeEncodeError:
            title = "UnicodeEncodeError. See Pubmed article id " + str(item)
        except AttributeError:
            title = "AtributeError. See Pubmed article id " + str(item)
        year = str(soup.find('year').text)
        # grant information
        grants = soup.find_all('grant')
        grantids = []
        grantagencies = []
        for tag in grants:
            # get grant agency info
            if "agency" in str(tag):
                agency = (str(tag.find('agency').text))
                if agency not in grantagencies:
                    grantagencies.append(agency)
                    agencydict[agency] = agencydict.get(agency, 0) + 1
            # get grant id info
            if "id" in str(tag):
                grantid = (str(tag.find('grantid').text).replace(" ", ""))
                if grantid not in grantids:
                    grantids.append(grantid)
        # append article information to datafile
        data.write(item + '\n' + disease + '\n' + "Title: " + title + '\n' + year + '\n')
        if len(grantagencies) > 0:
            data.write("Grant Agencies: " + ' '.join(map(str, grantagencies)) + '\n')
        if len(grantids) > 0:
            data.write("Grant IDs: " + ' '.join(map(str, grantids)) + '\n')
        data.write('\n')
        # save information for summary file
        numarticles += 1
        if len(grantids) > 0 or len(grantagencies) > 0:
            numarticles_with_grants += 1
    # help pretty print dictionary
    list2 = []
    for item in agencydict.items():
        item = str(item).replace("'", "")
        list2.append(item[1:len(item) - 1])
    # append disease information to summary.txt
    summary.write("Disease: " + disease + '\n' + "Total articles: " + str(
        numarticles) + '\n' + "Articles with listed grants: " + str(
        numarticles_with_grants) + '\n' + "Percentage articles with listed grants: " + str(
        float(numarticles_with_grants) / float(numarticles)) + '\n\t' + ('\n\t'.join(map(str, list2))) + '\n' + '\n')

# run the program
main()
