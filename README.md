# FundMe
A search tool to return information about research grant support on a given list of diseases.

##Overview:
FundMe.py will search the PubMed database for articles on diseases from a given list and return grant information. 
FundMe uses the Entrez E-utility API for PubMed. See http://www.ncbi.nlm.nih.gov/books/NBK25501. 

##To use:
1. Make sure you have python running on your machine. See https://wiki.python.org/moin/BeginnersGuide/Download
2. Download FundMe.py to your machine.
3. Open a terminal window.
4. Navigate to the directory containing FundMe.py
5. Create file containing a list of diseases of interest.
6. Enter `"python FundMe.py"`
7. Follow prompts in terminal.

##Input:
1. Path of a disease file. Disease file must be a .txt file with one disease per line.
2. Path for two output files, a summary file and a data file.
3. Start year. Beginning of year range for article search (ex: `2010`).
4. End year. End of year range for article search (ex: `2015`).

##Output:
1. Summary information with:
   
  a. Disease name

  b. Number of articles with the disease in the article title (maximum of 1000).
    
  c. Number of these articles with listed grant support.
    
  d. Percentage of articles with listed grant support.
    
  e. List of grant agencies and number of articles with support from that agency.
2. Data for each article with:
    
  a. Disease name

  b. Article title

  c. Year published

  d. Grant agency, if any

  e. Grant ID, if any

