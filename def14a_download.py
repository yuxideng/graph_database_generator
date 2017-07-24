import unicodedata
from SECEdgar.crawler import SecCrawler
import re, os, sys, time, glob, argparse, json
from bs4 import BeautifulSoup
import entities

# TODO considering intaking these variables from command line
COMPANY_COUNT = 8
date = "20170608"
count = "1"
mydir = ''
def filing_def14a(self, company_code, cik, priorto, count):

        self.make_directory(company_code, cik, priorto, 'DEF 14A')

        # generate the url to crawl
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+"&type=def+14a&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)
        print ("started 10-Q " + str(company_code))
        r = requests.get(base_url)
        data = r.text

        # get doc list data
        doc_list, doc_name_list = self.create_document_list(data)

        try:
            self.save_in_directory(company_code, cik, priorto, doc_list, doc_name_list, 'DEF 14A')
        except Exception as e:
            print (str(e))

        print ("Successfully downloaded all the files")

#use the following one (advance_clean_soup) for cleaning html text
def advance_clean_soup(filepath):
    with open(filepath, "r") as myfile:
        read_string = myfile.read()
    soup = BeautifulSoup(read_string)
    uni_str= soup.get_text()
    ascii_str = unicodedata.normalize('NFKD',uni_str).encode('ascii','ignore')
    #clearascii_str=re.sub('\n',' ',ascii_str)
    return str(ascii_str)


# DO NOT use the following function advance_clean. If you need to clean text, use advace_clean_soup
def advance_clean(filepath):
    with open(filepath, "r") as myfile:
        read_string = myfile.read()
    table_cleaner = re.compile('(?i)<table.*?</table>')
    regexs = [table_cleaner, '<.*?>', '\n', '\t', '&nbsp', '&#']
    for regex in regexs:
        read_string = re.sub(regex, ' ', read_string)
    return read_string


def get_filings(text_path,key,url):
    t1 = time.time()
    # create object
    #seccrawler = SecCrawler()
    # read data.txt
    with open(text_path) as f:
        content = f.readlines()

    # download DEF 14A for companies in data.txt
    for line in content:
        #parsing data.txt file
        line = line.replace("\n", "")
        pair = line.split(' ')
        mydir = os.path.join("SEC-Edgar-Data", pair[0], pair[1], "DEF 14A")
        #seccrawler.filing_def14a(pair[0], pair[1], date, count)
        allfiles = glob.glob(mydir + '/*.txt')
        selected = allfiles[len(allfiles) - 1]
        print selected
        in_str=advance_clean_soup(selected)
        in_strr=in_str[50000:80000]
        result=entities.run_relation(in_strr,key,url)
        with open(os.path.join(mydir,"relationships.json"),'w') as outfile:
            outfile.write((json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True).encode("utf8")))
        #print (json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True).encode("utf8"))
    t2 = time.time()
    print ("Total Time taken: "),
    print (t2 - t1)
