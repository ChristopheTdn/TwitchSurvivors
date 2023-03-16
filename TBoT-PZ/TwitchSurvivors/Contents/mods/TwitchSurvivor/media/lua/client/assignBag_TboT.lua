function assignBag()

    local player = getSpecificPlayer(0)
    TwitchSurvivorsBag=player:getInventory():AddItem("TwitchSurvivors.Bag_TwitchSurvivors")
end
Events.OnNewGame.Add(assignBag)
