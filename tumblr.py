#!/usr/local/bin/python3

import tkinter as tk
import pytumblr as pytumblr
import threading

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
  'mLvXdqzLEzBIqS3JO7IyDmjI8jdY61qMDTRzTUdf6ojmXOYufX'
)

# Make the request
# likes = client.likes()

# print(likes)

# followings = client.following()['blogs']
# followings = client.following(offset=0, limit=10)['blogs']

# for following in followings:
#     print(following['name'])
#     pass

# info = client.info()
# print(info)

# def getFollowing(offset=0, limit=20):
#     return client.following(offset=offset, limit=limit)['blogs']

# def getAllFollowing():
#     allFollowing = []
#     currentLength = 0
#     maxLength = info['user']['following']
#     while currentLength < maxLength:
#         following = client.following(offset=currentLength, limit=20)['blogs']
#         print(currentLength)
#         for _following in following:
#             print(_following['name'])
#         allFollowing.extend(following)
#         currentLength += len(following)
#     return allFollowing

# allFollowing = getAllFollowing()
# for following in allFollowing:
#     print(following['name'])
#print(len(allFollowing))

#posts = client.posts('listentoloveme', type='video')['posts']

def getAllPosts(name):
    allPosts = []
    currentLength = 0
    maxLength = 1
    while currentLength < maxLength:
        posts = client.posts(name, type='video', offset=currentLength, limit=20)
        maxLength = posts['total_posts']
        posts = posts['posts']
        allPosts.extend(posts)
        currentLength += len(posts)
    return allPosts

#allPosts = getAllPosts('listentoloveme')
#for post in allPosts:
#    print(post['video_url'])

LIMIT = 20

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.state = 'wait'
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.label = tk.Label(self, text='input tumblr username U want to grab')
        self.label.pack(side='top')

        self.input = tk.Entry(self)
        self.input.pack(side='top')
        self.input.insert('end', '')

        self.hi_there = tk.Button(self, text='get', command=self.getContent)
        self.hi_there.pack(side="top")

        self.textArea = tk.Text(self)
        self.textArea.pack(side='bottom')

    def getContent(self):
        if self.state == 'loading':
            self.state = 'waitToStop'
            print('waitToStop')
            return
        elif self.state == 'waitToStop':
            print('please wait to stop first')
            return
        name = self.input.get()
        print('start to grab:', name)
        self.getAllPosts(name)

    def getAllPosts(self, name):
        self.state = 'loading'
        t = threading.Thread(target=self.getPosts, args=(name, 0))
        t.setDaemon(True)
        t.start()

    def getPosts(self, name, currentLength):
        print('wait to load %s to %s:' % (currentLength, currentLength + LIMIT))
        posts = client.posts(name, type='video', offset=currentLength, limit=LIMIT)
        maxLength = posts['total_posts']
        posts = posts['posts']
        currentLength += len(posts)
        text = ''
        for post in posts:
            if('video_url' in post):
                text += (post['video_url'] + '\n')
        self.textArea.insert('end', text)
        print(text, currentLength, maxLength)
        if self.state == 'waitToStop':
            self.state = 'wait'
            print('stop to load more')
            return
        if currentLength >= maxLength or len(posts) == 0:
            print('end, no more')
            return
        else:
            t = threading.Thread(target=self.getPosts, args=(name, currentLength))
            t.setDaemon(True)
            t.start()


root = tk.Tk()
app = Application(master=root)
app.mainloop()