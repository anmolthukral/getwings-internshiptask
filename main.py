from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import datetime
import urllib2
import json

class Loggedusers(ndb.Model):
    email=ndb.StringProperty(indexed=True)
    lat=ndb.FloatProperty(indexed=False)
    longitude=ndb.FloatProperty(indexed=False)
    time_login=ndb.DateTimeProperty(indexed=False)
    time_logout=ndb.DateTimeProperty(indexed=False)
    login_flag=ndb.StringProperty(indexed=True)
    intrests=ndb.StringProperty(indexed=True,default="NONE")


LOGIN_WIKI="""
<p> the login will use your google account to login, by simple user authentication API and your saved google account state.</p>

"""    

WIKIINTRO="""
<h1> the internship task submitted by ANMOL THUKRAL </h1>
<p> this is the basic working of the api/webapp asked for the internship task<p>
<p>The below mentioned are the details of the user, which is logged in more likely emailID and location<br/>
THE LOCATION IS FETCHED AUTOMATICALLY WITH THE USE OF "FREEGEOIP", i guess this won't be against the rule
refrence to freegeoip is <a href="http://freegeoip.net/json/" >FREEGEOIP></a> click on the above link to get your location as a json
</p>
"""

FORM_ADDINTERNST=""" 
<h1> FORM TO ADD INTERSTS</h1>
<p> the mentioned below form is used to call the form uses addinterst controller which updates the database as per the provided intersts</p>
<br/><br/><br/><br/><br/>
<form action="/addinterst" method="post">
<input type="text" name="interest" />
<input type="submit" value="addintest" />
</form>
<br/><br/><br/><br/>


"""


API_HTML="""
    <br/>
    <h1 style="color:red;" >API block</h1>
    <a href="/api" >click here to check the API </a>
    <h1> WIKI about API</h1>
    <p> this link is used to call basic api which provides the JSON data for the users in the data base which are available whether loged in or not
    The link calls the /api controller in an unparameterized way
    </p><br/><h2>CALL: /api?login=true</h2>
    <a href="/api?login=true" >click here to check the API with filter of logged in users </a>
    <p> this link is used to call basic api which provides the JSON data for the users in the data base which are available whether loged in
    <br/>The link also calls  the /api controller in an parameterized way
    </p>
    <br/><h2>CALL: /api?login=false</h2> 
    <a href="/api?login=false" >click here to check the API with filter of logged out users </a>
    <p> this link is used to call basic api which provides the JSON data for the users in the data base which are available whether loged in/or not depending on the paramenter passed
    <br/>The link also calls  the /api controller in an parameterized way
    </p>
    <h2>CALL: /api?filer=cricket</h2>
    <a href="/api?filter=cricket" >click here to check the API with filter of intrests </a>
    <p> this link is used to call basic api which provides the JSON data for the users in the data base which have there interst as <em>CRICKET</em> <br/>
    <br/>The link also calls  the /api controller in an parameterized way
    <br/> </p>

    <h1> THE APICONTROLLER or in this Class APIHandler is used in order to manage all the API calls</h1>

    <h2> some other environment details</h2>
    <p> the webapp is build with python programming language and uses GOOGLE APPENGINE as its runtime and also the NDB datastore is used in this project which is the highly scalable google's implementation for python's appengine framework</p>

    """

# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            self.response.write(user.nickname)
            self.response.write(WIKIINTRO)
            self.response.write("welcome <br/>")
            self.response.write("\n"+ user.email())
            time=datetime.datetime.now()
            logout_time=datetime.datetime(2016,12,17,0,0)
            self.response.write("<br/>")
            self.response.write(datetime.datetime.now().time())
            emailid=user.email()
            key_email=ndb.Key(Loggedusers,user.email())
            query=Loggedusers.query(Loggedusers.email==emailid)
            logusers=query.fetch()
            if not logusers:
                f = urllib2.urlopen('http://freegeoip.net/json/',timeout=10000)
                json_string = f.read()
                f.close()
                location=json.loads(json_string)
                latitude=location['latitude']
                longitude=location['longitude']
                loggedusers=Loggedusers(email=user.email(),lat=latitude,longitude=longitude,time_login=time,login_flag="yes",time_logout=logout_time,key=key_email)
                USER_KEY=loggedusers.put()
            else:
                for loguser in logusers:
                    loguser.login_flag="yes"
                    loguser.time_login=time
                    loguser.time_logout=logout_time
                    loguser.put()
            logusers=query.fetch()
            loggedusers=logusers[0]
            self.response.write("<br/> your current location is")
            self.response.write("<br/>")
            self.response.write(loggedusers.lat)
            self.response.write("<br/>")
            self.response.write(loggedusers.longitude)
               
            url="/logout"
            url_linktext="logout"         
        else:
            self.response.write(LOGIN_WIKI)
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        self.response.write("<br/> <a href=\""+url+"\">"+url_linktext+"</a>" )    
        if user:
            self.response.write( FORM_ADDINTERNST)
            self.response.write(API_HTML)

# [END main_page]


class Logout(MainPage):
    def  get(self):
        user=users.get_current_user()
        emailid=user.email()
        query=Loggedusers.query(Loggedusers.email==emailid)
        logusers=query.fetch(1)
        for loguser in logusers:
            loguser.login_flag="no"
            loguser.time_logout=datetime.datetime.now()
            key=loguser.put()
        url = users.create_logout_url("/")
        self.redirect(url)

        
class Addinterst(webapp2.RequestHandler):
    def post(self):
        intersts=self.request.get('interest')
        self.response.write(intersts)
        user=users.get_current_user()
        emailid=user.email()
        self.response.write(user)
        query=Loggedusers.query(Loggedusers.email==emailid)
        logusers=query.fetch()
        self.response.write(logusers)
        for loguser in logusers:
            if loguser.intrests=='NONE':
                loguser.intrests=intersts
                self.response.write(loguser.intrests)
            else:
                loguser.intrests=loguser.intrests+","+intersts 
                self.response.write(loguser.intrests)
            key=loguser.put()
            self.response.write(loguser.intrests)
        self.redirect("/")


class APIHandler(webapp2.RequestHandler):
    def get(self):
        login=self.request.get('login')
        filer=self.request.get('filter')
        user=users.get_current_user()
        emailid=user.email()
        query=Loggedusers.query(Loggedusers.email!=emailid)
        #login =true query
        if login=='true':
            query=query.filter(Loggedusers.login_flag=="yes")
        if login=='false':
            query=query.filter(Loggedusers.login_flag=="no")
        otherusers=query.fetch()
        splitstring=""
        if filer:
            splitstring=filer.split(',')
        latitude=0.0
        longitude=0.0
        logusers=Loggedusers.query(Loggedusers.email==emailid)
        listusers=[]
        for loguser in logusers:
            latitude=loguser.lat
            longitude=loguser.longitude
            json_write="{ \"email\":\""+loguser.email+"\",\"intersts\":\""+loguser.intrests+"\",\"latitude\":\""+str(loguser.lat)+"\",\"longitude\":\""+str(loguser.longitude)+"\", \"login staus\":\""+loguser.login_flag+"\" }"
        for otheruser in otherusers:
            otherlat=otheruser.lat
            otherLong=otheruser.longitude
            otherinter=otheruser.intrests
            if not splitstring:
                listusers=fetcher()
            else:
                for single in splitstring:
                    if single not in otherinter:
                        continue
                    else:
                        listusers=fetcher()
        listusers.sort(key=lambda x: x.distance, reverse=True)
        json_string = json.dumps(listusers, default=obj_dict)
        self.response.write('{ "current_user": ')
        self.response.write(json_write)
        self.response.write('},{ "other_users": ')
        self.response.write(json_string)
        self.response.write("}   } ")

    def fetcher():    
        fetchurl="https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins="+str(latitude)+","+str(longitude)+"&destinations="+str(otherlat)+","+str(otherLong)+"&key=[API_KEY_HERE_SERVER_KEY]"
        f = urllib2.urlopen(fetchurl,timeout=10000)
        json_string = f.read()
        f.close()
        rows=json.loads(json_string)
        try:
            distance=rows['rows'][0]['elements'][0]['distance']['value']
        except:
            distance=0.0
            tempObject=DistanceUser(otheruser.intrests,distance,otherlat,otherLong,otheruser.email,otheruser.login_flag)
            listusers.append(tempObject)
        return listusers    



def obj_dict(obj):
    return obj.__dict__


class DistanceUser:
    def __init__(self,intersts,distance,latitude,longitude,email,login):
        self.intrests=intersts
        self.distance=distance
        self.latitude=latitude
        self.longitude=longitude
        self.email=email
        self.login=login

    def toJson():
            json_str="{ \"email\":\""+self.email+"\",\"intersts\":\""+self.intersts+"\",\"distance\":\""+str(self.distance)+"\",\"latitude\":\""+str(self.latitude)+"\",\"longitude\":\""+str(self.longitude)+"\", \"login staus\":\""+self.login+"\" }"
            return json_str



route=[
    ('/',MainPage),
    ('/logout',Logout),
    ('/addinterst',Addinterst),
    ('/api',APIHandler)
    ]
app = webapp2.WSGIApplication(route, debug=True)
# [END app]