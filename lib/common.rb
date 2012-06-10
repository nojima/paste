#!/usr/bin/env ruby
# coding: utf-8

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
