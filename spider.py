#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

import mechanize
import urllib
from bs4 import BeautifulSoup
import urlparse
import pyperclip

# TODO;
# When a link is deleted the button remains
# remove duplicate links
# sort out radio buuton visibility

copy      = 0
link_dict = {}

class Spider(App):
    pass

class Searchterm(TextInput):
    def searchterm(self, text):
        global search_term # kv id is out of scope
        search_term = text
        return search_term

class GetLinksButton(Button):

    link_number = 1

    def add_buttons(self, links):
        link_list = [] # incase user wants to copy the links to the clipboard
        for link in links:
            count = GetLinksButton.link_number
            link_list.append(link)
            link_button = LinkButton(
                text='link number ' + str(count)
            )
            GetLinksButton.link_number += 1
            self.links_grid.add_widget(link_button)
            link_dict[count] = link
        return link_list

    def get_links(self):
        links     = GetLinks()
        link_list = links.get_links()
        return link_list

    # Also handles copying to the clipboard
    def run(self):
        global copy
        links = self.get_links()
        if copy == 'copy_all' :
            links = ''
            link_list = self.add_buttons(links)
            for link in link_list:
                links.append(link+'/n')
            pyperclip.copy(links)
        elif copy == 'copy_first':
            link_list = self.add_buttons(links)
            link = link_list.pop()
            pyperclip.copy(link)
        else:
            self.add_buttons(links)
        copy = 0


class Clearlinkbuttons(Button):

    def clear_links(self):
        self.links_grid.clear_widgets()
        GetLinksButton.link_number = 1

class Checkbox(CheckBox):
    def on_check(self, state):
        global copy
        copy = state

##
class LinkButton(Button):
    def popup(self, text):
        ref = int(text[12:])
        pop = Del_view_copy(key=ref)
        pop.open()

#####
class Del_view_copy(Popup):

    text = StringProperty()

    def __init__(self, key, **kwargs):
        super(Del_view_copy, self).__init__(**kwargs)
        self.key   = key
        self.text  = link_dict[key]
        self.title = 'link no. %s' %(key)

    def copy(self):
        pyperclip.copy(self.link)

    def delete(self):
        del link_dict[self.key]

    def close(self):
        self.dismiss()


class GetLinks:
    goog = "https://www.google.co.uk/search?client=ubuntu&channel=fs&q="

    @classmethod
    def get_browser(cls):
        br            = mechanize.Browser()
        br.addheaders = [('user_agent','chrome')]
        br.set_handle_robots(False)
        return br

    def get_links(self):
        urls     = []
        br       = self.get_browser()
        htmltext = br.open(self.goog + search_term).read()
        soup     = BeautifulSoup(htmltext)
        for tag in soup.findAll('a',href=True):
            raw     = tag['href']
            b1      = urlparse.urlparse(tag['href']).hostname
            b2      = urlparse.urlparse(tag['href']).path
            new_url = "http://"+ str(b1)+str(b2)
            urls.append(new_url)
        return urls

if __name__=='__main__':
    Test().run()

