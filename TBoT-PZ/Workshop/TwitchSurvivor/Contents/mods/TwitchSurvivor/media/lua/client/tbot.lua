function afficheTexte()
    local player = getSpecificPlayer(0)

    TwitchSurvivorTime = GameTime:getInstance();
    TwitchSurvivor = TwitchSurvivorTime:getModData();
    TwitchSurvivor.TwitchSurvivorBag =player:getInventory():getItemFromTypeRecurse("TwitchSurvivor.Bag_TwitchSurvivor")

    local file=getModFileReader("TwitchSurvivor","media/config/butin.txt",false)
    if not file then return end
    local lines = "" -- empty table for now
    local efface = false
    while true do
        local line = file:readLine() -- read a line, not sure if BufferedReader class can return the whole file at once.
        if line == nil or line=="" then -- nothing returned, end of file, close and break from loop
            file:close()
            break
        end
        TwitchSurvivor.TwitchSurvivorBag:getInventory():AddItem(line)
        efface=true
    end

    if efface == true then
        local textebot=getModFileWriter("TwitchSurvivor","/media/config/butin.txt",true, false)
        textebot:write("")
        textebot:close()
    end

    local textebot=getModFileReader("TwitchSurvivor","/media/config/radio.txt",true)
    local phrase = textebot:readLine()
    textebot:close()
    if phrase ~= nil then -- player:getInventory():getItemFromTypeRecurse("TwitchSurvivor.Bag_TwitchSurvivor")
        player:Say(phrase)
        local textebot=getModFileWriter("TwitchSurvivor","/media/config/radio.txt",true, false)
        textebot:write("")
        textebot:close()
    end

end
Events.EveryOneMinute.Add(afficheTexte)