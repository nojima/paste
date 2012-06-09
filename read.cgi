#!/usr/bin/env ruby
# coding: utf-8
require 'cgi'
require 'sqlite3'

def method_not_allowed(cgi)
  cgi.out('status' => 'MOTHOD_NOT_ALLOWED', 'type' => 'text/html') do
    "<title>Paste</title><h2>405 Method Not Allowed</h2>"
  end
  exit
end

def not_found(cgi)
  cgi.out('status' => 'NOT_FOUND', 'type' => 'text/html') do
    "<title>Paste</title><h2>404 Not Found</h2>"
  end
  exit
end

cgi = CGI.new

if cgi.request_method and cgi.request_method != "GET"
  method_not_allowed(cgi)
end

id = File.basename(cgi.path_info, '.txt')
db = SQLite3::Database.new('paste.db')
text = db.get_first_value('SELECT text FROM Texts WHERE id = ?', id)

if text
  cgi.out('type' => 'text/plain') { text }
else
  not_found(cgi)
end
