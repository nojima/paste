#!/usr/bin/env ruby
# coding: utf-8
require 'cgi'
require 'erb'
require 'sqlite3'
require './lib/common.rb'

def read_record(id, cgi)
  db = SQLite3::Database.new('db/paste.sqlite3')
  10.times do
    begin
      return db.get_first_row('SELECT type, text FROM Texts WHERE id = ?', id)
    rescue SQLite3::BusyException
      sleep 0.5
    end
  end
  service_unavailable(cgi)
end

def render(id, type, text, cgi)
  case type
  when '.txt'
    cgi.out('type' => 'text/plain; charset=utf-8') { text }
  when '.tex'
    erb = ERB.new(IO.read('./view/mathjax.html.erb'))
    cgi.out('type' => 'text/html; charset=utf-8') {
      include ERB::Util
      erb.result(binding)
    }
  end
end

cgi = CGI.new

case cgi.request_method
when 'GET'
  type = File.extname(cgi.path_info)
  id = File.basename(cgi.path_info, type)
  record = read_record(id, cgi)

  if record and (type == record[0] or type == '.txt')
    render(id, type, record[1], cgi)
  else
    not_found(cgi)
  end
when 'POST':
  type = cgi['type']
  text = cgi['text']
  if SupportedFileTypes.include?(type)
    render('Preview', type, text, cgi)
  else
    bad_request
  end
else
  method_not_allowed(cgi)
end
