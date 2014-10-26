import requests
import datetime
from BeautifulSoup import BeautifulSoup

FAKENAME_SERVICE = 'http://www.fakenamegenerator.com/gen-random-us-us.php'
MONTHS = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

class Identity(object):
    def setGender(self, gender):
        self.gender = 'M' if gender=='Male' else 'F'

    def setName(self, firstname, lastname, middlename=''):
        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename

    def setDOB(self, year, month, day):
        self.DOB = datetime.date(int(year), int(month), int(day))
    
    def setAddress(self, street, city, state, postcode):
        self.street = street
        self.city = city
        self.state = state
        self.postcode = postcode
    
    def setTelphone(self, telphone):
        self.telphone = telphone

    def toCSV(self):
        return '{lastname}, {firstname}, {gender}, {dob}, {address1}, {address2}, {address3}, {city}, {state}, {zip}, {telphone}'.format(
            lastname=self.lastname,
            firstname=self.firstname,
            gender=self.gender,
            dob=self.DOB,
            address1=self.street,
            address2='',
            address3='',
            city=self.city,
            state=self.state,
            zip=self.postcode,
            telphone=self.telphone)       

    def __str__(self):
        return 'Name: {firstname} {middlename} {lastname}\n\
Gender: {gender}\n\
Address: {street} {city} {state} {postcode}\n\
Telphone: {telphone}\n\
Date of Birth: {dob}'.format(
            firstname=self.firstname,
            middlename=self.middlename,
            lastname=self.lastname,
            gender=self.gender,
            street=self.street,
            city=self.city,
            state=self.state,
            postcode=self.postcode,
            telphone=self.telphone,
            dob = self.DOB)

    def __repr__(self):
        return str(self)


def generateIdentity():    
    r = requests.get(FAKENAME_SERVICE)
    parsed = BeautifulSoup(r.content)
    # parse gender
    bcsDiv = parsed.find('div', {'class': 'bcs'})
    img = bcsDiv.find('img')
    gender = img['alt']

    infoDiv = parsed.find('div', {'class': 'info'}).find('div', {'class': 'content'})
    # parse name
    firstname, middlename, surname = infoDiv.find('div', {'class': 'address'}).find('h3').string.split(' ')
    middlename = middlename[:-1]
    # parse address
    addressDiv = infoDiv.find('div', {'class': 'address'}).find('div', {'class': 'adr'})
    address1 = addressDiv.contents[0].strip()
    city, rest = addressDiv.contents[2].strip().split(',')
    state, postcode = rest.strip().split(' ')
    # parse telphone
    telphone = infoDiv.find('li', {'class': 'tel'}).find('span').string
    # parse day of birth
    dobStr = infoDiv.find('li', {'class': 'bday'}).string
    dobStr = dobStr[:dobStr.index('(')]
    rest, year = dobStr.strip().split(',')
    month, day = rest.strip().split(' ')
    year = year.strip()

    identity = Identity()
    identity.setGender(gender)
    identity.setName(firstname, surname, middlename)
    identity.setDOB(year, MONTHS[month], day)
    identity.setTelphone(telphone)
    identity.setAddress(address1, city, state, postcode)
    return identity


def main():
    identity = generateIdentity()
    print(identity)
    print(identity.toCSV())

if __name__ == '__main__':
    main()

