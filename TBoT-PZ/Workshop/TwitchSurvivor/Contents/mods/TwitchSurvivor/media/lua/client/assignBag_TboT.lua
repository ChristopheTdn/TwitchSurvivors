function assignBag()

    local player = getSpecificPlayer(0)
    TwitchSurvivorsTime = GameTime:getInstance();
    TwitchSurvivors = TwitchSurvivors:getModData();
    if TwitchSurvivors.TwitchSurvivorsBag == nil then
        TwitchSurvivors.TwitchSurvivorsBag=player:getInventory():AddItem("TwitchSurvivors.Bag_TwitchSurvivors")
    end
end
Events.OnNewGame.Add(assignBag)
