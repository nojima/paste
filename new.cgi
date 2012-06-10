#!/usr/bin/env ruby
# coding: utf-8
require 'cgi'
require 'sqlite3'
require 'digest/sha1'
require './lib/common'

def save_text(id, text, cgi)
  db = SQLite3::Database.new('db/paste.sqlite3')
  10.times do
    begin
      db.execute("INSERT INTO Texts (id, text) VALUES (?, ?)", [id, text])
      return true
    rescue SQLite3::SQLException
      # ignore SQL errors
      return true
    rescue SQLite3::BusyException
      # wait when DB is busy
      sleep 0.5
    end
  end
  service_unavailable(cgi)
end

cgi = CGI.new

if cgi.request_method and cgi.request_method != "POST"
  method_not_allowed(cgi)
end

text = cgi['text']
id = Digest::SHA1.hexdigest(text)
save_text(id, text, cgi)

cgi.out('status' => 'REDIRECT', 'type' => 'text/html', 'location' => "#{id}.txt") do
  "<title>Paste</title><h1>Submitted</h1>"
end
