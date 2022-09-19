#import the libraries
from bs4 import BeautifulSoup
import re
import requests
import time
import csv

try:
    urls=[]         
    seen=set()
    #fetch the page links for all locations in the list
    locations=['New+York%2C+NY','Manhattan%2C+NY','Silicon+Valley%2C+CA','Jersey+City%2C+NJ','Washington%2C+DC','California','Massachusetts','Illinois','Virginia','Texas','Tennessee','Pennsylvania','Oregon','Ohio','North+Carolina','South+Carolina','Missouri','Minnesota','Michigan','Maryland','Georgia','Florida','Connecticut','Colorado','Idaho','Arizona','Indiana','Utah','Alabama']
    for loc in locations:
        for pageNum in range(0,100):
            urls.append('https://www.indeed.com/jobs?q=data%20scientist&l={}&start={}'.format(loc,str(pageNum*10)))
      
    #print(urls)
    
    #open the file to write job desc,job title
    fw=open('Data_Scientist.csv','w',encoding='utf8')
    writer=csv.writer(fw,lineterminator='\n')
    count=0
    page=0
    #fetch the links for each job from page
    for url in urls:
        for i in range(5): # try 5 times
            #send a request to access the url
            response=requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            time.sleep(2)
            if response: 
                break # we got the file, break the loop
            else:time.sleep(2) # wait 2 secs
            
            
        # all five attempts failed, return  None
        if not response: print(None)
        data=response.text# read in the text from the file
        soup = BeautifulSoup(data, 'html5lib')
        jobs=soup.findAll('a',{'class':re.compile(r'tapItem fs-unmask result'),'href':re.compile(r'/clk?')})
         
        for job in jobs:
           link=job.get('href')
           time.sleep(2)
                   
           link1='https://www.indeed.com' + link
           print('Done')
           #for each JOB's webpage, you need to connect to the link first:
           job_response = requests.get(link1)
           time.sleep(3)
           print("test3")
           job_data = job_response.text
           job_soup = BeautifulSoup(job_data, 'html5lib')
           
           #fetch the job description text from html
           job_description_tag = job_soup.find('div',{'id':'jobDescriptionText'})
           job_description = job_description_tag.text if job_description_tag else "N/A"
           jd="".join(job_description.splitlines())
           
           if jd in seen: continue # skip duplicate job desc
           seen.add(jd)
        
           writer.writerow([jd,'Data Scientist']) 
           count=count+1
           print(count)
        page=page+1
        print("page",page)
    fw.close()
except:
    print("Error occured")
