from bs4 import BeautifulSoup
import requests
from time import sleep
import shutil
import string

login_URL = "https://xx/login"
baseUrl = "https://xx"

USERNAME = "xx"
PASSWORD = "xx"

outputdir = "xx"


def getSession():
    session_requests = requests.session()
    login = session_requests.get(login_URL , verify=False)

    # extract the token
    token=""
    soup = BeautifulSoup(login.text, "html.parser")
    for n in soup('input'):
        if n['name'] == '_token':
            token = n['value']
            break

    # now post to that login page with some valid credentials and the token
    auth = {
    'email': USERNAME
    , 'password': PASSWORD
    , 'login_xx': ' '
    , 'login_xx':' '
    , '_token': token}
    #print(auth)
    session_requests.post(login_URL, data=auth)

    return session_requests



def getWebStuff():
    s = getSession()
    fileNumber = 1
    #Last Observation
    URL = "https://xxxxx"


    while (URL!=""):
        print(f"Processing : {URL}")

        r = s.get(URL,verify=False)
        #print(r.text)

        soup = BeautifulSoup(r.content, "html.parser")


        #find the obs name and date
        topLink = soup.find('div',"main-content").h1
        ObservationName = topLink.text.strip()


        #Remove invalid chars
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        #print(valid_chars)
        ObservationName= ''.join(c for c in ObservationName if c in valid_chars)
        print(ObservationName)


        meta = soup.find('meta', attrs={'name':'obs-id'})
        ObservationMeta = meta.attrs['content']
        token = ""
        for n in soup('input'):
            if n['name'] == '_token':
                token = n['value']
                break



        #Get the PDF download
        Data = {
        'pdf_options[format]': 'default'
        , 'pdf_options[show_author]': 1
        , 'pdf_options[show_date]': 1
        , 'pdf_options[show_comments]':1
        , '_token': token}


        sleep(2)
        #Get the PDF file for the observation
        response = s.post(URL, data=Data, stream=True)
        sleep(2)

        #Set the filename
        filename = f'{outputdir}{ObservationMeta}-{ObservationName}-{fileNumber}.pdf'

        #Write the PDF file down
        chunk_size =2000
        with open(filename ,'wb') as fd:
            for chunk in response.iter_content(chunk_size):
                fd.write(chunk)

        #Find and download any images
        for img in soup.find_all("img", class_="obs-media"):
            imglink = img['src']

            url = imglink
            response = s.get(url, stream=True)
            fileNumber = fileNumber +1
            filename = f'{outputdir}{ObservationMeta}-{ObservationName}-{fileNumber}.png'
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            sleep(2)

        # find the next ob link
        nextURL = soup.find("li", class_="next").a['href']
        URL = nextURL
        #Reset the file number
        fileNumber = 1
        sleep(2)


def main():
    getWebStuff()

if __name__ == "__main__":
    main()