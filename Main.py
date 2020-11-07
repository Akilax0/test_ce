'''
    REQUIREMENTS:
        pip install requests
    HELP:
        gihanjayatilaka[at]eng[dot]pdn[dot]ac[dot]lk

'''
import requests
from datetime import datetime

ORGANIZATION="cepdnaclk"
PROJECTS=[]
START_BATCH=10
END_BATCH=17
FIRST_YEAR=2
FINAL_YEAR=4
OUTPUT_FILE_NAME="index.html"


def urlOrganization():
    return "https://api.github.com/orgs/{}".format(ORGANIZATION)


def urlOrganizationRepos(pageNo):
    return "https://api.github.com/orgs/{}/repos?page={}".format(ORGANIZATION,pageNo)

def initialize():
    for batch in range(START_BATCH,END_BATCH+1):
        temp=[]
        for year in range(FIRST_YEAR,FINAL_YEAR+1):
            temp.append([])
        PROJECTS.append(temp)          

def inRange(x,minNumber,maxNumber):
    if type(x)==str:
        x=int(x)
    if minNumber>maxNumber:
        minNumber,maxNumber=maxNumber,minNumber
    if minNumber<=x and maxNumber>=x:
        return True
    else:
        return False


def writeHtmlPreamble():
    s="""
        <html>
        <head>
        <title>University of Peradeniya : Department of Computer Engineering : Projects</title>
        </head>
        <body>
        <h2><a href="https://www.pdn.ac.lk/">University of Peradeniya</a> : <a href="http://www.ce.pdn.ac.lk/">Department of Computer Engineering</a> : Projects</h2>
        <p>Other project listings: <a href="http://www.ce.pdn.ac.lk/projects/">http://www.ce.pdn.ac.lk/projects/</a> and <a href="https://cepdnaclk.github.io/sites/projects/">https://cepdnaclk.github.io/sites/projects/</a></p>

    """
    return s

def writeHtmlEnd():
    s="""<br><br>
        <p>Last update : {}<br>
        Maintainance information is given <a href="https://github.com/cepdnaclk/projects/">here</a>.
        Click <a href="https://gihan.me/contact/">here</a> for support.<br>
        If you want to get involved and improve this webpage (appearance or functionality) please contact roshanr[at]eng[dot]pdn[dot]ac[dot]lk.<br>
        </body>
        </html>
    """.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    return s

def writeHTMLContents():
    s="""<h3>Contents</h3>
    <ul>
    """
    for b in range(len(PROJECTS)):
        for y in range(len(PROJECTS[b])):
            if len(PROJECTS[b][y])>0:
                s = s + """<li><a href="#{}">{}</a></li>""".format("e"+str(b+START_BATCH)+"-"+str(y+FIRST_YEAR)+"yp", "E"+str(b+START_BATCH)+" "+str(y+FIRST_YEAR)+"<sup>"+th(y+FIRST_YEAR)+"</sup> year projects")
    
    s = s + "</ul>"
    return s

    #adfsad


def writeHTMLSection(batch,year):
    if len(PROJECTS[batch][year])==0:
        return ""
    
    s="""<h3 id="{}">{}</h3>""".format("e"+str(batch+START_BATCH)+"-"+str(year+FIRST_YEAR)+"yp", "E"+str(batch+START_BATCH)+" "+str(year+FIRST_YEAR)+"<sup>"+th(year+FIRST_YEAR)+"</sup> year projects")

    s = s + """<ul>"""

    for p in PROJECTS[batch][year]:
        title,url=p[0],p[1]
        title=title[0].capitalize()+title[1:]
        s = s + """<li>{} [<a href="{}">github</a>""".format(title,url)
        try:
            webUrl=url.replace("github.com/cepdnaclk/","cepdnaclk.github.io/")
            if str(requests.get(webUrl))=="<Response [200]>":
                s=s+""", <a href="{}">webpage</a>""".format(webUrl)
        except:
            1+1#Nothing here
        s=s+"""]</li>"""
    
    s=s+"""</ul>"""
    return s


def th(n):
    if n==1:
        return "st"
    elif n==2:
        return "nd"
    elif n==3:
        return "rd"
    else:
        return "th"

if __name__=="__main__":
    print("START")
    outputFile = open(OUTPUT_FILE_NAME,"w+")
    initialize()
    print(PROJECTS)
    URL = urlOrganization()
    r=requests.get(url=URL)
    j=r.json()
    print(j)
    print("\n\n\n\n")

    
    for p in range(1,1000):
        
        r=requests.get(url=urlOrganizationRepos(p))
        print(urlOrganizationRepos(p))
        # sleep(60)
        jsonData=r.json()

        print(p,jsonData)

        if len(jsonData)==0:
            break

        for i in range(len(jsonData)):
            print(i)
            repoName=jsonData[i]["name"].strip().split("-")
            if repoName[0][0]=="e":
                if repoName[1][1:]=="yp":
                    batch=int(repoName[0][1:])
                    year=int(repoName[1][:1])

                    if inRange(batch,START_BATCH,END_BATCH) and inRange(year,FIRST_YEAR,FINAL_YEAR):
                        PROJECTS[batch-START_BATCH][year-FIRST_YEAR].append([" ".join(repoName[2:]),jsonData[i]["html_url"]])
    
    outputFile.write(writeHtmlPreamble())
    outputFile.write(writeHTMLContents())
    for b in range(END_BATCH-START_BATCH+1):
        for y in range(FINAL_YEAR-FIRST_YEAR+1):
            outputFile.write(writeHTMLSection(b,y))
    outputFile.write(writeHtmlEnd())

    print("END")









