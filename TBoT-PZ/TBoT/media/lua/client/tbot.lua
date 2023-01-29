function afficheTexte()

    local player = getSpecificPlayer(0)
    local file=getModFileReader("TBoT","butin.txt",false)
    if not file then return end
    local lines = "" -- empty table for now
    local efface = false
    while true do
        local line = file:readLine() -- read a line, not sure if BufferedReader class can return the whole file at once.
        if line == nil or line=="" then -- nothing returned, end of file, close and break from loop
            file:close()
            break
        end
        TBoT.tbag:getInventory():AddItem(line)
        efface=true
    end

    if efface == true then
        local textebot=getModFileWriter("TBoT","butin.txt",true, false)
        textebot:write("")
        textebot:close()
    end

    local textebot=getModFileReader("TBoT","texte.txt",true)
    local phrase = textebot:readLine()
    textebot:close()
    if phrase ~= nil then -- player:getInventory():getItemFromTypeRecurse("TBoT.Bag_TBoT")
        player:Say(phrase)
        local textebot=getModFileWriter("TBoT","texte.txt",true, false)
        textebot:write("")
        textebot:close()
    end

end
Events.EveryOneMinute.Add(afficheTexte)