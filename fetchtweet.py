from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from PIL import ImageTk,Image
import tkinter.font
import os
import time

window=tk.Tk()
window.geometry("500x450")
window.title("FetchTweets")
window.configure(bg="#B0E2FF")

font=tk.font.Font(family="Eras Medium ITC",size=30)

lbl_title=tk.Label(text="FETCHTWEETS",font=font,bg="#B0E2FF",fg="#0D4F8B")
lbl_title.pack(pady=10)
bg=ImageTk.PhotoImage(file="twitter.jpg")
lbl_1=tk.Label(image=bg,bg="#B0E2FF")
lbl_1.pack(pady=10)

lbl_name=tk.Label(text="Enter name of the person whose tweets you want to display ",font="20")
lbl_name.pack(pady=10)

ent_name=tk.Entry(width=30,font="Arial 10",bg="lightyellow")
ent_name.pack(pady=10)

#Function for extracting tweets from twitter
def fetch(name):
    #open chrome
    driver = webdriver.Chrome(ChromeDriverManager().install())
    time.sleep(2)
    
    #open url
    driver.get(f"https://twitter.com/search?q={name}&src=typed_query")
    time.sleep(2)
    
    #clicking 'people' tab
    driver.find_element_by_link_text('People').click()
    time.sleep(2)

    #selecting the first result
    results=driver.find_elements_by_css_selector(".css-1dbjc4n.r-j7yic.r-qklmqi.r-1adg3ll.r-1ny4l3l")
    results[0].click()
    time.sleep(3)

    #extracting name,twitter handle and bio
    fetch.username=driver.find_element_by_css_selector(".css-901oao.r-18jsvk2.r-1qd0xha.r-adyw6z.r-1vr29t4.r-135wba7.r-bcqeeo.r-1udh08x.r-qvutc0").text
    fetch.handle=driver.find_element_by_css_selector(".css-901oao.css-bfa6kz.r-m0bqgq.r-18u37iz.r-1qd0xha.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0").text
    fetch.bio=driver.find_element_by_css_selector(".css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0").text
    #print(username,handle,bio)

    #Extracting tweets
    heigh=1500
    driver.execute_script("window.scrollTo(0,{})".format(heigh))
    time.sleep(2)
    fetch.tws={}
    date=driver.find_elements_by_xpath("//*[@data-testid='tweet']/div[2]/div[1]/div[1]/div/div/a")
    tweet=driver.find_elements_by_xpath("//*[@data-testid='tweet']/div[2]/div[2]/div[1]")
    for j in range(0,len(tweet)):
        fetch.tws[tweet[j].text]=date[j].text

    #closing chrome
    driver.close()

#Function for second window
def func():
    name=ent_name.get()
    fetch(name)
    window.configure(bg="#B0E2FF")
    for widget in window.winfo_children():
        widget.destroy()

    #heading for the window
    tweet_lbl=tk.Label(text="TWEETS",fg='white',bg='#0D4F8B',font='Arial 10')
    tweet_lbl.pack(ipady=5,ipadx=5,pady=10)
    
    #Frame for bio
    frame_name=tk.Frame(bg="#B0E2FF")
    frame_name.pack(anchor="w",padx=20)
    label_name=tk.Label(master=frame_name,text="Name : ",bg="#B0E2FF",font="Verdana 10 bold italic",fg="#0D4F8B")
    label_name.pack(side="left")
    label_name2=tk.Label(master=frame_name,text=fetch.username,font="Verdana 10 ",bg="#B0E2FF")
    label_name2.pack(side="right")

    frame_handle=tk.Frame(bg="#B0E2FF")
    frame_handle.pack(anchor='w',padx=20)
    label_handle=tk.Label(master=frame_handle,text="Twitter Handle : ",bg="#B0E2FF",font="Verdana 10 bold italic",fg="#0D4F8B")
    label_handle.pack(side="left")
    label_handle2=tk.Label(master=frame_handle,text=fetch.handle,font="Verdana 10 ",bg="#B0E2FF")
    label_handle2.pack(side="right")

    frame_bio=tk.Frame(bg="#B0E2FF")
    frame_bio.pack(anchor="w",padx=20,pady=5)
    label_bio=tk.Label(master=frame_bio,text="Bio : ",bg="#B0E2FF",font="Verdana 10 bold italic",fg="#0D4F8B")
    label_bio.pack(side="left")
    label_bio2=tk.Label(master=frame_bio,text=fetch.bio,font="Verdana 10",bg="#B0E2FF",wraplength=400,justify=tk.LEFT)
    label_bio2.pack(side="right")

    #Displaying Tweets
    frame_tweet=tk.Frame(bg="#B0E2FF")
    frame_tweet.pack(anchor='w',padx=30)
    tweet_head_date=tk.Label(master=frame_tweet,width=10,text="Date",bg="#6495ED",font="Helvetica 10")
    tweet_head_date.pack(side=tk.LEFT,pady=5)
    tweet_head_cont=tk.Label(master=frame_tweet,width=50,text="Tweet",bg="#6495ED",font="Helvetica 10")
    tweet_head_cont.pack(side=tk.RIGHT,pady=5,padx=10)

    cont=list(fetch.tws.keys())
    dates=list(fetch.tws.values()) 

    frm_tw=tk.Frame(bg="#B0E2FF")
    frm_tw.pack(anchor='w')
    for i in range(len(dates)):
        tweet_frame=tk.Frame(master=frm_tw,bg="#B0E2FF")
        tweet_frame.pack(anchor='w',padx=30,pady=5)
        td=tk.Label(master=tweet_frame,text=dates[i],width=10,justify=tk.LEFT,bg="#B0E2FF",font="arial 9 italic")
        td.pack(side=tk.LEFT,pady=2)
        tc=tk.Label(master=tweet_frame,text=cont[i],wraplength=350,justify=tk.LEFT,bg="#B0E2FF")
        tc.pack(side=tk.RIGHT,pady=2,padx=10,ipadx=2)
    
    
#GO Button
btn_go=tk.Button(text="Go",font="Arial 12",bg="#0D4F8B",fg="white",command=func)
btn_go.pack(pady=5)

window.mainloop()
