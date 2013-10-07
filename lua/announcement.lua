-- @ Reids server filter user announcement
-- key tp,users:formats
-- result tp:formats

local announce = KEYS[1]
local receipt = KEYS[2]
local uid = KEYS[3]
local receipts = {}
local result = {}

local function split_key(key)
   local pos = string.find(key, ":")
   
   if not pos then
      return nil
   end

   local flags = string.sub(key, 0, pos - 1)
   local formats = string.sub(key, pos, -1)
   local tp, users = 0, ''
   pos = string.find(flags, ',')
   tp = string.sub(flags, 0, pos - 1)
   users = string.sub(flags, pos + 1, -1)

   return (users == '0' or string.find(users, uid) and string.find(receipt, tp)), tp .. formats
end

for i, key in pairs(redis.call("zrevrange", announce, 0, -1)) do
   local match, data = split_key(key)

   if match then
      table.insert(result, data)
   end
end

return result
