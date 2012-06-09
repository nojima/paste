#!/usr/bin/env ruby
# coding: utf-8
require 'cgi'
require 'sqlite3'
require 'digest/sha1'

def method_not_allowed(cgi)
  cgi.out('status' => 'MOTHOD_NOT_ALLOWED', 'type' => 'text/html') do
    "<title>Paste</title><h2>405 Method Not Allowed</h2>"
  end
  exit
end

cgi = CGI.new

if cgi.request_method and cgi.request_method != "POST"
  method_not_allowed(cgi)
end

text = cgi['text']
id = Digest::SHA1.hexdigest(text)

db = SQLite3::Database.new('paste.db')
db.execute("INSERT INTO Texts (id, text) VALUES (?, ?)", [id, text])

cgi.out('status' => 'REDIRECT', 'type' => 'text/html', 'location' => "#{id}.txt") do
  "<title>Paste</title><h2>Submitted</h2>"
end
