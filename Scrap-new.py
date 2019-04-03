
# coding: utf-8

# In[3]:


import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import urllib.request
from tqdm import tqdm


# In[119]:


movieName = 'avengers_endgame'
movieYear = '2019'
moviePageURL = f'http://www.impawards.com/{movieYear}/{movieName}_gallery.html'
response = requests.get(moviePageURL)


# In[8]:


soup = BeautifulSoup(response.text, "html.parser")


# In[70]:


allLinks = soup.findAll('a')


# In[74]:


posterLinks = [link for link in allLinks if link.img and link.img['src'].find('posters') >= 0]


# In[77]:


postersPages = [a['href'] for a in posterLinks]


# In[125]:


postersToDownload = []


# In[141]:


for posterPage in tqdm(postersPages):
    url = f'http://www.impawards.com/2019/{posterPage}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    allLinks = soup.findAll('a')
    posterLinks = [link for link in allLinks if link['href'].find(movieName) >= 0 and link.contents[0].find('x') not in [None, -1]]
    bigestPosterName = posterLinks[-1]['href']
    bigestPosterName = bigestPosterName.replace('html', 'jpg')
    biggestPosterLink = f'http://www.impawards.com/{movieYear}/posters/{bigestPosterName}'
    postersToDownload.append(biggestPosterLink)


# In[144]:


with open('test.txt', 'w') as file:
    file.write('\n'.join(postersToDownload))


# In[145]:


for poster in tqdm(postersToDownload):
    urllib.request.urlretrieve(poster, poster.split('/')[-1])


# In[147]:


import aria2p


# In[167]:


aria2p.add_uris(uris=["http://www.impawards.com/2019/posters/avengers_endgame_xxlg.jpg"])


# In[191]:


import comtypes.client as cc
import comtypes

referrer = ""
cookie = ""
postData = ""
user = ""
password = ""
cc.GetModule(["{ECF21EAB-3AA8-4355-82BE-F777990001DD}",1,0])
# not sure about the syntax here, but cc.GetModule will tell you the name of the wrapper it generated
import comtypes.gen.IDManLib as IDMan
idm1 = cc.CreateObject("IDMan.CIDMLinkTransmitter", None, None, IDMan.ICIDMLinkTransmitter2)
idm1.SendLinkToIDM("http://www.impawards.com/2019/posters/avengers_endgame_xxlg.jpg",
referrer, cookie, postData, user, password, r"C:\\", "idman401.exe", 0)

