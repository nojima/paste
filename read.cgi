#!/usr/bin/env ruby
# coding: utf-8
require 'cgi'
require 'sqlite3'

def method_not_allowed(cgi)
  cgi.out('status' => 'MOTHOD_NOT_ALLOWED', 'type' => 'text/html') do
    "<title>Paste</title><h1>405 Method Not Allowed</h1>"
  end
  exit
end

def not_found(cgi)
  cgi.out('status' => 'NOT_FOUND', 'type' => 'text/html') do
    "<title>Paste</title><h1>404 Not Found</h1>"
  end
  exit
end

def service_unavailable(cgi)
  cgi.out('status' => 'SERVICE_UNAVAILABLE', 'type' => 'text/html') do
    "<title>Paste</title><h1>503 Service Unavailable</h1>"
  end
  exit
end

def read_text(id, cgi)
  db = SQLite3::Database.new('db/paste.sqlite3')
  10.times do
    begin
      return db.get_first_value('SELECT text FROM Texts WHERE id = ?', id)
    rescue SQLite3::BusyException
      sleep 0.5
    end
  end
  service_unavailable(cgi)
end

cgi = CGI.new

if cgi.request_method and cgi.request_method != "GET"
  method_not_allowed(cgi)
end

id = File.basename(cgi.path_info, '.txt')
text = read_text(id, cgi)

if text
  cgi.out('type' => 'text/plain; charset=utf-8') { text }
else
  not_found(cgi)
end
