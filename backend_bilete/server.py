import http.server
import json
import os

port = 8081
data_file = 'db.json'

class tickethandler(http.server.BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        # aprobam cererile de test de la browser
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    def do_GET(self):

        if self.path == '/tickets':
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as file:
                    tickets_data = file.read()
            else:
                tickets_data = "[]"
            
            self.send_response(200)#200 ok, exista path ul
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(tickets_data.encode('utf-8'))
        elif self.path.startswith('/tickets/'):
            ticket_id = int(self.path.split('/')[-1])
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as file:
                    tickets=json.loads(file.read())
                    ticket_wanted=[t for t in tickets if t['id']==ticket_id]
                    if ticket_wanted:
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(ticket_wanted[0]).encode('utf-8'))
                    else:
                        self.send_response(404)
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('content-type', 'application/json')
                        self.end_headers()
                        mesaj=json.dumps({"message":"biletul nu exista"})
                        self.wfile.write(mesaj.encode('utf-8'))
                
        else:
            # codul 404 pentru not found
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('content-type', 'application/json')#?
            self.end_headers()
            
            mesaj = json.dumps({"message": "ruta nu exista"})
            self.wfile.write(mesaj.encode('utf-8'))
    
    def do_POST(self):
        if self.path == '/tickets':
            # unitate de masura ca sa stim cand incheiem
            content_length = int(self.headers['Content-Length'])
            
            # cererea de la client
            post_data = self.rfile.read(content_length)
            new_ticket = json.loads(post_data.decode('utf-8'))

            # citim ce avem deja in fisier
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as file:
                    tickets = json.loads(file.read())
            else:
                tickets = []
            new_id = 1
            if tickets:
                new_id = max(t['id'] for t in tickets) + 1
            
            new_ticket['id'] = new_id

            tickets.append(new_ticket)
            with open(data_file, 'w', encoding='utf-8') as file:
                file.write(json.dumps(tickets, indent=4))

            self.send_response(201)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(new_ticket).encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('content-type', 'application/json')
            self.end_headers()
            mesaj = json.dumps({"message": "ruta nu exista"})
            self.wfile.write(mesaj.encode('utf-8'))
    
    def do_DELETE(self):
        if self.path.startswith('/tickets/'):
            ticket_id = int(self.path.split('/')[-1])
        if(os.path.exists(data_file)):
            with open(data_file, 'r', encoding='utf-8') as file:
                tickets = json.loads(file.read())
            new_tickets=[t for t in tickets if t['id']!=ticket_id]  
        if len(tickets) > len(new_tickets):
                    with open(data_file, 'w', encoding='utf-8') as file:
                        file.write(json.dumps(new_tickets, indent=4))
                    
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"message": "bilet sters"}).encode())    
                
           
        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('content-type', 'application/json')
            self.end_headers()
            mesaj = json.dumps({"message": "ruta nu exista"})
            self.wfile.write(mesaj.encode('utf-8'))  
    def do_PUT(self):
             if self.path.startswith('/tickets/'):
                ticket_id = int(self.path.split('/')[-1])
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                updated_ticket = json.loads(put_data.decode('utf-8'))
                
                if os.path.exists(data_file):
                    with open(data_file, 'r', encoding='utf-8') as file:
                        tickets = json.loads(file.read())
                    
                    for i, t in enumerate(tickets):
                        if t['id'] == ticket_id:
                            updated_ticket['id'] = ticket_id
                            tickets[i] = updated_ticket
                            with open(data_file, 'w', encoding='utf-8') as file:
                                file.write(json.dumps(tickets, indent=4))
                            
                            self.send_response(200)
                            self.send_header('Access-Control-Allow-Origin', '*')
                            self.send_header('content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps(updated_ticket).encode('utf-8'))
                            return
                    
                    self.send_response(404)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('content-type', 'application/json')
                    self.end_headers()
                    mesaj = json.dumps({"message": "biletul nu exista"})
                    self.wfile.write(mesaj.encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('content-type', 'application/json')
                    self.end_headers()
                    mesaj = json.dumps({"message": "biletul nu exista"})
                    self.wfile.write(mesaj.encode('utf-8'))



def run():
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, tickethandler)
    
    print(f"serverul ruleaza pe http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()