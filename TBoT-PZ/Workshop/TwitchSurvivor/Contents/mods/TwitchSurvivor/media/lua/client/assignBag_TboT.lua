function assignBag()

    local player = getSpecificPlayer(0)
    TBoTTime = GameTime:getInstance();
    TBoT = TBoTTime:getModData();
    if TBoT.tbag == nil then
        TBoT.tbag=player:getInventory():AddItem("TwitchSurvivor.Bag_TwitchSurvivor")
    end
end
Events.OnNewGame.Add(assignBag)
