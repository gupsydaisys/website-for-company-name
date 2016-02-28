import testData
import convert

d, notFound, query2URLS = convert.matchURLToName(testData.getNCompanies(15))
for k in d:
    print k
    print d[k]
    print

print notFound


# query2URLS = {}
# query2URLS['Southern Company'] = ['http://www.southerncompany.com/', 'http://www.southerncompany.com/about-us/careers/home.cshtml', 'http://www.southerncompany.com/what-doing/energy-innovation/nuclear-energy/job-opportunity.cshtml', 'https://en.wikipedia.org/wiki/Southern_Company']
# d, notFound = convert.getBestURLForName(query2URLS)

##################### CORRECT ANSWER SIMPLE ##########################################
# query2URLS = {}
# query2URLS["Microsoft"] = ['https://www.microsoft.com/', 'https://www.microsoft.com/en-us/download', 'https://support.microsoft.com/', 'https://en.wikipedia.org/wiki/Microsoft']
# query2URLS["National Pen Company"] = ['http://www.pens.com/national-pen-company', 'http://www.pens.com/', 'http://www.pens.com/customer-service-national-pen', 'http://www.pens.com/about-national-pen']
# query2URLS["Designzillas, LLC"] = ['http://www.designzillas.com/', 'http://www.designzillas.com/hiring', 'http://www.designzillas.com/about-us', 'http://www.designzillas.com/contact-us']
# query2URLS["California College of Arts"] = ['https://www.cca.edu/', 'https://www.cca.edu/academics', 'https://www.cca.edu/admissions', 'https://en.wikipedia.org/wiki/California_College_of_the_Arts']
# query2URLS["Flynn"] = ['http://www.flynncenter.org/', 'https://flynn.io/', 'https://en.wikipedia.org/wiki/Errol_Flynn', 'https://github.com/flynn/flynn']
# d, notFound = convert.getBestURLForName(query2URLS)

# for k in d:
#     print k
#     print d[k]
#     print

# print notFound

# Microsoft -> microsoft.com
# National Pen Company -> nationalpen.com
# Designzillas, LLC -> designzillas.com
# California college of Arts -> cca.edu
# Flynn -> flynn.io