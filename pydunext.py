from bs4 import BeautifulSoup
import requests

import time

class User():
    def __init__(self, username, password):
        # Login to the website and get the cookies
        login_url = f"https://dpsgurgaon84.edunext1.com/SignUp?username={username}&password={password}"
        response = requests.post(login_url)
        self.cookies = response.cookies
        dashboardURL="https://dpsgurgaon84.edunext1.com/Applications?module=SljEjVHJzr0ianNlvVCQxw"
        response = requests.get(dashboardURL, cookies=self.cookies)
        soup = BeautifulSoup(response.text, "html.parser")
        self.photoURL=soup.find_all('img', {'class': 'profile-pic'})[0]['src']
        # print(self.photoURL)
        self.hwlist = self.__get_hw()
        self.circularlist = self.__get_circulars()

    # Use the cookies to access the main URL
    main_url = "https://dpsgurgaon84.edunext1.com/Applications?module=SljEjVHJzr0ianNlvVCQxw&redirecturl=L1N0dWRlbnREYXNoYm9hcmRBcHAvU0Fzc2lnbm1lbnRz"

    def __get_hw(self):
        response = requests.get(self.main_url, cookies=self.cookies)
        out = response.text
        table_data = []
        for row in BeautifulSoup(out, features="lxml")("tr"):
            table_data.append([cell.text for cell in row("td")])
        hw = {}
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the table element by its class or ID attribute
        # table = soup.find("table", {"class": "display table table-bordered no-footer"})
        ids=[]
        
        # Find all the buttons in the table
        
        buttons = soup.find_all("button", {"type": "button", "title": "Details", "class": "btn btn-primary btn-icon btn-rounded table-btn"})

        for button in buttons:
            onclick_value = button["onclick"].replace("viewopen(\"", "").replace("\")", "")
            id=onclick_value.split("&")[0].split("=")[1]
            ids.append(id)
        for id in ids:
            page=requests.get("https://dpsgurgaon84.edunext1.com/StudentDashboardApp/UpdateAssignment?said="+id, cookies=self.cookies)
            soupd = BeautifulSoup(page.text, "html.parser")
            subject=soupd.find_all("input", {"id": "classname"})[0].get("value")
            name=soupd.find_all("input", {"name": "name"})[0].get("value")
            date=soupd.find_all("input", {"id": "date"})[0].get("value")
            deadline=soupd.find_all("input", {"id": "deadlinedate"})[0].get("value")
            description=soupd.find_all("div", {"class": "col-lg-10"})[0].get_text()
            attachmentse=soupd.find_all("a", {"rel": "noopener noreferrer nofollow"})
            attachments={}
            if description=="None":
                description="No Description"
            if subject==None:
                subject="No Subject"
            if name==None:
                name="No Name"
            # if date==None:
            #     date=""
            if deadline==None:
                deadline="No Deadline"
            if attachmentse==None:
                attachmentse=[]
            for attachment in attachmentse:
                if attachment.get("href") != "https://edunexttechnologies.com":
                    attachments[attachment.text.replace('\r\n                                                    ','').replace('\n','')]="https://dpsgurgaon84.edunext1.com"+attachment.get("href")
            attachments.pop("",None)
            hw[id]={"subject":subject,"name":name,"date":date,"deadline":deadline,"description":description,"attachments":attachments}
            # print(subject,name,date,deadline,description)
        # Print the extracted data
        self.retrieved=time.time() # Time of retrieval
        return hw
    
    def __get_circulars(self):
        url="https://dpsgurgaon84.edunext1.com/StudentDashboardApp/SCirculars"
        response = requests.get(url, cookies=self.cookies)
        out = response.text
        soup = BeautifulSoup(out, "html.parser")
        circulars = {}
        # Find the table element by its class or ID attribute
        for i in range(1,50):
            hrefval='#accordion-control-group'+str(i)
            name=soup.find_all('a',{'href': hrefval})
            if len(name)==0:
                break
            else:
                name=name[0]
            data=soup.find_all('div',{'id': 'accordion-control-group'+str(i)})[0]
            attachmentse=soup.find_all('a',{'rel': 'noopener noreferrer nofollow'})[0]
            description=data.text.split('Attachment')[0].split('\n\n\n Description:\n')[1].replace('\r\n                                ','').replace('\n                        ','')
            circulars[name.text.replace('  ','').replace('\n','').replace('\r','').replace('\xa0\xa0\xa0\xa0Circular Subject:','')]={'description': description, 'attachments': []}
            if attachmentse['href'] != "https://edunexttechnologies.com":
                circulars[name.text.replace('  ','').replace('\n','').replace('\r','').replace('\xa0\xa0\xa0\xa0Circular Subject:','')]['attachments'].append({attachmentse.text.replace('\r\n                                ',''): "https://dpsgurgaon84.edunext1.com"+attachmentse['href']})
        return circulars
if '__main__' == __name__:
    username = input("Enter your admission number: ")
    password = input("Enter your password: ")
    user = User(username, password)
    print(user.hwlist)
    print(user.circularlist)
