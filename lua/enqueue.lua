local redis = require "resty.redis"
local red = redis:new()
local ok, err = red:connect("127.0.0.1", 6379)

if not ok then
    ngx.say("failed to connect: ", err)
    return
end

function string.starts(String,Start)
   return string.sub(String,1,string.len(Start))==Start
end

if string.starts(ngx.var.request_uri, '/simple') then
    ok, err = red:rpush("hotqueue:cheeseshop", ngx.var.request_uri)
    if not ok then
        ngx.say("failed to append to list: ", err)
        return
    end
end

ngx.exit(ngx.HTTP_NOT_FOUND)