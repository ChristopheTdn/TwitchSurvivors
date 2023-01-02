function afficheTexte()

    local player = getSpecificPlayer(0)
    local textebot=getModFileReader("TBoT","texte.txt",true)
    local phrase = textebot:readLine()
    textebot:close()
    if phrase ~= nil then -- player:getInventory():getItemFromTypeRecurse("TBoT.Bag_TBoT")
        player:Say(phrase)
        local textebot=getModFileWriter("TBoT","texte.txt",true, false)
        textebot:write("")
        textebot:close()
        TBoTable["tbagData"]:getInventory():AddItem("Base.Pistol")
    end
end

Events.EveryOneMinute.Add(afficheTexte)