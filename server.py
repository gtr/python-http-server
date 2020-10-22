import socket
import sys

# NOTE: it works but it takes LONG time to actually load the html content im not sure why

class HTML(object):
    """
    Class for HTML content
    """
    def __init__(self):
        self.home_counter = 0
        self.page2_counter = 0
        self.page3_counter = 0

    def get_home(self):
        content = "<HTML><HEAD><TITLE>HTTP Homework</TITLE></HEAD><BODY><H3><CENTER>HTTP Homework</CENTER></H3>This is the main page<P>You can click on <A HREF=”/page2”>page 2</A> or <A HREF=”/page3”>or Page 3</A><P><CENTER>This server has been used " + str(self.home_counter) + " times</CENTER></BODY></HTML>"
        return content.encode()

    def get_page2(self):
        content = "<HTML><HEAD><TITLE>HTTP Homework</TITLE></HEAD><BODY><H3><CENTER>HTTP Homework</CENTER></H3>This is page 2<P>You can go <A HREF=”/”>back</A> <P><CENTER>This server has been used " + str(self.page2_counter) + " times</CENTER></BODY></HTML>"
        return content.encode()

    def get_page3(self):
        content = "<HTML><HEAD><TITLE>HTTP Homework</TITLE></HEAD><BODY><H3><CENTER>HTTP Homework</CENTER></H3>This is page 3<P>You can go <A HREF=”/”>back</A> <P><CENTER>This server has been used " + str(self.page3_counter) + " times</CENTER></BODY></HTML>"
        return content.encode()

    def get404(self):
        return "<HTML>404: not found</HTML>".encode()

    def increase_counter(self, page):
        """
        Increases the counter for a given page number
        """
        if page == 1:
            self.home_counter += 1
        elif page == 2:
            self.page2_counter += 1
        elif page == 3:
            self.page3_counter += 1
        else:
            print("wrong input")
            sys.exit(1)


class HTTPServer(object):
    """
    HTTP server
    """
    def __init__(self):
        self.HOST = "localhost"
        self.PORT = 8080
        self.HTML = HTML()
    
    def go(self):
        """
        Main entry point for server 
        """
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Starting HTTP server on " + self.HOST + ":" + str(self.PORT))
        self.socket.bind((self.HOST, self.PORT))

        self.socket.listen()

        while True:
            client, address = self.socket.accept()
            self.handle_connection(client, address)


    def handle_connection(self, client, address):
        """
        Handles incoming an client connection (just one for now)
        """
        while True:
            data = client.recv(1024).decode()
            method = data.split("\n")[0].split(" ")[0]
            doc = data.split("\n")[0].split(" ")[1]

            if method == "GET":
                self.handle_GET(client, doc)
            else:
                print("Unknown method")
                sys.exit(1)

    
    def handle_GET(self, client, doc):
        """
        Handles a GET request - no other requests handled atm
        """
        if doc == "/":
            self.HTML.increase_counter(1)
            response = self.build_http_header(200)
            response += self.HTML.get_home()
        elif doc == "/page2":
            self.HTML.increase_counter(2)
            response = self.build_http_header(200)
            response += self.HTML.get_page2()
        elif doc == "/page3":
            self.HTML.increase_counter(3)
            response = self.build_http_header(200)
            response += self.HTML.get_page3()
        else:
            response = self.build_http_header(404)
            response += self.HTML.get404()

        print(response)

        client.send(response)

        

    def build_http_header(self, code):
        """
        Builds http header for a given code
        """
        if code == 200:
            header = "HTTP/1.1 200 OK\r\n"
        elif code == 404:
            header = "HTTP/1.1 404 Not Found\r\n"
        else:
            sys.exit(1)
        
        header += "Server: gtc250\r\n"
        header += "Content-Type: text/html\r\n"
        header += "Connection: Closed\r\n\r\n"
        
        return header.encode()
        



def main():
    srv = HTTPServer()
    srv.go() # go!


main()

    


