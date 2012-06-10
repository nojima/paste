#!/usr/bin/env ruby
# coding: utf-8
require 'cgi'
require 'erb'
require 'sqlite3'
require 'digest/sha1'
require './lib/common'

def save_text(id, type, text, cgi)
  unless SupportedFileTypes.include?(type)
    bad_request
  end

  db = SQLite3::Database.new('db/paste.sqlite3')
  10.times do
    begin
      db.execute("INSERT INTO Texts (id, type, text) VALUES (?, ?, ?)", [id, type, text])
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

case cgi.request_method
when "GET"
  erb = ERB.new(IO.read('./view/new.html.erb'))
  cgi.out { erb.result(binding) }
when "POST"
  type = cgi['type']
  text = cgi['text']
  id = Digest::SHA1.hexdigest(type + ":" + text)
  save_text(id, type, text, cgi)

  cgi.out('status' => 'REDIRECT', 'type' => 'text/html', 'location' => "#{id}#{type}") do
    "<title>Paste</title><h1>Submitted</h1>"
  end
else
  method_not_allowed(cgi)
end
