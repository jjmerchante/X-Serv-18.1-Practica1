#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp
import urllib


class acorta(webapp.webApp):

    numUrl = 0
    dictUrl = {}
    dictNewUrl = {}

    def htmlFormat(self, body):
        return '<html><body><p>' + body + '</p></body></html>'

    def addURL(self, url):
        if url not in self.dictUrl.keys():
            newURL = "http://localhost:1236/" + str(self.numUrl)
            self.numUrl += 1
            self.dictUrl[url] = newURL
            self.dictNewUrl[newURL] = url
        else:
            newURL = self.dictUrl[url]
        return newURL

    def getHtmlListUrls(self):
        urlshtml = ""
        for url in self.dictUrl.keys():
            urlshtml += "<p><a href=" + url + ">" + url + "</a>" + \
                "   -->   " + "<a href=" + self.dictUrl[url] + ">" + \
                self.dictUrl[url] + "</a></p>"
        return urlshtml

    def parse(self, request):
        verb = request.split(" ")[0]
        resource = request.split(" ")[1]
        body = request.split("\r\n\r\n", 1)[1]
        return (verb, resource, body)

    def process(self, parsedRequest):
        (verb, resource, body) = parsedRequest

        formul = '<form action="" method="POST" accept-charset="UTF-8">' + \
            'URL para acortar: <input type="text" name="url">' + \
            '<input type="submit" value="Acorta!"></form>'

        if verb == "GET":
            if resource == "/":
                httpCode = "200 OK"
                urlshtml = self.getHtmlListUrls()
                httpBody = self.htmlFormat(formul + urlshtml)
            else:
                url = "http://localhost:1236" + resource
                if url in self.dictNewUrl.keys():
                    urlRedir = self.dictNewUrl[url]
                    httpCode = '301 Redirect\nLocation: ' + urlRedir
                    httpBody = self.htmlFormat(
                        "<a href=" + urlRedir + ">Pincha si no redirige</a>")
                else:
                    httpCode = "404 Recurso no disponible"
                    httpBody = self.htmlFormat("404 Recurso no disponible")
        elif verb == "POST" and resource == "/":
            url = body.split("url=", 1)[1]
            url = urllib.unquote(url)
            if not url.startswith("http://") and \
                    not url.startswith("https://"):
                url = "http://" + url
            newURL = self.addURL(url)
            httpCode = "200 OK"
            body = "<p><a href=" + url + ">" + url + "</a>" + \
                "  -->  <a href=" + newURL + ">" + newURL + "</a></p>"
            httpBody = self.htmlFormat(body)
        else:
            httpCode = "404 Not Found"
            httpBody = self.htmlFormat("Metodo no disponible")

        return (httpCode, httpBody)

if __name__ == '__main__':
    try:
        testacorta = acorta("localhost", 1236)
    except KeyboardInterrupt:
        print "\nCerrando el servidor\n"
