function afficheTexte()
    local player = getSpecificPlayer(0)

    TwitchSurvivorsBag =player:getInventory():getItemFromTypeRecurse("TwitchSurvivors.Bag_TwitchSurvivors")

    local file=getModFileReader("TwitchSurvivors","media/config/butin.txt",false)
    if not file then return end
    local lines = "" -- empty table for now
    local efface = false
    while true do
        local line = file:readLine() -- read a line, not sure if BufferedReader class can return the whole file at once.
        if line == nil or line=="" then -- nothing returned, end of file, close and break from loop
            file:close()
            break
        end
        TwitchSurvivorsBag:getInventory():AddItem(line)
        efface=true
    end

    if efface == true then
        local textebot=getModFileWriter("TwitchSurvivors","/media/config/butin.txt",true, false)
        textebot:write("")
        textebot:close()
    end

    local textebot=getModFileReader("TwitchSurvivors","/media/config/radio.txt",true)
    local phrase = textebot:readLine()
    textebot:close()
    if phrase ~= nil then -- player:getInventory():getItemFromTypeRecurse("TwitchSurvivors.Bag_TwitchSurvivors")
        player:Say(phrase)
        local textebot=getModFileWriter("TwitchSurvivors","/media/config/radio.txt",true, false)
        textebot:write("")
        textebot:close()
    end

end
Events.EveryOneMinute.Add(afficheTexte)
